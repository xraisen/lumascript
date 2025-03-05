"""
WASM instruction set definitions
Each instruction has:
- name: The instruction name
- operands: List of operand types
- category: Instruction category
"""

WASM_INSTRUCTIONS = {
    # Control instructions
    0x00: {"name": "unreachable", "operands": [], "category": "control"},
    0x01: {"name": "nop", "operands": [], "category": "control"},
    0x02: {"name": "block", "operands": ["blocktype"], "category": "control"},
    0x03: {"name": "loop", "operands": ["blocktype"], "category": "control"},
    0x04: {"name": "if", "operands": ["blocktype"], "category": "control"},
    0x05: {"name": "else", "operands": [], "category": "control"},
    0x0B: {"name": "end", "operands": [], "category": "control"},
    0x0C: {"name": "br", "operands": ["leb128"], "category": "control"},
    0x0D: {"name": "br_if", "operands": ["leb128"], "category": "control"},
    
    # Variable instructions
    0x20: {"name": "local.get", "operands": ["leb128"], "category": "variable"},
    0x21: {"name": "local.set", "operands": ["leb128"], "category": "variable"},
    0x22: {"name": "local.tee", "operands": ["leb128"], "category": "variable"},
    0x23: {"name": "global.get", "operands": ["leb128"], "category": "variable"},
    0x24: {"name": "global.set", "operands": ["leb128"], "category": "variable"},
    
    # Memory instructions
    0x28: {"name": "i32.load", "operands": ["leb128", "leb128"], "category": "memory"},
    0x29: {"name": "i64.load", "operands": ["leb128", "leb128"], "category": "memory"},
    0x2A: {"name": "f32.load", "operands": ["leb128", "leb128"], "category": "memory"},
    0x2B: {"name": "f64.load", "operands": ["leb128", "leb128"], "category": "memory"},
    
    # Numeric instructions
    0x41: {"name": "i32.const", "operands": ["i32"], "category": "numeric"},
    0x42: {"name": "i64.const", "operands": ["i64"], "category": "numeric"},
    0x43: {"name": "f32.const", "operands": ["f32"], "category": "numeric"},
    0x44: {"name": "f64.const", "operands": ["f64"], "category": "numeric"},
    
    # Arithmetic instructions
    0x6A: {"name": "i32.add", "operands": [], "category": "arithmetic"},
    0x6B: {"name": "i32.sub", "operands": [], "category": "arithmetic"},
    0x6C: {"name": "i32.mul", "operands": [], "category": "arithmetic"},
    0x6D: {"name": "i32.div_s", "operands": [], "category": "arithmetic"},
    0x6E: {"name": "i32.div_u", "operands": [], "category": "arithmetic"},
    
    # Comparison instructions
    0x45: {"name": "i32.eqz", "operands": [], "category": "comparison"},
    0x46: {"name": "i32.eq", "operands": [], "category": "comparison"},
    0x47: {"name": "i32.ne", "operands": [], "category": "comparison"},
    0x48: {"name": "i32.lt_s", "operands": [], "category": "comparison"},
    0x49: {"name": "i32.lt_u", "operands": [], "category": "comparison"},
    
    # Conversion instructions
    0xA7: {"name": "i32.wrap_i64", "operands": [], "category": "conversion"},
    0xA8: {"name": "i64.extend_i32_s", "operands": [], "category": "conversion"},
    0xA9: {"name": "i64.extend_i32_u", "operands": [], "category": "conversion"},
    0xBA: {"name": "i32.trunc_f32_s", "operands": [], "category": "conversion"},
    0xBB: {"name": "i32.trunc_f32_u", "operands": [], "category": "conversion"}
}

# Instruction categories for easy filtering
INSTRUCTION_CATEGORIES = {
    "control": ["unreachable", "nop", "block", "loop", "if", "else", "end", "br", "br_if"],
    "variable": ["local.get", "local.set", "local.tee", "global.get", "global.set"],
    "memory": ["i32.load", "i64.load", "f32.load", "f64.load"],
    "numeric": ["i32.const", "i64.const", "f32.const", "f64.const"],
    "arithmetic": ["i32.add", "i32.sub", "i32.mul", "i32.div_s", "i32.div_u"],
    "comparison": ["i32.eqz", "i32.eq", "i32.ne", "i32.lt_s", "i32.lt_u"],
    "conversion": ["i32.wrap_i64", "i64.extend_i32_s", "i64.extend_i32_u", "i32.trunc_f32_s", "i32.trunc_f32_u"]
}

def get_instruction(opcode: int) -> dict:
    """Get instruction details by opcode"""
    return WASM_INSTRUCTIONS.get(opcode, None)

def get_category_instructions(category: str) -> list:
    """Get all instructions in a category"""
    return INSTRUCTION_CATEGORIES.get(category, []) 