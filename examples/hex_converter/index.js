import init, { LumaHexConverter } from './pkg/lumascript.js';

async function demo() {
    await init();
    
    const converter = new LumaHexConverter();
    
    // Text to hex
    const text = "LumaScript";
    const hex = converter.text_to_hex(text);
    console.log(`Text: ${text}`);
    console.log(`Hex: ${hex}`);
    
    // Hex to text
    const decoded = converter.hex_to_text(hex);
    console.log(`Decoded: ${decoded}`);
    
    // Get operation stats
    console.log(converter.get_stats());
}

demo(); 