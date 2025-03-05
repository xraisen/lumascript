use lumascript::interpreter::evaluator::Evaluator;
use lumascript::compiler::lexer::Lexer;
use lumascript::compiler::parser::Parser;

fn main() {
    let code = r#"
        func main() {
            print("Hello from LumaScript!");
        }
    "#;

    let lexer = Lexer::new(code);
    let mut parser = Parser::new(lexer);
    let ast = parser.parse().unwrap();
    
    let mut evaluator = Evaluator::new();
    let result = evaluator.eval(&ast).unwrap();
    
    println!("{}", result);
} 