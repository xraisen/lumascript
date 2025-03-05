use tokio::net::{TcpListener, TcpStream};
use tokio::sync::mpsc;
use serde::{Serialize, Deserialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CacheNode {
    id: String,
    address: String,
    port: u16,
    status: NodeStatus,
    last_heartbeat: Instant,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum NodeStatus {
    Active,
    Syncing,
    Recovering,
    Failed,
}

pub struct DistributedCache<T> {
    nodes: Arc<RwLock<HashMap<String, CacheNode>>>,
    local_node: CacheNode,
    sync_channel: mpsc::Sender<SyncMessage>,
    recovery_manager: Arc<RecoveryManager>,
}

impl<T: Clone + Send + Sync> DistributedCache<T> {
    pub async fn new(local_address: String, port: u16) -> Self {
        let local_node = CacheNode {
            id: uuid::Uuid::new_v4().to_string(),
            address: local_address.clone(),
            port,
            status: NodeStatus::Active,
            last_heartbeat: Instant::now(),
        };

        let (sync_tx, sync_rx) = mpsc::channel(100);
        let recovery_manager = Arc::new(RecoveryManager::new());

        let cache = Self {
            nodes: Arc::new(RwLock::new(HashMap::new())),
            local_node: local_node.clone(),
            sync_channel: sync_tx,
            recovery_manager: recovery_manager.clone(),
        };

        // Start background tasks
        tokio::spawn(cache.start_heartbeat());
        tokio::spawn(cache.handle_sync_messages(sync_rx));
        tokio::spawn(cache.monitor_nodes());

        cache
    }

    async fn start_heartbeat(&self) {
        let mut interval = tokio::time::interval(Duration::from_secs(5));
        loop {
            interval.tick().await;
            self.broadcast_heartbeat().await;
        }
    }

    async fn broadcast_heartbeat(&self) {
        let heartbeat = HeartbeatMessage {
            node_id: self.local_node.id.clone(),
            timestamp: Instant::now(),
        };

        let nodes = self.nodes.read().await;
        for node in nodes.values() {
            if let Ok(mut stream) = TcpStream::connect(format!("{}:{}", node.address, node.port)).await {
                if let Ok(_) = serde_json::to_writer(&mut stream, &heartbeat) {
                    // Heartbeat sent successfully
                }
            }
        }
    }

    async fn handle_sync_messages(&self, mut rx: mpsc::Receiver<SyncMessage>) {
        while let Some(message) = rx.recv().await {
            match message {
                SyncMessage::Replicate { key, value } => {
                    self.replicate_value(key, value).await;
                }
                SyncMessage::Invalidate { key } => {
                    self.invalidate_value(key).await;
                }
                SyncMessage::RecoveryRequest { node_id } => {
                    self.handle_recovery_request(node_id).await;
                }
            }
        }
    }

    async fn replicate_value(&self, key: String, value: T) {
        let nodes = self.nodes.read().await;
        for node in nodes.values() {
            if let Ok(mut stream) = TcpStream::connect(format!("{}:{}", node.address, node.port)).await {
                let message = SyncMessage::Replicate {
                    key: key.clone(),
                    value: value.clone(),
                };
                let _ = serde_json::to_writer(&mut stream, &message);
            }
        }
    }

    async fn monitor_nodes(&self) {
        let mut interval = tokio::time::interval(Duration::from_secs(10));
        loop {
            interval.tick().await;
            let mut nodes = self.nodes.write().await;
            let now = Instant::now();
            
            for node in nodes.values_mut() {
                if now.duration_since(node.last_heartbeat) > Duration::from_secs(30) {
                    node.status = NodeStatus::Failed;
                    self.recovery_manager.handle_node_failure(node.id.clone()).await;
                }
            }
        }
    }
} 