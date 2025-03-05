use chrono::{DateTime, Utc};
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
pub struct VersionInfo {
    timestamp: DateTime<Utc>,
    commit_hash: String,
    changes: Vec<Change>,
    status: ComponentStatus,
}

impl VersionInfo {
    pub fn log_change(&mut self, component: &str, change: &str) {
        self.changes.push(Change {
            component: component.to_string(),
            description: change.to_string(),
            timestamp: Utc::now(),
        });
    }
} 