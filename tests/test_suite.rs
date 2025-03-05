use wasm_bindgen_test::*;
use lumascript::*;

#[test]
fn test_hex_converter_basic() {
    let mut converter = LumaHexConverter::new();
    
    // Test simple conversion
    let input = "Hello";
    let hex = converter.text_to_hex(input);
    assert_eq!(hex, "48656c6c6f"); // "Hello" in hex
    
    // Test conversion back
    let text = converter.hex_to_text(&hex).unwrap();
    assert_eq!(text, "Hello");
}

#[test]
fn test_special_characters() {
    let mut converter = LumaHexConverter::new();
    
    // Test with special characters
    let input = "LumaScript🚀";
    let hex = converter.text_to_hex(input);
    let text = converter.hex_to_text(&hex).unwrap();
    assert_eq!(text, input);
}

#[test]
fn test_empty_input() {
    let mut converter = LumaHexConverter::new();
    
    // Test empty string
    let hex = converter.text_to_hex("");
    assert_eq!(hex, "");
    
    let text = converter.hex_to_text("").unwrap();
    assert_eq!(text, "");
} 