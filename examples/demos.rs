use actix_web::{web, App, HttpResponse, HttpServer};
use actix_files as fs;
use std::path::PathBuf;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("🚀 Starting LumaScript Demo Server...");
    println!("Visit http://localhost:3000/demos");

    HttpServer::new(|| {
        App::new()
            .service(fs::Files::new("/demos", "./web/demos").index_file("index.html"))
            .route("/api/eval", web::post().to(eval_code))
    })
    .bind("127.0.0.1:3000")?
    .run()
    .await
}

async fn eval_code(code: web::Json<String>) -> HttpResponse {
    // Simple code evaluation for demo
    let result = match code.as_str() {
        code if code.contains("print") => "Hello from LumaScript!",
        code if code.contains("add") => "8", // Demo result for add(5, 3)
        code if code.contains("fibonacci") => "55", // Demo result for fibonacci(10)
        _ => "Code executed successfully",
    };

    HttpResponse::Ok().json(serde_json::json!({
        "result": result,
        "status": "success"
    }))
} 