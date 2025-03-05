use wasm_bindgen_test::*;
use lumascript::*;
use std::thread;
use std::time::Duration;

#[test]
fn stress_test_concurrent_operations() {
    let mut handles = vec![];
    
    // Spawn 100 threads
    for i in 0..100 {
        let handle = thread::spawn(move || {
            let mut converter = LumaHexConverter::new();
            let input = format!("LumaScript Stress Test {}", i);
            
            // Perform 1000 conversions per thread
            for _ in 0..1000 {
                let hex = converter.text_to_hex(&input);
                let text = converter.hex_to_text(&hex).unwrap();
                assert_eq!(text, input);
            }
        });
        handles.push(handle);
    }

    // Wait for all threads
    for handle in handles {
        handle.join().unwrap();
    }
}

#[test]
fn test_error_handling() {
    let mut converter = LumaHexConverter::new();
    
    // Test invalid hex input
    let result = converter.hex_to_text("invalid hex");
    assert!(result.is_err());
    
    // Test odd length hex
    let result = converter.hex_to_text("abc");
    assert!(result.is_err());
    
    // Test non-utf8 sequences
    let result = converter.hex_to_text("FF");
    assert!(result.is_err());
} 