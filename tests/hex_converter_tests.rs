#[cfg(test)]
mod tests {
    use super::*;
    use wasm_bindgen_test::*;

    #[wasm_bindgen_test]
    fn test_conversion() {
        let mut converter = LumaHexConverter::new();
        
        let original = "LumaScript";
        let hex = converter.text_to_hex(original);
        let decoded = converter.hex_to_text(&hex).unwrap();
        
        assert_eq!(original, decoded);
        assert!(converter.get_stats().contains("Operations: 2"));
    }
} 