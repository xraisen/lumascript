const { hello_world, LumaRuntime } = require('lumascript');

// Test the WASM functions
console.log(hello_world());

const runtime = new LumaRuntime();
console.log(runtime.print("Node.js test")); 