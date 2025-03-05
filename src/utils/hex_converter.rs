use wasm_bindgen::prelude::*;
use chrono::{DateTime, Utc};

#[wasm_bindgen]
pub struct LumaHexConverter {
    last_operation: Option<DateTime<Utc>>,
    operation_count: u32,
}

#[wasm_bindgen]
impl LumaHexConverter {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        Self {
            last_operation: None,
            operation_count: 0,
        }
    }

    pub fn text_to_hex(&mut self, text: &str) -> String {
        self.last_operation = Some(Utc::now());
        self.operation_count += 1;
        text.bytes()
            .map(|b| format!("{:02x}", b))
            .collect::<String>()
    }

    pub fn hex_to_text(&mut self, hex: &str) -> Result<String, JsValue> {
        self.last_operation = Some(Utc::now());
        self.operation_count += 1;
        
        // Convert hex to bytes
        let bytes = (0..hex.len())
            .step_by(2)
            .filter_map(|i| {
                u8::from_str_radix(&hex[i..i + 2], 16).ok()
            })
            .collect::<Vec<u8>>();

        String::from_utf8(bytes)
            .map_err(|e| JsValue::from_str(&e.to_string()))
    }

    pub fn get_stats(&self) -> String {
        format!(
            "Operations: {}\nLast operation: {}",
            self.operation_count,
            self.last_operation
                .map(|t| t.to_rfc3339())
                .unwrap_or_else(|| "Never".to_string())
        )
    }
} 