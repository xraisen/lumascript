// LumaScript String Implementation

/// String structure with small string optimization (SSO)
struct String {
    // Union of inline storage and heap storage
    union {
        struct {
            data: ptr<i8>,      // Pointer to heap data
            length: i32,        // String length
            capacity: i32       // Allocated capacity
        },
        struct {
            inline_data: [24]i8,  // Inline storage for small strings
            is_inline: i8         // Flag for SSO
        }
    }
}

/// Core string functions
impl String {
    /// Create new empty string
    func new() -> String {
        let str: String;
        str.is_inline = 1;
        str.inline_data[0] = 0;
        return str;
    }

    /// Create string from literal
    func from_literal(lit: ptr<i8>, len: i32) -> String {
        if (len <= 23) {
            // Use SSO for small strings
            let str: String;
            str.is_inline = 1;
            memcpy(str.inline_data, lit, len);
            str.inline_data[len] = 0;
            return str;
        } else {
            // Allocate heap storage
            let str: String;
            str.is_inline = 0;
            str.length = len;
            str.capacity = len + 1;
            str.data = alloc(i8, str.capacity);
            memcpy(str.data, lit, len);
            @(str.data + len) = 0;
            return str;
        }
    }

    /// Get string length
    func length(self) -> i32 {
        if (self.is_inline) {
            return strlen(self.inline_data);
        }
        return self.length;
    }

    /// Get character at index
    func charAt(self, index: i32) -> i8 {
        if (index < 0 || index >= self.length()) {
            throw "Index out of bounds";
        }
        if (self.is_inline) {
            return self.inline_data[index];
        }
        return @(self.data + index);
    }

    /// Get substring
    func substring(self, start: i32, end: i32) -> String {
        let len = self.length();
        if (start < 0 || end > len || start > end) {
            throw "Invalid substring range";
        }
        let substr_len = end - start;
        if (self.is_inline) {
            return String::from_literal(self.inline_data + start, substr_len);
        }
        return String::from_literal(self.data + start, substr_len);
    }

    /// Concatenate with another string
    func concat(self, other: String) -> String {
        let len1 = self.length();
        let len2 = other.length();
        let new_len = len1 + len2;
        
        let result = String::with_capacity(new_len);
        
        // Copy first string
        if (self.is_inline) {
            memcpy(result.data, self.inline_data, len1);
        } else {
            memcpy(result.data, self.data, len1);
        }
        
        // Copy second string
        if (other.is_inline) {
            memcpy(result.data + len1, other.inline_data, len2);
        } else {
            memcpy(result.data + len1, other.data, len2);
        }
        
        @(result.data + new_len) = 0;
        result.length = new_len;
        return result;
    }

    /// Create string with given capacity
    func with_capacity(capacity: i32) -> String {
        if (capacity <= 23) {
            return String::new();
        }
        let str: String;
        str.is_inline = 0;
        str.length = 0;
        str.capacity = capacity + 1;  // +1 for null terminator
        str.data = alloc(i8, str.capacity);
        @(str.data) = 0;
        return str;
    }

    /// Free string resources
    func free(self) {
        if (!self.is_inline && self.data != null) {
            free(self.data);
        }
    }

    /// Find first occurrence of substring
    func indexOf(self, substr: String) -> i32 {
        let len = self.length();
        let sublen = substr.length();
        
        if (sublen > len) return -1;
        if (sublen == 0) return 0;
        
        for (let i = 0; i <= len - sublen; i += 1) {
            let found = true;
            for (let j = 0; j < sublen; j += 1) {
                if (self.charAt(i + j) != substr.charAt(j)) {
                    found = false;
                    break;
                }
            }
            if (found) return i;
        }
        return -1;
    }

    /// Find last occurrence of substring
    func lastIndexOf(self, substr: String) -> i32 {
        let len = self.length();
        let sublen = substr.length();
        
        if (sublen > len) return -1;
        if (sublen == 0) return len;
        
        for (let i = len - sublen; i >= 0; i -= 1) {
            let found = true;
            for (let j = 0; j < sublen; j += 1) {
                if (self.charAt(i + j) != substr.charAt(j)) {
                    found = false;
                    break;
                }
            }
            if (found) return i;
        }
        return -1;
    }

    /// Check if string contains substring
    func contains(self, substr: String) -> bool {
        return self.indexOf(substr) >= 0;
    }

    /// Check if string starts with prefix
    func startsWith(self, prefix: String) -> bool {
        let len = prefix.length();
        if (len > self.length()) return false;
        
        for (let i = 0; i < len; i += 1) {
            if (self.charAt(i) != prefix.charAt(i)) {
                return false;
            }
        }
        return true;
    }

    /// Check if string ends with suffix
    func endsWith(self, suffix: String) -> bool {
        let len = suffix.length();
        let str_len = self.length();
        if (len > str_len) return false;
        
        for (let i = 0; i < len; i += 1) {
            if (self.charAt(str_len - len + i) != suffix.charAt(i)) {
                return false;
            }
        }
        return true;
    }

    /// Convert string to uppercase
    func toUpperCase(self) -> String {
        let len = self.length();
        let result = String::with_capacity(len);
        
        for (let i = 0; i < len; i += 1) {
            let c = self.charAt(i);
            if (c >= 'a' && c <= 'z') {
                @(result.data + i) = c - 32;
            } else {
                @(result.data + i) = c;
            }
        }
        
        result.length = len;
        @(result.data + len) = 0;
        return result;
    }

    /// Convert string to lowercase
    func toLowerCase(self) -> String {
        let len = self.length();
        let result = String::with_capacity(len);
        
        for (let i = 0; i < len; i += 1) {
            let c = self.charAt(i);
            if (c >= 'A' && c <= 'Z') {
                @(result.data + i) = c + 32;
            } else {
                @(result.data + i) = c;
            }
        }
        
        result.length = len;
        @(result.data + len) = 0;
        return result;
    }

    /// Remove whitespace from both ends
    func trim(self) -> String {
        let len = self.length();
        let start = 0;
        let end = len - 1;
        
        // Find first non-whitespace
        while (start < len && (self.charAt(start) == ' ' || 
                              self.charAt(start) == '\t' || 
                              self.charAt(start) == '\n' || 
                              self.charAt(start) == '\r')) {
            start += 1;
        }
        
        // Find last non-whitespace
        while (end >= start && (self.charAt(end) == ' ' || 
                               self.charAt(end) == '\t' || 
                               self.charAt(end) == '\n' || 
                               self.charAt(end) == '\r')) {
            end -= 1;
        }
        
        if (end < start) {
            return String::new();
        }
        
        return self.substring(start, end + 1);
    }

    /// Split string by delimiter
    func split(self, delimiter: String) -> Array<String> {
        let result = Array<String>::new();
        let start = 0;
        let len = self.length();
        let delim_len = delimiter.length();
        
        while (start < len) {
            let pos = self.indexOf(delimiter);
            if (pos == -1) {
                result.push(self.substring(start, len));
                break;
            }
            
            result.push(self.substring(start, pos));
            start = pos + delim_len;
        }
        
        return result;
    }

    /// Replace occurrences of old with new
    func replace(self, old: String, new: String) -> String {
        let builder = StringBuilder::new();
        let start = 0;
        let len = self.length();
        let old_len = old.length();
        
        while (start < len) {
            let pos = self.indexOf(old);
            if (pos == -1) {
                builder.append(self.substring(start, len));
                break;
            }
            
            builder.append(self.substring(start, pos));
            builder.append(new);
            start = pos + old_len;
        }
        
        return builder.toString();
    }

    /// Repeat string n times
    func repeat(self, count: i32) -> String {
        if (count <= 0) return String::new();
        
        let len = self.length();
        let total_len = len * count;
        let result = String::with_capacity(total_len);
        
        for (let i = 0; i < count; i += 1) {
            if (self.is_inline) {
                memcpy(result.data + (i * len), self.inline_data, len);
            } else {
                memcpy(result.data + (i * len), self.data, len);
            }
        }
        
        result.length = total_len;
        @(result.data + total_len) = 0;
        return result;
    }

    /// Pad string on the left
    func padLeft(self, padChar: i8, length: i32) -> String {
        let current_len = self.length();
        if (current_len >= length) return self;
        
        let result = String::with_capacity(length);
        let pad_len = length - current_len;
        
        // Fill padding
        for (let i = 0; i < pad_len; i += 1) {
            @(result.data + i) = padChar;
        }
        
        // Copy original string
        if (self.is_inline) {
            memcpy(result.data + pad_len, self.inline_data, current_len);
        } else {
            memcpy(result.data + pad_len, self.data, current_len);
        }
        
        result.length = length;
        @(result.data + length) = 0;
        return result;
    }

    /// Pad string on the right
    func padRight(self, padChar: i8, length: i32) -> String {
        let current_len = self.length();
        if (current_len >= length) return self;
        
        let result = String::with_capacity(length);
        
        // Copy original string
        if (self.is_inline) {
            memcpy(result.data, self.inline_data, current_len);
        } else {
            memcpy(result.data, self.data, current_len);
        }
        
        // Fill padding
        for (let i = current_len; i < length; i += 1) {
            @(result.data + i) = padChar;
        }
        
        result.length = length;
        @(result.data + length) = 0;
        return result;
    }
}

/// String builder for efficient concatenation
struct StringBuilder {
    chunks: Array<String>,
    total_length: i32
}

impl StringBuilder {
    /// Create new string builder
    func new() -> StringBuilder {
        let builder: StringBuilder;
        builder.chunks = Array::new();
        builder.total_length = 0;
        return builder;
    }

    /// Append string to builder
    func append(self, str: String) {
        self.chunks.push(str);
        self.total_length += str.length();
    }

    /// Build final string
    func toString(self) -> String {
        let result = String::with_capacity(self.total_length);
        let offset = 0;
        
        for (let i = 0; i < self.chunks.length(); i += 1) {
            let chunk = self.chunks[i];
            let len = chunk.length();
            
            if (chunk.is_inline) {
                memcpy(result.data + offset, chunk.inline_data, len);
            } else {
                memcpy(result.data + offset, chunk.data, len);
            }
            
            offset += len;
        }
        
        @(result.data + self.total_length) = 0;
        result.length = self.total_length;
        return result;
    }
} 