// Bitwise Operations
func bit_and(a: i32, b: i32) -> i32 {
    return a & b;
}

func bit_or(a: i32, b: i32) -> i32 {
    return a | b;
}

func bit_xor(a: i32, b: i32) -> i32 {
    return a ^ b;
}

func bit_not(a: i32) -> i32 {
    return ~a;
}

func bit_shift_left(a: i32, shift: i32) -> i32 {
    if (shift < 0 || shift >= 32) {
        panic("Invalid shift amount");
    }
    return a << shift;
}

func bit_shift_right(a: i32, shift: i32) -> i32 {
    if (shift < 0 || shift >= 32) {
        panic("Invalid shift amount");
    }
    return a >> shift;
}

// Bit manipulation utilities
func set_bit(value: i32, position: i32) -> i32 {
    if (position < 0 || position >= 32) {
        panic("Invalid bit position");
    }
    return value | (1 << position);
}

func clear_bit(value: i32, position: i32) -> i32 {
    if (position < 0 || position >= 32) {
        panic("Invalid bit position");
    }
    return value & ~(1 << position);
}

func toggle_bit(value: i32, position: i32) -> i32 {
    if (position < 0 || position >= 32) {
        panic("Invalid bit position");
    }
    return value ^ (1 << position);
}

func get_bit(value: i32, position: i32) -> bool {
    if (position < 0 || position >= 32) {
        panic("Invalid bit position");
    }
    return (value & (1 << position)) != 0;
}

// SIMD Operations
struct Vec4 {
    x: f32,
    y: f32,
    z: f32,
    w: f32
}

struct Vec8 {
    data: f32[8]
}

func vec4_add(a: Vec4, b: Vec4) -> Vec4 {
    return Vec4 {
        x: a.x + b.x,
        y: a.y + b.y,
        z: a.z + b.z,
        w: a.w + b.w
    };
}

func vec4_mul(a: Vec4, b: Vec4) -> Vec4 {
    return Vec4 {
        x: a.x * b.x,
        y: a.y * b.y,
        z: a.z * b.z,
        w: a.w * b.w
    };
}

func vec4_dot(a: Vec4, b: Vec4) -> f32 {
    return a.x * b.x + a.y * b.y + a.z * b.z + a.w * b.w;
}

func vec8_add(a: Vec8, b: Vec8) -> Vec8 {
    let result = Vec8 { data: [0.0; 8] };
    for (let i = 0; i < 8; i += 1) {
        result.data[i] = a.data[i] + b.data[i];
    }
    return result;
}

func vec8_mul(a: Vec8, b: Vec8) -> Vec8 {
    let result = Vec8 { data: [0.0; 8] };
    for (let i = 0; i < 8; i += 1) {
        result.data[i] = a.data[i] * b.data[i];
    }
    return result;
}

// SIMD intrinsics
func simd_load_aligned(ptr: ptr<f32>) -> Vec4 {
    // In a real implementation, this would use platform-specific SIMD instructions
    return Vec4 {
        x: @ptr,
        y: @(ptr + 1),
        z: @(ptr + 2),
        w: @(ptr + 3)
    };
}

func simd_store_aligned(ptr: ptr<f32>, vec: Vec4) {
    // In a real implementation, this would use platform-specific SIMD instructions
    @ptr = vec.x;
    @(ptr + 1) = vec.y;
    @(ptr + 2) = vec.z;
    @(ptr + 3) = vec.w;
}

// Matrix Operations with Operator Overloading
struct Matrix {
    data: ptr<f64>,
    rows: i32,
    cols: i32
}

impl Matrix {
    func new(rows: i32, cols: i32, data: Array<f64>) -> Matrix {
        let size = rows * cols;
        if (data.length() != size) {
            panic("Invalid matrix dimensions");
        }
        
        let ptr = allocate_memory(size * 8);  // 8 bytes per f64
        for (let i = 0; i < size; i += 1) {
            @(ptr + i) = data[i];
        }
        
        return Matrix { data: ptr, rows: rows, cols: cols };
    }
    
    func operator+(self, other: Matrix) -> Matrix {
        if (self.rows != other.rows || self.cols != other.cols) {
            panic("Matrix dimensions must match");
        }
        
        let size = self.rows * self.cols;
        let result = Matrix::new(self.rows, self.cols, [0.0; size]);
        
        for (let i = 0; i < size; i += 1) {
            @(result.data + i) = @(self.data + i) + @(other.data + i);
        }
        
        return result;
    }
    
    func operator*(self, other: Matrix) -> Matrix {
        if (self.cols != other.rows) {
            panic("Invalid matrix dimensions for multiplication");
        }
        
        let result = Matrix::new(self.rows, other.cols, [0.0; self.rows * other.cols]);
        
        for (let i = 0; i < self.rows; i += 1) {
            for (let j = 0; j < other.cols; j += 1) {
                let sum = 0.0;
                for (let k = 0; k < self.cols; k += 1) {
                    sum += @(self.data + i * self.cols + k) * 
                           @(other.data + k * other.cols + j);
                }
                @(result.data + i * result.cols + j) = sum;
            }
        }
        
        return result;
    }
    
    func operator*(self, scalar: f64) -> Matrix {
        let size = self.rows * self.cols;
        let result = Matrix::new(self.rows, self.cols, [0.0; size]);
        
        for (let i = 0; i < size; i += 1) {
            @(result.data + i) = @(self.data + i) * scalar;
        }
        
        return result;
    }
    
    func determinant(self) -> f64 {
        if (self.rows != self.cols) {
            panic("Matrix must be square");
        }
        
        if (self.rows == 1) {
            return @self.data;
        }
        
        if (self.rows == 2) {
            return @self.data * @(self.data + 3) - 
                   @(self.data + 1) * @(self.data + 2);
        }
        
        // For larger matrices, use Laplace expansion
        let det = 0.0;
        for (let j = 0; j < self.cols; j += 1) {
            let cofactor = self.cofactor(0, j);
            det += @(self.data + j) * cofactor;
        }
        return det;
    }
    
    func cofactor(self, row: i32, col: i32) -> f64 {
        let minor = self.minor(row, col);
        let cofactor = minor.determinant();
        if ((row + col) % 2 == 1) {
            cofactor = -cofactor;
        }
        return cofactor;
    }
    
    func minor(self, row: i32, col: i32) -> Matrix {
        let size = (self.rows - 1) * (self.cols - 1);
        let data = [0.0; size];
        let idx = 0;
        
        for (let i = 0; i < self.rows; i += 1) {
            if (i == row) continue;
            for (let j = 0; j < self.cols; j += 1) {
                if (j == col) continue;
                data[idx] = @(self.data + i * self.cols + j);
                idx += 1;
            }
        }
        
        return Matrix::new(self.rows - 1, self.cols - 1, data);
    }
    
    func transpose(self) -> Matrix {
        let result = Matrix::new(self.cols, self.rows, [0.0; self.rows * self.cols]);
        
        for (let i = 0; i < self.rows; i += 1) {
            for (let j = 0; j < self.cols; j += 1) {
                @(result.data + j * result.cols + i) = @(self.data + i * self.cols + j);
            }
        }
        
        return result;
    }
    
    func free(self) {
        free_memory(self.data);
    }
}

// Advanced Numeric Types
struct BigInt {
    digits: ptr<i32>,
    length: i32,
    sign: i32
}

impl BigInt {
    func from_string(s: String) -> BigInt {
        let len = s.length();
        let digits = allocate_memory(len * 4);  // 4 bytes per digit
        let sign = 1;
        
        if (s[0] == '-') {
            sign = -1;
            s = s.substring(1);
        }
        
        for (let i = 0; i < len; i += 1) {
            @(digits + i) = s[i] - '0';
        }
        
        return BigInt { digits: digits, length: len, sign: sign };
    }
    
    func add(self, other: BigInt) -> BigInt {
        // Implementation of big integer addition
        // This is a simplified version - real implementation would handle carries
        let max_len = max(self.length, other.length);
        let result = allocate_memory(max_len * 4);
        
        for (let i = 0; i < max_len; i += 1) {
            let sum = 0;
            if (i < self.length) sum += @(self.digits + i);
            if (i < other.length) sum += @(other.digits + i);
            @(result + i) = sum;
        }
        
        return BigInt { 
            digits: result, 
            length: max_len, 
            sign: self.sign 
        };
    }
    
    func to_string(self) -> String {
        let s = String::with_capacity(self.length + 1);
        if (self.sign < 0) s.push('-');
        for (let i = 0; i < self.length; i += 1) {
            s.push(@(self.digits + i) + '0');
        }
        return s;
    }
    
    func free(self) {
        free_memory(self.digits);
    }
}

struct Complex {
    real: f64,
    imag: f64
}

impl Complex {
    func add(self, other: Complex) -> Complex {
        return Complex {
            real: self.real + other.real,
            imag: self.imag + other.imag
        };
    }
    
    func multiply(self, other: Complex) -> Complex {
        return Complex {
            real: self.real * other.real - self.imag * other.imag,
            imag: self.real * other.imag + self.imag * other.real
        };
    }
    
    func conjugate(self) -> Complex {
        return Complex {
            real: self.real,
            imag: -self.imag
        };
    }
    
    func magnitude(self) -> f64 {
        return sqrt(self.real * self.real + self.imag * self.imag);
    }
}

struct Decimal {
    value: i64,
    scale: i32
}

impl Decimal {
    func from_string(s: String, scale: i32) -> Decimal {
        let parts = s.split('.');
        let whole = parts[0];
        let fraction = parts.length() > 1 ? parts[1] : "";
        
        let value = 0;
        for (let i = 0; i < whole.length(); i += 1) {
            value = value * 10 + (whole[i] - '0');
        }
        
        for (let i = 0; i < fraction.length(); i += 1) {
            value = value * 10 + (fraction[i] - '0');
        }
        
        return Decimal { value: value, scale: scale };
    }
    
    func add(self, other: Decimal) -> Decimal {
        let scale = max(self.scale, other.scale);
        let scaled_a = self.value * power(10, scale - self.scale);
        let scaled_b = other.value * power(10, scale - other.scale);
        
        return Decimal {
            value: scaled_a + scaled_b,
            scale: scale
        };
    }
    
    func to_string(self, places: i32) -> String {
        let s = String::new();
        let value = self.value;
        let scale = self.scale;
        
        if (value < 0) {
            s.push('-');
            value = -value;
        }
        
        let whole = value / power(10, scale);
        let fraction = value % power(10, scale);
        
        s.push_str(whole.to_string());
        if (places > 0) {
            s.push('.');
            let frac_str = fraction.to_string();
            for (let i = 0; i < places - frac_str.length(); i += 1) {
                s.push('0');
            }
            s.push_str(frac_str);
        }
        
        return s;
    }
}

// SIMD Optimization
#[simd]
func vector_add(a: ptr<f32>, b: ptr<f32>, result: ptr<f32>, length: i32) {
    for (let i = 0; i < length; i += 4) {
        let vec_a = simd_load_aligned(a + i);
        let vec_b = simd_load_aligned(b + i);
        let vec_result = vec_a + vec_b;
        simd_store_aligned(result + i, vec_result);
    }
} 