import init, { LumaInterpreter } from 'lumascript';

async function runLumaScript() {
    await init();
    
    const interpreter = new LumaInterpreter();
    const code = `
        func main() {
            print("Hello from LumaScript!");
        }
    `;
    
    try {
        await interpreter.eval(code);
    } catch (e) {
        console.error("Execution error:", e);
    }
}

runLumaScript(); 