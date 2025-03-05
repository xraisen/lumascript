use criterion::{black_box, criterion_group, criterion_main, Criterion};
use lumascript::LumaHexConverter;

pub fn benchmark_conversions(c: &mut Criterion) {
    let mut converter = LumaHexConverter::new();
    
    c.bench_function("text_to_hex", |b| b.iter(|| {
        converter.text_to_hex(black_box("LumaScript Performance Test"))
    }));
    
    let hex = converter.text_to_hex("LumaScript Performance Test");
    c.bench_function("hex_to_text", |b| b.iter(|| {
        converter.hex_to_text(black_box(&hex))
    }));
}

criterion_group!(benches, benchmark_conversions);
criterion_main!(benches); 