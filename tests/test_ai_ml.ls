// Test Tensor Operations
func test_tensor_operations() {
    // Test tensor creation
    let x = Tensor::new([2, 2], Device::CPU);
    assert(x.shape == [2, 2], "Tensor shape should be [2, 2]");
    assert(x.device == Device::CPU, "Tensor device should be CPU");
    
    // Test tensor operations
    let y = x.matmul(x);
    assert(y.shape == [2, 2], "Matrix multiplication shape should be [2, 2]");
    
    // Test GPU acceleration
    let z = Tensor::new([2, 2], Device::GPU);
    let w = z.matmul(z);
    assert(w.device == Device::GPU, "Result should be on GPU");
}

// Test Neural Networks
func test_neural_networks() {
    // Test model creation
    let model = create_model();
    assert(model.layers.length() == 2, "Model should have 2 layers");
    
    // Test forward pass
    let input = Tensor::new([1, 784], Device::CPU);
    let output = model.forward(input);
    assert(output.shape == [1, 10], "Output shape should be [1, 10]");
    
    // Test backward pass
    let gradient = Tensor::new([1, 10], Device::CPU);
    model.backward(gradient);
    // Verify gradients are computed
    for (let layer in model.layers) {
        assert(layer.weights.grad != null, "Layer weights should have gradients");
        assert(layer.bias.grad != null, "Layer bias should have gradients");
    }
}

// Test Data Science Features
func test_dataframe_operations() {
    // Test DataFrame creation
    let df = DataFrame::from_csv("test_data.csv");
    assert(df.columns.length() > 0, "DataFrame should have columns");
    
    // Test filtering
    let filtered = df.filter(|x| x["age"] > 30);
    assert(filtered.length() <= df.length(), "Filtered DataFrame should be smaller or equal");
    
    // Test groupby
    let grouped = df.groupby("city");
    assert(grouped.groups.length() > 0, "Grouped DataFrame should have groups");
    
    // Test SQL-like operations
    let result = sql<<SELECT * FROM df WHERE salary > 100000>>;
    assert(result.length() > 0, "SQL query should return results");
}

// Test Scientific Computing
func test_scientific_computing() {
    // Test complex numbers
    let z1 = Complex { real: 3.0, imag: 4.0 };
    let z2 = Complex { real: 1.0, imag: 2.0 };
    let sum = z1.add(z2);
    assert(sum.real == 4.0, "Complex addition real part should be 4.0");
    assert(sum.imag == 6.0, "Complex addition imaginary part should be 6.0");
    
    // Test quaternions
    let q1 = Quaternion { w: 1.0, x: 0.0, y: 0.0, z: 0.0 };
    let q2 = Quaternion { w: 0.0, x: 1.0, y: 0.0, z: 0.0 };
    let product = q1.multiply(q2);
    assert(product.w == 0.0, "Quaternion multiplication w should be 0.0");
    assert(product.x == 1.0, "Quaternion multiplication x should be 1.0");
    
    // Test physical units
    let speed = 5.0 * Unit::Meter / Unit::Second;
    let mass = 10.0 * Unit::Kilogram;
    let energy = 0.5 * mass * speed * speed;
    assert(energy.unit == Unit::Joule, "Energy should be in Joules");
}

// Test Web & Visualization
func test_web_visualization() {
    // Test web components
    let data = DataFrame::from_csv("dashboard_data.csv");
    let dashboard = Dashboard { data: data };
    let html = dashboard.render();
    assert(html.contains("<h1>"), "HTML should contain heading");
    assert(html.contains("<Plot"), "HTML should contain plot component");
    
    // Test 3D visualization
    let scene = Scene3D::new();
    let mesh = create_test_mesh();
    scene.add_mesh(mesh);
    let image = scene.render();
    assert(image.width > 0, "Rendered image should have width");
    assert(image.height > 0, "Rendered image should have height");
}

// Test Optimization Features
func test_optimization_features() {
    // Test JIT compilation
    let data = Tensor::new([1000, 1000], Device::CPU);
    let result = hot_loop(data);
    assert(result.shape == data.shape, "JIT result shape should match input");
    
    // Test distributed computing
    let sharded_data = ShardedTensor::new(4);  // 4 shards
    let model = train_model(sharded_data);
    assert(model.layers.length() > 0, "Trained model should have layers");
}

// Helper functions
func create_test_mesh() -> Mesh {
    // Create a simple test mesh
    let vertices = [
        Vec3 { x: 0.0, y: 0.0, z: 0.0 },
        Vec3 { x: 1.0, y: 0.0, z: 0.0 },
        Vec3 { x: 0.0, y: 1.0, z: 0.0 }
    ];
    let indices = [0, 1, 2];
    return Mesh::new(vertices, indices);
}

// Run all tests
func main() {
    test_tensor_operations();
    test_neural_networks();
    test_dataframe_operations();
    test_scientific_computing();
    test_web_visualization();
    test_optimization_features();
    println("All AI/ML and scientific computing tests passed!");
} 