// String operations example in LumaScript

func greet(name: string) -> string {
    let greeting: string = "Hello, ";
    return concat(greeting, name);
}

func extract_word(text: string, start: i32, word_length: i32) -> string {
    return substr(text, start, word_length);
}

func count_chars(text: string) -> i32 {
    return len(text);
}

func main() -> i32 {
    let name: string = "Alice";
    let message: string = greet(name);
    let length: i32 = count_chars(message);
    
    // Extract "Hello" from the message
    let hello: string = extract_word(message, 0, 5);
    
    // Create a longer message
    let exclamation: string = "!!!";
    let full_message: string = concat(message, exclamation);
    
    return length;  // Returns the length of "Hello, Alice"
} 