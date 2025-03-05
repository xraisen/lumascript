// Dynamic array implementation in LumaScript
// Demonstrates memory management, pointer operations, and resizing

func create_array() -> ptr<i32> {
    // Initial capacity of 4 elements
    let capacity: i32 = 4;
    let array: ptr<i32> = alloc(i32, capacity + 1);  // +1 for storing size
    @array = 0;  // Initial size is 0
    return array;
}

func get_size(array: ptr<i32>) -> i32 {
    return @array;  // First element stores the size
}

func get_capacity(array: ptr<i32>) -> i32 {
    // Capacity is stored implicitly by allocation size
    return sizeof(@(array + 1));
}

func push(array: ptr<i32>, value: i32) -> i32 {
    let size: i32 = get_size(array);
    let capacity: i32 = get_capacity(array);
    
    // Check if we need to resize
    if (size >= capacity) {
        // Double the capacity
        let new_capacity: i32 = capacity * 2;
        let new_array: ptr<i32> = alloc(i32, new_capacity + 1);
        
        // Copy existing elements
        let i: i32 = 0;
        while (i <= size) {
            @(new_array + i) = @(array + i);
            i += 1;
        }
        
        // Free old array
        free(array);
        array = new_array;
    }
    
    // Add new element
    @(array + size + 1) = value;
    @array = size + 1;  // Update size
    return size + 1;
}

func get(array: ptr<i32>, index: i32) -> i32 {
    let size: i32 = get_size(array);
    if (index < 0 || index >= size) {
        return -1;  // Error: Index out of bounds
    }
    return @(array + index + 1);  // +1 to skip size element
}

func set(array: ptr<i32>, index: i32, value: i32) -> i32 {
    let size: i32 = get_size(array);
    if (index < 0 || index >= size) {
        return 0;  // Error: Index out of bounds
    }
    @(array + index + 1) = value;  // +1 to skip size element
    return 1;  // Success
}

func delete_array(array: ptr<i32>) {
    free(array);
} 