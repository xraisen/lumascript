use chrono::{DateTime, Utc};
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct TimeStamp {
    created: DateTime<Utc>,
    modified: DateTime<Utc>,
    operation: String,
    status: String,
}

impl TimeStamp {
    pub fn new(operation: &str) -> Self {
        let now = Utc::now();
        Self {
            created: now,
            modified: now,
            operation: operation.to_string(),
            status: "initialized".to_string(),
        }
    }

    pub fn update(&mut self, status: &str) {
        self.modified = Utc::now();
        self.status = status.to_string();
    }
} 