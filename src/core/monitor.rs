use chrono::{DateTime, Utc};
use serde::{Serialize, Deserialize};
use std::fs::{File, OpenOptions};
use std::io::Write;

#[derive(Serialize, Deserialize, Debug)]
pub struct OperationLog {
    timestamp: DateTime<Utc>,
    operation: String,
    status: String,
    performance_metrics: Metrics,
    changes: Vec<Change>,
}

#[derive(Serialize, Deserialize, Debug)]
struct Metrics {
    execution_time_ms: f64,
    memory_usage_kb: u64,
    success_rate: f64,
}

#[derive(Serialize, Deserialize, Debug)]
struct Change {
    file: String,
    commit_hash: String,
    changes: String,
}

impl OperationLog {
    pub fn log(&self) -> Result<(), std::io::Error> {
        let log_file = OpenOptions::new()
            .create(true)
            .append(true)
            .open("lumascript_operations.log")?;
            
        writeln!(log_file, "{}", serde_json::to_string(self)?)?;
        Ok(())
    }
} 