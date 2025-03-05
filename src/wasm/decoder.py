from typing import List, Dict, Tuple
import struct
from .instructions import WASM_INSTRUCTIONS

class WASMDecoder:
    def __init__(self):
        self.position = 0
        self.instructions = WASM_INSTRUCTIONS

    def decode_sections(self, data: bytes) -> List[dict]:
        """Decode WASM sections from binary data"""
        sections = []
        while self.position < len(data):
            section = self._decode_section(data)
            if section:
                sections.append(section)
        return sections

    def _decode_section(self, data: bytes) -> dict:
        """Decode a single WASM section"""
        section_id = data[self.position]
        self.position += 1
        
        # Decode section size (LEB128)
        size, bytes_read = self._decode_leb128(data[self.position:])
        self.position += bytes_read
        
        # Read section content
        content = data[self.position:self.position + size]
        self.position += size
        
        return {
            "id": section_id,
            "size": size,
            "content": self._decode_section_content(section_id, content)
        }

    def _decode_leb128(self, data: bytes) -> Tuple[int, int]:
        """Decode LEB128 variable-length integer"""
        result = 0
        shift = 0
        bytes_read = 0
        
        while True:
            byte = data[bytes_read]
            result |= (byte & 0x7f) << shift
            bytes_read += 1
            if not (byte & 0x80):
                break
            shift += 7
            
        return result, bytes_read

    def _decode_section_content(self, section_id: int, content: bytes) -> dict:
        """Decode section content based on section ID"""
        decoders = {
            1: self._decode_type_section,
            3: self._decode_function_section,
            7: self._decode_export_section,
            10: self._decode_code_section
        }
        
        decoder = decoders.get(section_id, self._decode_unknown_section)
        return decoder(content)

    def _decode_type_section(self, content: bytes) -> dict:
        """Decode type section (function signatures)"""
        count, pos = self._decode_leb128(content)
        types = []
        
        for _ in range(count):
            form = content[pos]
            pos += 1
            
            param_count, bytes_read = self._decode_leb128(content[pos:])
            pos += bytes_read
            params = list(content[pos:pos + param_count])
            pos += param_count
            
            result_count, bytes_read = self._decode_leb128(content[pos:])
            pos += bytes_read
            results = list(content[pos:pos + result_count])
            pos += result_count
            
            types.append({
                "form": form,
                "params": params,
                "results": results
            })
            
        return {"count": count, "types": types}

    def _decode_function_section(self, content: bytes) -> dict:
        """Decode function section (type indices)"""
        count, pos = self._decode_leb128(content)
        indices = []
        
        while pos < len(content):
            index, bytes_read = self._decode_leb128(content[pos:])
            pos += bytes_read
            indices.append(index)
            
        return {"count": count, "indices": indices}

    def _decode_export_section(self, content: bytes) -> dict:
        """Decode export section"""
        count, pos = self._decode_leb128(content)
        exports = []
        
        for _ in range(count):
            name_len, bytes_read = self._decode_leb128(content[pos:])
            pos += bytes_read
            name = content[pos:pos + name_len].decode('utf-8')
            pos += name_len
            
            kind = content[pos]
            pos += 1
            index, bytes_read = self._decode_leb128(content[pos:])
            pos += bytes_read
            
            exports.append({
                "name": name,
                "kind": kind,
                "index": index
            })
            
        return {"count": count, "exports": exports}

    def _decode_code_section(self, content: bytes) -> dict:
        """Decode code section (function bodies)"""
        count, pos = self._decode_leb128(content)
        bodies = []
        
        for _ in range(count):
            body_size, bytes_read = self._decode_leb128(content[pos:])
            pos += bytes_read
            body = content[pos:pos + body_size]
            pos += body_size
            
            bodies.append(self._decode_function_body(body))
            
        return {"count": count, "bodies": bodies}

    def _decode_function_body(self, body: bytes) -> dict:
        """Decode a function body"""
        local_count, pos = self._decode_leb128(body)
        locals = []
        
        for _ in range(local_count):
            count, bytes_read = self._decode_leb128(body[pos:])
            pos += bytes_read
            type_byte = body[pos]
            pos += 1
            locals.append({"count": count, "type": type_byte})
            
        instructions = self._decode_instructions(body[pos:])
        
        return {
            "local_count": local_count,
            "locals": locals,
            "instructions": instructions
        }

    def _decode_instructions(self, data: bytes) -> List[dict]:
        """Decode WASM instructions"""
        instructions = []
        pos = 0
        
        while pos < len(data):
            opcode = data[pos]
            pos += 1
            
            if opcode not in self.instructions:
                raise ValueError(f"Unknown opcode: 0x{opcode:02x}")
                
            instruction = self.instructions[opcode]
            operands = []
            
            for operand_type in instruction["operands"]:
                if operand_type == "leb128":
                    value, bytes_read = self._decode_leb128(data[pos:])
                    pos += bytes_read
                    operands.append(value)
                elif operand_type == "i32":
                    value = struct.unpack("<i", data[pos:pos + 4])[0]
                    pos += 4
                    operands.append(value)
                    
            instructions.append({
                "opcode": opcode,
                "name": instruction["name"],
                "operands": operands
            })
            
        return instructions

    def _decode_unknown_section(self, content: bytes) -> dict:
        """Decode unknown section (raw bytes)"""
        return {"raw": content.hex()} 