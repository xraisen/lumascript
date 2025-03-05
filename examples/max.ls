// Function to return the maximum of two numbers
func max(a: i32, b: i32) -> i32 {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

// Function to check if a number is positive
func is_positive(x: i32) -> i32 {
    if (x > 0) {
        return 1;
    }
    return 0;
}

// Function to find the absolute value
func abs(x: i32) -> i32 {
    if (x < 0) {
        return 0 - x;
    }
    return x;
} 