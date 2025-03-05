use wasm_bindgen::prelude::*;
use crate::interpreter::evaluator::Evaluator;
use crate::compiler::lexer::Lexer;
use crate::compiler::parser::Parser;
use serde_json;

#[wasm_bindgen]
pub struct LumaScript {
    evaluator: Evaluator,
}

#[wasm_bindgen]
impl LumaScript {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        console_error_panic_hook::set_once();
        Self {
            evaluator: Evaluator::new(),
        }
    }

    pub fn eval(&mut self, code: &str) -> Result<String, String> {
        let lexer = Lexer::new(code);
        let mut parser = Parser::new(lexer);
        let ast = parser.parse()?;
        
        let result = self.evaluator.eval(&ast)?;
        Ok(format!("{:?}", result))
    }

    pub fn get_cache_stats(&self) -> JsValue {
        let (ast_stats, value_stats) = self.evaluator.get_cache_stats();
        let metrics = self.evaluator.get_performance_metrics();
        
        let stats = serde_json::json!({
            "ast_cache": {
                "size": ast_stats.size,
                "hit_ratio": ast_stats.hit_ratio,
                "hit_count": ast_stats.hit_count,
                "miss_count": ast_stats.miss_count,
            },
            "value_cache": {
                "size": value_stats.size,
                "hit_ratio": value_stats.hit_ratio,
                "hit_count": value_stats.hit_count,
                "miss_count": value_stats.miss_count,
            },
            "performance": {
                "avg_eval_time": metrics.avg_eval_time(),
                "cache_hit_ratio": metrics.cache_hit_ratio(),
            }
        });

        JsValue::from_serde(&stats).unwrap()
    }
} 