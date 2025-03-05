// Tensor Operations
struct Tensor<T> {
    data: ptr<T>,
    shape: Array<i32>,
    device: Device,
    requires_grad: bool,
    grad: ptr<T>,
    ops: Array<Operation>
}

enum Device {
    CPU,
    GPU,
    TPU
}

struct Operation {
    type: OpType,
    inputs: Array<Tensor<T>>,
    output: Tensor<T>,
    backward: func(Array<Tensor<T>>, Tensor<T>)
}

enum OpType {
    MatMul,
    Add,
    ReLU,
    Sigmoid,
    Tanh
}

impl Tensor<T> {
    func new(shape: Array<i32>, device: Device) -> Tensor<T> {
        let size = 1;
        for (let dim in shape) {
            size *= dim;
        }
        
        let data = allocate_memory(size * sizeof(T));
        if (device == Device::GPU) {
            // Allocate GPU memory
            data = gpu_allocate(size * sizeof(T));
        }
        
        return Tensor {
            data: data,
            shape: shape,
            device: device,
            requires_grad: false,
            grad: null,
            ops: []
        };
    }
    
    func matmul(other: Tensor<T>) -> Tensor<T> {
        if (self.shape.length() != 2 || other.shape.length() != 2) {
            panic("MatMul requires 2D tensors");
        }
        
        if (self.shape[1] != other.shape[0]) {
            panic("Invalid dimensions for matrix multiplication");
        }
        
        let result = Tensor::new([self.shape[0], other.shape[1]], self.device);
        result.requires_grad = self.requires_grad || other.requires_grad;
        
        if (self.device == Device::GPU) {
            matmul_gpu(self, other, result);
        } else {
            matmul_cpu(self, other, result);
        }
        
        if (result.requires_grad) {
            result.ops.push(Operation {
                type: OpType::MatMul,
                inputs: [self, other],
                output: result,
                backward: matmul_backward
            });
        }
        
        return result;
    }
    
    func add(other: Tensor<T>) -> Tensor<T> {
        if (!shapes_match(self, other)) {
            panic("Shapes must match for addition");
        }
        
        let result = Tensor::new(self.shape, self.device);
        result.requires_grad = self.requires_grad || other.requires_grad;
        
        if (self.device == Device::GPU) {
            add_gpu(self, other, result);
        } else {
            add_cpu(self, other, result);
        }
        
        if (result.requires_grad) {
            result.ops.push(Operation {
                type: OpType::Add,
                inputs: [self, other],
                output: result,
                backward: add_backward
            });
        }
        
        return result;
    }
    
    func relu() -> Tensor<T> {
        let result = Tensor::new(self.shape, self.device);
        result.requires_grad = self.requires_grad;
        
        if (self.device == Device::GPU) {
            relu_gpu(self, result);
        } else {
            relu_cpu(self, result);
        }
        
        if (result.requires_grad) {
            result.ops.push(Operation {
                type: OpType::ReLU,
                inputs: [self],
                output: result,
                backward: relu_backward
            });
        }
        
        return result;
    }
    
    func backward(gradient: Tensor<T>) {
        if (!self.requires_grad) return;
        
        if (self.grad == null) {
            self.grad = allocate_memory(self.size() * sizeof(T));
            if (self.device == Device::GPU) {
                self.grad = gpu_allocate(self.size() * sizeof(T));
            }
        }
        
        // Copy gradient to self.grad
        if (self.device == Device::GPU) {
            gpu_copy(gradient.data, self.grad, self.size() * sizeof(T));
        } else {
            memcpy(gradient.data, self.grad, self.size() * sizeof(T));
        }
        
        // Backward pass through operations
        for (let op in self.ops.reverse()) {
            op.backward(op.inputs, self.grad);
        }
    }
    
    func free() {
        if (self.data != null) {
            if (self.device == Device::GPU) {
                gpu_free(self.data);
            } else {
                free_memory(self.data);
            }
        }
        if (self.grad != null) {
            if (self.device == Device::GPU) {
                gpu_free(self.grad);
            } else {
                free_memory(self.grad);
            }
        }
    }
}

// Neural Network Implementation
struct Layer {
    weights: Tensor<f32>,
    bias: Tensor<f32>,
    activation: Activation
}

enum Activation {
    ReLU,
    Sigmoid,
    Tanh
}

struct NeuralNetwork {
    layers: Array<Layer>
}

impl NeuralNetwork {
    func new() -> NeuralNetwork {
        return NeuralNetwork { layers: [] };
    }
    
    func add_layer(layer: Layer) {
        self.layers.push(layer);
    }
    
    func forward(input: Tensor<f32>) -> Tensor<f32> {
        let x = input;
        for (let layer in self.layers) {
            let z = x.matmul(layer.weights).add(layer.bias);
            match layer.activation {
                Activation::ReLU => x = z.relu(),
                Activation::Sigmoid => x = z.sigmoid(),
                Activation::Tanh => x = z.tanh()
            }
        }
        return x;
    }
    
    func backward(gradient: Tensor<f32>) {
        let grad = gradient;
        for (let layer in self.layers.reverse()) {
            // Compute gradients for weights and bias
            let input = layer.input;
            let weight_grad = input.transpose().matmul(grad);
            let bias_grad = grad.sum(0);
            
            // Update weights and bias
            layer.weights = layer.weights.add(weight_grad.scale(-learning_rate));
            layer.bias = layer.bias.add(bias_grad.scale(-learning_rate));
            
            // Compute gradient for next layer
            grad = grad.matmul(layer.weights.transpose());
        }
    }
    
    func free() {
        for (let layer in self.layers) {
            layer.weights.free();
            layer.bias.free();
        }
    }
}

// Data Science Features
struct DataFrame {
    columns: HashMap<String, Array<Any>>,
    index: Array<i32>
}

impl DataFrame {
    func from_csv(path: String) -> DataFrame {
        let file = open_file(path, "r");
        let header = file.readline().split(",");
        let columns = HashMap::new();
        
        for (let col in header) {
            columns[col] = [];
        }
        
        while (!file.eof()) {
            let line = file.readline().split(",");
            for (let i = 0; i < header.length(); i += 1) {
                columns[header[i]].push(parse_value(line[i]));
            }
        }
        
        file.close();
        return DataFrame {
            columns: columns,
            index: range(0, columns[header[0]].length())
        };
    }
    
    func filter(predicate: func(Any) -> bool) -> DataFrame {
        let mask = [];
        for (let i = 0; i < self.index.length(); i += 1) {
            mask.push(predicate(self.get_row(i)));
        }
        
        let new_columns = HashMap::new();
        for (let col in self.columns) {
            new_columns[col] = [];
            for (let i = 0; i < mask.length(); i += 1) {
                if (mask[i]) {
                    new_columns[col].push(self.columns[col][i]);
                }
            }
        }
        
        return DataFrame {
            columns: new_columns,
            index: self.index.filter(|i| mask[i])
        };
    }
    
    func groupby(column: String) -> GroupBy {
        let groups = HashMap::new();
        for (let i = 0; i < self.index.length(); i += 1) {
            let key = self.columns[column][i];
            if (!groups.contains(key)) {
                groups[key] = [];
            }
            groups[key].push(i);
        }
        
        return GroupBy {
            groups: groups,
            df: self
        };
    }
    
    func plot() -> Plot {
        return Plot::new(self);
    }
}

// Scientific Computing
struct Complex {
    real: f64,
    imag: f64
}

impl Complex {
    func add(other: Complex) -> Complex {
        return Complex {
            real: self.real + other.real,
            imag: self.imag + other.imag
        };
    }
    
    func multiply(other: Complex) -> Complex {
        return Complex {
            real: self.real * other.real - self.imag * other.imag,
            imag: self.real * other.imag + self.imag * other.real
        };
    }
    
    func conjugate() -> Complex {
        return Complex {
            real: self.real,
            imag: -self.imag
        };
    }
    
    func magnitude() -> f64 {
        return sqrt(self.real * self.real + self.imag * self.imag);
    }
}

struct Quaternion {
    w: f64,
    x: f64,
    y: f64,
    z: f64
}

impl Quaternion {
    func multiply(other: Quaternion) -> Quaternion {
        return Quaternion {
            w: self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
            x: self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            y: self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            z: self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
        };
    }
}

struct Quantity<T> {
    value: T,
    unit: Unit
}

enum Unit {
    Meter,
    Second,
    Kilogram,
    Newton,
    Joule
}

impl Quantity<T> {
    func operator*(other: Quantity<T>) -> Quantity<T> {
        return Quantity {
            value: self.value * other.value,
            unit: self.unit * other.unit
        };
    }
    
    func operator/(other: Quantity<T>) -> Quantity<T> {
        return Quantity {
            value: self.value / other.value,
            unit: self.unit / other.unit
        };
    }
}

// Web & Visualization
@web
struct Dashboard {
    data: DataFrame
}

impl Dashboard {
    func render() -> HTML {
        return html! {
            <div class="dashboard">
                <h1>{ self.data.title }</h1>
                <Plot data=self.data />
            </div>
        };
    }
}

struct Scene3D {
    meshes: Array<Mesh>,
    camera: Camera,
    lights: Array<Light>
}

impl Scene3D {
    func new() -> Scene3D {
        return Scene3D {
            meshes: [],
            camera: Camera::new(),
            lights: []
        };
    }
    
    func add_mesh(mesh: Mesh) -> Scene3D {
        self.meshes.push(mesh);
        return self;
    }
    
    func render() -> Image {
        let renderer = Renderer::new();
        renderer.set_camera(self.camera);
        renderer.set_lights(self.lights);
        
        for (let mesh in self.meshes) {
            renderer.render_mesh(mesh);
        }
        
        return renderer.get_image();
    }
}

// Optimization Features
@jit
func hot_loop(data: Tensor<f32>) -> Tensor<f32> {
    let result = Tensor::new(data.shape, data.device);
    for (let i = 0; i < data.size; i += 1) {
        result[i] = data[i] * data[i];
    }
    return result;
}

@distributed
func train_model(data: ShardedTensor) -> Model {
    let model = create_model();
    for (let epoch = 0; epoch < 100; epoch += 1) {
        model.train(data);
        model.sync();
    }
    return model;
} 