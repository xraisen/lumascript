#[test]
func test_string_creation() {
    // Test empty string
    let empty = String::new();
    assert_eq(empty.length(), 0);
    assert_eq(empty.is_inline, 1);

    // Test small string (SSO)
    let small = String::from_literal("Hello", 5);
    assert_eq(small.length(), 5);
    assert_eq(small.is_inline, 1);
    assert_eq(small.charAt(0), 'H');
    assert_eq(small.charAt(4), 'o');

    // Test large string (heap allocation)
    let large = String::from_literal("This is a longer string that won't fit in SSO", 44);
    assert_eq(large.length(), 44);
    assert_eq(large.is_inline, 0);
    assert_eq(large.charAt(0), 'T');
    assert_eq(large.charAt(43), 'O');
}

#[test]
func test_string_operations() {
    let str = String::from_literal("Hello, World!", 13);
    
    // Test substring
    let sub = str.substring(0, 5);
    assert_eq(sub.length(), 5);
    assert_eq(sub.charAt(0), 'H');
    assert_eq(sub.charAt(4), 'o');

    // Test concatenation
    let other = String::from_literal(" Compiler", 9);
    let concat = str.concat(other);
    assert_eq(concat.length(), 22);
    assert_eq(concat.charAt(13), 'C');
}

#[test]
func test_string_builder() {
    let builder = StringBuilder::new();
    
    builder.append(String::from_literal("Hello", 5));
    builder.append(String::from_literal(", ", 2));
    builder.append(String::from_literal("World", 5));
    builder.append(String::from_literal("!", 1));
    
    let result = builder.toString();
    assert_eq(result.length(), 13);
    assert_eq(result.charAt(0), 'H');
    assert_eq(result.charAt(12), '!');
}

#[test]
func test_string_intermediate_operations() {
    // Test indexOf and lastIndexOf
    let str = String::from_literal("Hello World");
    assert(str.indexOf("World") == 6);
    assert(str.indexOf("o") == 4);
    assert(str.lastIndexOf("o") == 7);
    assert(str.indexOf("xyz") == -1);
    
    // Test contains, startsWith, endsWith
    assert(str.contains("World"));
    assert(!str.contains("xyz"));
    assert(str.startsWith("Hello"));
    assert(str.endsWith("World"));
    assert(!str.startsWith("World"));
    assert(!str.endsWith("Hello"));
    
    // Test case conversion
    let upper = str.toUpperCase();
    assert(upper == "HELLO WORLD");
    let lower = str.toLowerCase();
    assert(lower == "hello world");
    
    // Test trim
    let padded = String::from_literal("  Hello World  ");
    let trimmed = padded.trim();
    assert(trimmed == "Hello World");
    
    // Test split
    let parts = str.split(" ");
    assert(parts.length() == 2);
    assert(parts[0] == "Hello");
    assert(parts[1] == "World");
    
    // Test replace
    let replaced = str.replace("World", "LumaScript");
    assert(replaced == "Hello LumaScript");
    
    // Test repeat
    let repeated = String::from_literal("ha").repeat(3);
    assert(repeated == "hahaha");
    
    // Test padding
    let padded_left = str.padLeft('*', 15);
    assert(padded_left == "****Hello World");
    let padded_right = str.padRight('*', 15);
    assert(padded_right == "Hello World****");
    
    // Clean up
    str.free();
    upper.free();
    lower.free();
    padded.free();
    trimmed.free();
    replaced.free();
    repeated.free();
    padded_left.free();
    padded_right.free();
    
    // Clean up array
    for (let i = 0; i < parts.length(); i += 1) {
        parts[i].free();
    }
    parts.free();
}

#[test]
func test_string_edge_cases() {
    let str = String::from_literal("Test", 4);
    
    // Test out of bounds access
    #[should_panic]
    str.charAt(-1);
    
    #[should_panic]
    str.charAt(4);
    
    // Test invalid substring range
    #[should_panic]
    str.substring(-1, 3);
    
    #[should_panic]
    str.substring(2, 5);
    
    #[should_panic]
    str.substring(3, 2);

    // Test empty string operations
    let empty = String::new();
    assert(empty.indexOf("") == 0);
    assert(empty.lastIndexOf("") == 0);
    assert(empty.contains(""));
    assert(empty.startsWith(""));
    assert(empty.endsWith(""));
    assert(empty.trim() == "");
    assert(empty.split("").length() == 0);
    assert(empty.replace("", "") == "");
    assert(empty.repeat(0) == "");
    assert(empty.padLeft('*', 0) == "");
    assert(empty.padRight('*', 0) == "");
    
    // Test single character string
    let single = String::from_literal("a");
    assert(single.indexOf("a") == 0);
    assert(single.lastIndexOf("a") == 0);
    assert(single.contains("a"));
    assert(single.startsWith("a"));
    assert(single.endsWith("a"));
    assert(single.trim() == "a");
    assert(single.split("a").length() == 2);
    assert(single.replace("a", "b") == "b");
    assert(single.repeat(1) == "a");
    assert(single.padLeft('*', 1) == "a");
    assert(single.padRight('*', 1) == "a");
    
    // Clean up
    empty.free();
    single.free();
}

#[test]
func test_string_memory() {
    // Test memory management for heap-allocated strings
    let large = String::from_literal("This is a very long string that will definitely use heap allocation", 63);
    assert_eq(large.is_inline, 0);
    assert_ne(large.data, null);
    
    // Test cleanup
    large.free();
    
    // Test string builder memory management
    let builder = StringBuilder::new();
    for (let i = 0; i < 1000; i += 1) {
        builder.append(String::from_literal("Test", 4));
    }
    let result = builder.toString();
    assert_eq(result.length(), 4000);
    result.free();
}

func test_string_performance() {
    // Test large string operations
    let large = String::with_capacity(1000);
    for (let i = 0; i < 1000; i += 1) {
        large.append("a");
    }
    
    // Test operations on large string
    let start = get_time();
    let upper = large.toUpperCase();
    let mid = get_time();
    let lower = large.toLowerCase();
    let end = get_time();
    
    // Verify performance
    assert(mid - start < 1000); // Should take less than 1ms
    assert(end - mid < 1000);   // Should take less than 1ms
    
    // Clean up
    large.free();
    upper.free();
    lower.free();
}

#[test]
func test_string_comprehensive() {
    // Test 1: Basic String Operations with Different Sizes
    let empty = String::new();
    let small = String::from_literal("Hello", 5);
    let medium = String::from_literal("This is a medium string", 22);
    let large = String::from_literal("This is a very long string that will definitely use heap allocation and test various operations", 89);
    
    // Test 2: String Search Operations
    assert(empty.indexOf("") == 0);
    assert(small.indexOf("lo") == 3);
    assert(medium.indexOf("medium") == 8);
    assert(large.indexOf("heap") == 45);
    
    assert(empty.lastIndexOf("") == 0);
    assert(small.lastIndexOf("l") == 3);
    assert(medium.lastIndexOf(" ") == 17);
    assert(large.lastIndexOf(" ") == 82);
    
    // Test 3: String Predicates
    assert(empty.contains(""));
    assert(small.contains("el"));
    assert(medium.contains("medium"));
    assert(large.contains("heap"));
    
    assert(empty.startsWith(""));
    assert(small.startsWith("He"));
    assert(medium.startsWith("This"));
    assert(large.startsWith("This"));
    
    assert(empty.endsWith(""));
    assert(small.endsWith("lo"));
    assert(medium.endsWith("string"));
    assert(large.endsWith("operations"));
    
    // Test 4: String Transformations
    let upper_small = small.toUpperCase();
    let lower_small = small.toLowerCase();
    assert(upper_small == "HELLO");
    assert(lower_small == "hello");
    
    let padded_small = small.padLeft('*', 8);
    let padded_right = small.padRight('*', 8);
    assert(padded_small == "***Hello");
    assert(padded_right == "Hello***");
    
    // Test 5: String Manipulation
    let repeated = small.repeat(3);
    assert(repeated == "HelloHelloHello");
    
    let trimmed = String::from_literal("  Hello  ", 8).trim();
    assert(trimmed == "Hello");
    
    // Test 6: String Splitting
    let parts = medium.split(" ");
    assert(parts.length() == 5);
    assert(parts[0] == "This");
    assert(parts[1] == "is");
    assert(parts[2] == "a");
    assert(parts[3] == "medium");
    assert(parts[4] == "string");
    
    // Test 7: String Replacement
    let replaced = medium.replace("medium", "long");
    assert(replaced == "This is a long string");
    
    // Test 8: String Builder
    let builder = StringBuilder::new();
    builder.append(small);
    builder.append(String::from_literal(" ", 1));
    builder.append(medium);
    let built = builder.toString();
    assert(built == "Hello This is a medium string");
    
    // Test 9: Edge Cases
    let single_char = String::from_literal("a", 1);
    assert(single_char.repeat(0) == "");
    assert(single_char.repeat(1) == "a");
    assert(single_char.repeat(5) == "aaaaa");
    
    let whitespace = String::from_literal("   ", 3);
    assert(whitespace.trim() == "");
    
    // Test 10: Memory Management
    let large_repeated = large.repeat(2);
    assert(large_repeated.length() == 178);
    
    // Clean up
    empty.free();
    small.free();
    medium.free();
    large.free();
    upper_small.free();
    lower_small.free();
    padded_small.free();
    padded_right.free();
    repeated.free();
    trimmed.free();
    replaced.free();
    built.free();
    single_char.free();
    whitespace.free();
    large_repeated.free();
    
    // Clean up array
    for (let i = 0; i < parts.length(); i += 1) {
        parts[i].free();
    }
    parts.free();
}

#[test]
func test_string_performance_comprehensive() {
    // Test 1: Large String Creation
    let start = get_time();
    let large = String::with_capacity(10000);
    for (let i = 0; i < 10000; i += 1) {
        large.append("a");
    }
    let creation_time = get_time() - start;
    assert(creation_time < 1000); // Should take less than 1ms
    
    // Test 2: String Operations on Large String
    start = get_time();
    let upper = large.toUpperCase();
    let upper_time = get_time() - start;
    assert(upper_time < 1000);
    
    start = get_time();
    let lower = large.toLowerCase();
    let lower_time = get_time() - start;
    assert(lower_time < 1000);
    
    // Test 3: String Search Performance
    start = get_time();
    for (let i = 0; i < 100; i += 1) {
        large.indexOf("aaaaaaaa");
    }
    let search_time = get_time() - start;
    assert(search_time < 5000); // Should take less than 5ms
    
    // Test 4: String Builder Performance
    start = get_time();
    let builder = StringBuilder::new();
    for (let i = 0; i < 1000; i += 1) {
        builder.append(String::from_literal("Test", 4));
    }
    let result = builder.toString();
    let builder_time = get_time() - start;
    assert(builder_time < 1000);
    
    // Test 5: String Replacement Performance
    start = get_time();
    let replaced = large.replace("a", "b");
    let replace_time = get_time() - start;
    assert(replace_time < 1000);
    
    // Clean up
    large.free();
    upper.free();
    lower.free();
    result.free();
    replaced.free();
}

#[test]
func test_string_error_handling() {
    // Test 1: Invalid Indices
    let str = String::from_literal("Test", 4);
    
    #[should_panic]
    str.charAt(-1);
    
    #[should_panic]
    str.charAt(4);
    
    #[should_panic]
    str.charAt(5);
    
    // Test 2: Invalid Substring Ranges
    #[should_panic]
    str.substring(-1, 3);
    
    #[should_panic]
    str.substring(2, 5);
    
    #[should_panic]
    str.substring(3, 2);
    
    #[should_panic]
    str.substring(4, 4);
    
    // Test 3: Invalid Split Delimiters
    let empty_delim = String::new();
    #[should_panic]
    str.split(empty_delim);
    
    // Test 4: Invalid Replacements
    let empty_old = String::new();
    #[should_panic]
    str.replace(empty_old, "new");
    
    // Test 5: Invalid Padding
    #[should_panic]
    str.padLeft('*', -1);
    
    #[should_panic]
    str.padRight('*', -1);
    
    // Clean up
    str.free();
    empty_delim.free();
    empty_old.free();
}

#[test]
func test_string_unicode() {
    // Test 1: Unicode Characters
    let unicode = String::from_literal("Hello 世界", 11);
    assert(unicode.length() == 11);
    assert(unicode.charAt(6) == '世');
    assert(unicode.charAt(7) == '界');
    
    // Test 2: Unicode Operations
    let upper_unicode = unicode.toUpperCase();
    assert(upper_unicode == "HELLO 世界");
    
    let padded_unicode = unicode.padLeft('*', 15);
    assert(padded_unicode == "****Hello 世界");
    
    // Test 3: Unicode Splitting
    let parts = unicode.split(" ");
    assert(parts.length() == 2);
    assert(parts[0] == "Hello");
    assert(parts[1] == "世界");
    
    // Clean up
    unicode.free();
    upper_unicode.free();
    padded_unicode.free();
    
    for (let i = 0; i < parts.length(); i += 1) {
        parts[i].free();
    }
    parts.free();
} 