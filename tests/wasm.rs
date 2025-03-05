use wasm_bindgen_test::*;
use lumascript::*;

wasm_bindgen_test_configure!(run_in_browser);

#[wasm_bindgen_test]
fn test_hello_world() {
    assert_eq!(hello_world(), "Hello from LumaScript WASM!");
}

#[wasm_bindgen_test]
fn test_runtime() {
    let runtime = LumaRuntime::new();
    assert_eq!(
        runtime.print("test"),
        "LumaScript: test"
    );
} 