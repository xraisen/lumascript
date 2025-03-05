use wasm_bindgen::prelude::*;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;

#[wasm_bindgen]
pub struct WasmInterpreter {
    operations: Arc<AtomicUsize>,
    last_operation: String,
    monitor: OperationMonitor,
}

#[wasm_bindgen]
impl WasmInterpreter {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        console_error_panic_hook::set_once();
        Self {
            operations: Arc::new(AtomicUsize::new(0)),
            last_operation: String::new(),
            monitor: OperationMonitor::new(),
        }
    }

    pub fn interpret(&mut self, hex: &str) -> Result<JsValue, JsValue> {
        let start = std::time::Instant::now();
        
        // Log operation start
        self.monitor.log_operation_start("interpret");
        
        // Increment operation counter
        self.operations.fetch_add(1, Ordering::SeqCst);
        
        // Perform interpretation
        let result = match self.process_hex(hex) {
            Ok(val) => {
                self.monitor.log_success();
                Ok(JsValue::from_str(&val))
            },
            Err(e) => {
                self.monitor.log_error(&e.to_string());
                Err(JsValue::from_str(&e.to_string()))
            }
        };

        // Log performance
        self.monitor.log_performance(start.elapsed());
        
        result
    }

    pub fn get_stats(&self) -> String {
        format!(
            "Operations: {}\nLast: {}\nSuccess Rate: {}%",
            self.operations.load(Ordering::SeqCst),
            self.last_operation,
            self.monitor.get_success_rate()
        )
    }
} 