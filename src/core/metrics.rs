pub struct PerformanceMetrics {
    cache_hits: usize,
    cache_misses: usize,
    parse_time: Vec<f64>,
    eval_time: Vec<f64>,
}

impl PerformanceMetrics {
    pub fn record_cache_hit(&mut self) {
        self.cache_hits += 1;
    }

    pub fn record_cache_miss(&mut self) {
        self.cache_misses += 1;
    }

    pub fn cache_hit_ratio(&self) -> f64 {
        let total = self.cache_hits + self.cache_misses;
        if total == 0 { return 0.0; }
        self.cache_hits as f64 / total as f64
    }
} 