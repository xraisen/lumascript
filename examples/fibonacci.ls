// Calculate the nth Fibonacci number
func fibonacci(n: i32) -> i32 {
    let a: i32 = 0;
    let b: i32 = 1;
    let i: i32 = 0;
    
    while (i < n) {
        let temp: i32 = a + b;
        a = b;
        b = temp;
        i += 1;
    }
    
    return a;
}

// Sum numbers from 1 to n
func sum_to(n: i32) -> i32 {
    let sum: i32 = 0;
    let i: i32 = 1;
    
    while (i <= n) {
        sum += i;
        i += 1;
    }
    
    return sum;
} 