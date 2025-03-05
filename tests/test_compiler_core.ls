#[test]
func test_lexer() {
    // Test number recognition
    let source = "123 0xFF 0b1010 3.14 1.23e-4";
    let tokens = lex(source);
    
    assert(tokens[0].type == TOKEN_INTEGER && tokens[0].value == 123);
    assert(tokens[1].type == TOKEN_INTEGER && tokens[1].value == 0xFF);
    assert(tokens[2].type == TOKEN_INTEGER && tokens[2].value == 0b1010);
    assert(tokens[3].type == TOKEN_FLOAT && tokens[3].value == 3.14);
    assert(tokens[4].type == TOKEN_FLOAT && tokens[4].value == 1.23e-4);
    
    // Test string recognition
    source = "\"hello\\nworld\"";
    tokens = lex(source);
    assert(tokens[0].type == TOKEN_STRING);
    assert(tokens[0].value == "hello\nworld");
    
    // Test operators
    source = "+ - * / % ** == != < > <= >=";
    tokens = lex(source);
    assert(tokens[0].type == TOKEN_PLUS);
    assert(tokens[1].type == TOKEN_MINUS);
    assert(tokens[2].type == TOKEN_MULTIPLY);
    assert(tokens[3].type == TOKEN_DIVIDE);
    assert(tokens[4].type == TOKEN_MODULO);
    assert(tokens[5].type == TOKEN_POWER);
    assert(tokens[6].type == TOKEN_EQ);
    assert(tokens[7].type == TOKEN_NE);
    assert(tokens[8].type == TOKEN_LT);
    assert(tokens[9].type == TOKEN_GT);
    assert(tokens[10].type == TOKEN_LE);
    assert(tokens[11].type == TOKEN_GE);
    
    // Test bitwise operators
    source = "& | ^ ~ << >>";
    tokens = lex(source);
    assert(tokens[0].type == TOKEN_BIT_AND);
    assert(tokens[1].type == TOKEN_BIT_OR);
    assert(tokens[2].type == TOKEN_BIT_XOR);
    assert(tokens[3].type == TOKEN_BIT_NOT);
    assert(tokens[4].type == TOKEN_SHIFT_LEFT);
    assert(tokens[5].type == TOKEN_SHIFT_RIGHT);
    
    // Test keywords
    source = "func return if else while for break continue true false null";
    tokens = lex(source);
    assert(tokens[0].type == TOKEN_FUNCTION);
    assert(tokens[1].type == TOKEN_RETURN);
    assert(tokens[2].type == TOKEN_IF);
    assert(tokens[3].type == TOKEN_ELSE);
    assert(tokens[4].type == TOKEN_WHILE);
    assert(tokens[5].type == TOKEN_FOR);
    assert(tokens[6].type == TOKEN_BREAK);
    assert(tokens[7].type == TOKEN_CONTINUE);
    assert(tokens[8].type == TOKEN_TRUE);
    assert(tokens[9].type == TOKEN_FALSE);
    assert(tokens[10].type == TOKEN_NULL);
}

#[test]
func test_parser() {
    // Test expression parsing
    let source = "1 + 2 * 3";
    let ast = parse(source);
    assert(ast.type == NODE_BINARY_OP);
    assert(ast.op == TOKEN_PLUS);
    assert(ast.left.type == NODE_INTEGER_LITERAL && ast.left.value == 1);
    assert(ast.right.type == NODE_BINARY_OP);
    assert(ast.right.op == TOKEN_MULTIPLY);
    assert(ast.right.left.type == NODE_INTEGER_LITERAL && ast.right.left.value == 2);
    assert(ast.right.right.type == NODE_INTEGER_LITERAL && ast.right.right.value == 3);
    
    // Test function parsing
    source = "func add(a: i32, b: i32) -> i32 { return a + b; }";
    ast = parse(source);
    assert(ast.type == NODE_FUNCTION);
    assert(ast.name == "add");
    assert(ast.params.length() == 2);
    assert(ast.return_type == TYPE_INT);
    assert(ast.body.type == NODE_BLOCK);
    assert(ast.body.statements.length() == 1);
    
    // Test control flow parsing
    source = "if (x > 0) { return x; } else { return -x; }";
    ast = parse(source);
    assert(ast.type == NODE_IF);
    assert(ast.condition.type == NODE_BINARY_OP);
    assert(ast.condition.op == TOKEN_GT);
    assert(ast.then_branch.type == NODE_BLOCK);
    assert(ast.else_branch.type == NODE_BLOCK);
}

#[test]
func test_type_checking() {
    // Test basic type checking
    let source = "let x: i32 = 42;";
    let ast = parse(source);
    let type_info = check_types(ast);
    assert(type_info.base_type == TYPE_INT);
    
    // Test type compatibility
    source = "let x: f64 = 42;";  // Implicit conversion from int to float
    ast = parse(source);
    type_info = check_types(ast);
    assert(type_info.base_type == TYPE_FLOAT);
    
    // Test type error
    source = "let x: i32 = \"hello\";";
    ast = parse(source);
    #[should_panic]
    check_types(ast);
    
    // Test function type checking
    source = "func add(a: i32, b: i32) -> i32 { return a + b; }";
    ast = parse(source);
    type_info = check_types(ast);
    assert(type_info.base_type == TYPE_FUNCTION);
    assert(type_info.return_type == TYPE_INT);
    assert(type_info.param_types.length() == 2);
    assert(type_info.param_types[0] == TYPE_INT);
    assert(type_info.param_types[1] == TYPE_INT);
}

#[test]
func test_optimization() {
    // Test constant folding
    let source = "2 + 3 * 4";
    let ast = parse(source);
    let optimized = fold_constants(ast);
    assert(optimized.type == NODE_INTEGER_LITERAL);
    assert(optimized.value == 14);
    
    // Test strength reduction
    source = "x * 2";
    ast = parse(source);
    optimized = reduce_strength(ast);
    assert(optimized.type == NODE_BINARY_OP);
    assert(optimized.op == TOKEN_SHIFT_LEFT);
    assert(optimized.right.type == NODE_INTEGER_LITERAL);
    assert(optimized.right.value == 1);
    
    // Test dead code elimination
    source = "if (false) { return 42; } return 0;";
    ast = parse(source);
    optimized = eliminate_dead_code(ast);
    assert(optimized.type == NODE_RETURN);
    assert(optimized.value.type == NODE_INTEGER_LITERAL);
    assert(optimized.value.value == 0);
}

#[test]
func test_code_generation() {
    // Test arithmetic operations
    let source = "1 + 2";
    let ast = parse(source);
    let code = generate_code(ast);
    assert(code.length() == 3);  // Load 1, Load 2, Add
    assert(code[0].type == INSTR_CONST && code[0].value == 1);
    assert(code[1].type == INSTR_CONST && code[1].value == 2);
    assert(code[2].type == INSTR_ADD);
    
    // Test function calls
    source = "add(1, 2)";
    ast = parse(source);
    code = generate_code(ast);
    assert(code.length() == 4);  // Load 1, Load 2, Call add
    assert(code[0].type == INSTR_CONST && code[0].value == 1);
    assert(code[1].type == INSTR_CONST && code[1].value == 2);
    assert(code[2].type == INSTR_CALL && code[2].name == "add");
    
    // Test control flow
    source = "if (x > 0) { return x; }";
    ast = parse(source);
    code = generate_code(ast);
    assert(code.length() > 4);  // Load x, Compare, Branch, Return
    assert(code[0].type == INSTR_LOAD && code[0].name == "x");
    assert(code[1].type == INSTR_CONST && code[1].value == 0);
    assert(code[2].type == INSTR_GT);
    assert(code[3].type == INSTR_BR_IF);
}

#[test]
func test_error_handling() {
    // Test syntax errors
    let source = "1 +";  // Missing right operand
    #[should_panic]
    parse(source);
    
    // Test type errors
    source = "let x: i32 = \"hello\";";
    let ast = parse(source);
    #[should_panic]
    check_types(ast);
    
    // Test undefined variable
    source = "x + 1";
    ast = parse(source);
    #[should_panic]
    check_types(ast);
    
    // Test division by zero
    source = "1 / 0";
    ast = parse(source);
    let code = generate_code(ast);
    #[should_panic]
    execute(code);
}

#[test]
func test_memory_management() {
    // Test allocation
    let ptr = allocate_memory(100);
    assert(ptr != null);
    
    // Test bounds checking
    #[should_panic]
    @(ptr + 100);  // Out of bounds access
    
    // Test cleanup
    free_memory(ptr);
    
    // Test memory tracking
    let stats = get_memory_stats();
    assert(stats.allocated == 0);
    assert(stats.freed == 100);
    
    // Test leak detection
    let ptr2 = allocate_memory(50);
    // ptr2 not freed - should be detected
    #[should_panic]
    check_memory_leaks();
} 