use wasm_bindgen::prelude::*;
use web_sys::{CanvasRenderingContext2d, HtmlCanvasElement};

#[wasm_bindgen]
pub struct Game {
    canvas: HtmlCanvasElement,
    ctx: CanvasRenderingContext2d,
    player_x: f64,
    player_y: f64,
}

#[wasm_bindgen]
impl Game {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        let canvas = document()
            .get_element_by_id("canvas")
            .unwrap()
            .dyn_into::<HtmlCanvasElement>()
            .unwrap();
        
        let ctx = canvas
            .get_context("2d")
            .unwrap()
            .unwrap()
            .dyn_into::<CanvasRenderingContext2d>()
            .unwrap();

        Self {
            canvas,
            ctx,
            player_x: 200.0,
            player_y: 150.0,
        }
    }

    pub fn start(&self) {
        self.draw();
    }

    pub fn move_player(&mut self, dx: f64, dy: f64) {
        self.player_x += dx;
        self.player_y += dy;
        self.draw();
    }

    fn draw(&self) {
        self.ctx.clear_rect(0.0, 0.0, self.canvas.width() as f64, self.canvas.height() as f64);
        
        // Draw player
        self.ctx.begin_path();
        self.ctx.arc(self.player_x, self.player_y, 20.0, 0.0, 2.0 * std::f64::consts::PI);
        self.ctx.set_fill_style(&JsValue::from_str("green"));
        self.ctx.fill();
    }
}

#[wasm_bindgen]
pub struct ParticleSystem {
    particles: Vec<Particle>,
    canvas: HtmlCanvasElement,
    ctx: CanvasRenderingContext2d,
}

#[wasm_bindgen]
impl ParticleSystem {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        let canvas = document()
            .get_element_by_id("canvas")
            .unwrap()
            .dyn_into::<HtmlCanvasElement>()
            .unwrap();
        
        let ctx = canvas
            .get_context("2d")
            .unwrap()
            .unwrap()
            .dyn_into::<CanvasRenderingContext2d>()
            .unwrap();

        Self {
            particles: Vec::new(),
            canvas,
            ctx,
        }
    }

    pub fn add_particle(&mut self, x: f64, y: f64) {
        self.particles.push(Particle::new(x, y));
    }

    pub fn update(&mut self) {
        for particle in &mut self.particles {
            particle.update();
        }
        self.particles.retain(|p| p.life > 0.0);
        self.draw();
    }

    fn draw(&self) {
        self.ctx.clear_rect(0.0, 0.0, self.canvas.width() as f64, self.canvas.height() as f64);
        
        for particle in &self.particles {
            self.ctx.begin_path();
            self.ctx.arc(particle.x, particle.y, 2.0, 0.0, 2.0 * std::f64::consts::PI);
            self.ctx.set_fill_style(&JsValue::from_str("rgba(255, 255, 255, 0.5)"));
            self.ctx.fill();
        }
    }
}

struct Particle {
    x: f64,
    y: f64,
    vx: f64,
    vy: f64,
    life: f64,
}

impl Particle {
    fn new(x: f64, y: f64) -> Self {
        Self {
            x,
            y,
            vx: (rand::random::<f64>() - 0.5) * 2.0,
            vy: (rand::random::<f64>() - 0.5) * 2.0,
            life: 1.0,
        }
    }

    fn update(&mut self) {
        self.x += self.vx;
        self.y += self.vy;
        self.life -= 0.01;
    }
} 