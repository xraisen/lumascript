use std::collections::HashMap;
use std::time::{Duration, Instant};
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CacheEntry<T> {
    value: T,
    created_at: Instant,
    last_accessed: Instant,
    access_count: u64,
}

pub struct Cache<T> {
    entries: HashMap<String, CacheEntry<T>>,
    max_size: usize,
    ttl: Duration,
    hit_count: u64,
    miss_count: u64,
}

impl<T: Clone> Cache<T> {
    pub fn new(max_size: usize, ttl_seconds: u64) -> Self {
        Self {
            entries: HashMap::with_capacity(max_size),
            max_size,
            ttl: Duration::from_secs(ttl_seconds),
            hit_count: 0,
            miss_count: 0,
        }
    }

    pub fn get(&mut self, key: &str) -> Option<T> {
        if let Some(entry) = self.entries.get_mut(key) {
            if entry.created_at.elapsed() <= self.ttl {
                entry.last_accessed = Instant::now();
                entry.access_count += 1;
                self.hit_count += 1;
                Some(entry.value.clone())
            } else {
                self.entries.remove(key);
                self.miss_count += 1;
                None
            }
        } else {
            self.miss_count += 1;
            None
        }
    }

    pub fn insert(&mut self, key: String, value: T) {
        if self.entries.len() >= self.max_size {
            // Remove least recently used entry
            let lru_key = self.entries
                .iter()
                .min_by_key(|(_, entry)| entry.last_accessed)
                .map(|(k, _)| k.clone());
            
            if let Some(key) = lru_key {
                self.entries.remove(&key);
            }
        }

        self.entries.insert(key, CacheEntry {
            value,
            created_at: Instant::now(),
            last_accessed: Instant::now(),
            access_count: 0,
        });
    }

    pub fn stats(&self) -> CacheStats {
        CacheStats {
            size: self.entries.len(),
            hit_count: self.hit_count,
            miss_count: self.miss_count,
            hit_ratio: if self.hit_count + self.miss_count > 0 {
                self.hit_count as f64 / (self.hit_count + self.miss_count) as f64
            } else {
                0.0
            },
        }
    }
}

#[derive(Debug)]
pub struct CacheStats {
    pub size: usize,
    pub hit_count: u64,
    pub miss_count: u64,
    pub hit_ratio: f64,
} 