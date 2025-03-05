use std::collections::VecDeque;
use serde::{Serialize, Deserialize};
use std::time::{Instant, Duration};
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CacheHistoryEntry {
    timestamp: Instant,
    operation: CacheOperation,
    key: String,
    value_size: usize,
    success: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum CacheOperation {
    Insert,
    Get,
    Remove,
    Invalidate,
    Recovery,
}

pub struct CacheHistory {
    entries: VecDeque<CacheHistoryEntry>,
    max_entries: usize,
    log_file: String,
    last_backup: Instant,
    backup_interval: Duration,
}

impl CacheHistory {
    pub fn new(max_entries: usize, log_file: &str) -> Self {
        Self {
            entries: VecDeque::with_capacity(max_entries),
            max_entries,
            log_file: log_file.to_string(),
            last_backup: Instant::now(),
            backup_interval: Duration::from_secs(300), // 5 minutes
        }
    }

    pub fn record(&mut self, operation: CacheOperation, key: String, value_size: usize, success: bool) {
        let entry = CacheHistoryEntry {
            timestamp: Instant::now(),
            operation,
            key,
            value_size,
            success,
        };

        if self.entries.len() >= self.max_entries {
            self.entries.pop_front();
        }
        self.entries.push_back(entry);
        self.maybe_backup();
    }

    fn maybe_backup(&mut self) {
        if self.last_backup.elapsed() >= self.backup_interval {
            self.backup();
            self.last_backup = Instant::now();
        }
    }

    fn backup(&self) {
        let backup_data = serde_json::to_string(&self.entries).unwrap();
        fs::write(&self.log_file, backup_data).expect("Failed to write backup");
    }

    pub fn recover(&mut self) -> Result<(), String> {
        if Path::new(&self.log_file).exists() {
            let data = fs::read_to_string(&self.log_file)
                .map_err(|e| format!("Failed to read backup: {}", e))?;
            
            let recovered: VecDeque<CacheHistoryEntry> = serde_json::from_str(&data)
                .map_err(|e| format!("Failed to parse backup: {}", e))?;
            
            self.entries = recovered;
            Ok(())
        } else {
            Ok(())
        }
    }

    pub fn get_stats(&self) -> CacheHistoryStats {
        let mut stats = CacheHistoryStats::default();
        
        for entry in &self.entries {
            match entry.operation {
                CacheOperation::Insert => stats.inserts += 1,
                CacheOperation::Get => stats.gets += 1,
                CacheOperation::Remove => stats.removes += 1,
                CacheOperation::Invalidate => stats.invalidations += 1,
                CacheOperation::Recovery => stats.recoveries += 1,
            }
            if entry.success {
                stats.successful_operations += 1;
            } else {
                stats.failed_operations += 1;
            }
        }
        
        stats
    }
}

#[derive(Debug, Default)]
pub struct CacheHistoryStats {
    pub inserts: u64,
    pub gets: u64,
    pub removes: u64,
    pub invalidations: u64,
    pub recoveries: u64,
    pub successful_operations: u64,
    pub failed_operations: u64,
} 