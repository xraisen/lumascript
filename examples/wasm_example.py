from src.core.compiler import LumaCompiler
from src.core.parser import WASMParser
from src.wasm.decoder import WASMDecoder
from src.utils.logger import Logger

def main():
    logger = Logger(__name__)
    
    # Example LumaScript code with multiple functions
    source = """
    func add(a: i32, b: i32) -> i32 {
        return a + b;
    }
    
    func sub(a: i32, b: i32) -> i32 {
        return a - b;
    }
    
    func mul(a: i32, b: i32) -> i32 {
        return a * b;
    }
    """
    
    try:
        # Compile to WASM
        logger.info("Compiling LumaScript to WASM...")
        compiler = LumaCompiler()
        wasm_binary = compiler.compile(source)
        
        # Convert to hex for inspection
        wasm_hex = wasm_binary.hex()
        logger.info(f"\nWASM Hex:\n{wasm_hex}")
        
        # Parse WASM for verification
        logger.info("\nParsing WASM...")
        parser = WASMParser()
        result = parser.parse(wasm_hex)
        
        # Print parsed structure
        logger.info("\nParsed WASM Structure:")
        logger.info(f"Version: {result['version']}")
        logger.info(f"Sections: {len(result['sections'])}")
        
        for section in result['sections']:
            logger.info(f"\nSection {section['id']}:")
            logger.info(f"  Size: {section['size']} bytes")
            
            if section['id'] == 1:  # Type section
                types = section['content']['types']
                logger.info(f"  Types: {len(types)}")
                for i, type_def in enumerate(types):
                    logger.info(f"    Type {i}:")
                    logger.info(f"      Form: {type_def['form']}")
                    logger.info(f"      Params: {type_def['params']}")
                    logger.info(f"      Results: {type_def['results']}")
                    
            elif section['id'] == 3:  # Function section
                indices = section['content']['indices']
                logger.info(f"  Function Indices: {indices}")
                
            elif section['id'] == 7:  # Export section
                exports = section['content']['exports']
                logger.info(f"  Exports: {len(exports)}")
                for export in exports:
                    logger.info(f"    {export['name']} (kind: {export['kind']}, index: {export['index']})")
                    
            elif section['id'] == 10:  # Code section
                bodies = section['content']['bodies']
                logger.info(f"  Function Bodies: {len(bodies)}")
                for i, body in enumerate(bodies):
                    logger.info(f"    Body {i}:")
                    logger.info(f"      Locals: {len(body['locals'])}")
                    logger.info(f"      Instructions: {len(body['instructions'])}")
                    for instr in body['instructions']:
                        logger.info(f"        {instr['name']}")
                        if 'operands' in instr:
                            logger.info(f"          Operands: {instr['operands']}")
        
        # Decode instructions
        logger.info("\nDecoding WASM instructions...")
        decoder = WASMDecoder()
        sections = decoder.decode_sections(wasm_binary)
        
        # Print decoded instructions
        for section in sections:
            if section['id'] == 10:  # Code section
                logger.info("\nDecoded Instructions:")
                for i, body in enumerate(section['content']['bodies']):
                    logger.info(f"\nFunction {i}:")
                    for instr in body['instructions']:
                        logger.info(f"  {instr['name']}")
                        if 'operands' in instr:
                            logger.info(f"    Operands: {instr['operands']}")
                            
    except Exception as e:
        logger.error(f"Error: {e}")
        raise

if __name__ == "__main__":
    main() 