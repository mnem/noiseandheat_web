var emitters;
var particle_count = 0;

function get_rendered_particle_count() {
	return particle_count;
}

function particle_init(canvas, context) {
	emitters = new Array();
	
	emitters.push(create_emitter_at(100, 100, "#ff0000", 1000));
	emitters.push(create_emitter_at(canvas.width / 2, 100, "#00ff00", 1000));
	emitters.push(create_emitter_at(canvas.width - 100, 100, "#0000ff", 1000));
	emitters.push(create_emitter_at(300, 300, "#ff00ff", 1000));
	emitters.push(create_emitter_at(canvas.width - 300, 300, "#00ffff", 1000));
	emitters.push(create_emitter_at(canvas.width/2, 500, "#ffffff", 1000));
}

function particle_update() {
    var i = emitters.length;
    while(i--) {
		emitter_update(emitters[i]);
	}
}

function particle_render(context) {
    var i = emitters.length;
    particle_count = 0;
    while(i--) {
		emitter_render(emitters[i], context);
	}
}

function emitter_update(e) {
    var i = e.particles.length;
    var p;
    var px;
    var py;
    var pl;

    while(i--) {
        p = e.particles[i];

        px = p.x + p.vx;
        py = p.y + p.vy;
        pl = p.life - 1;

        // Apply "Gravity"
        p.vy += 1;

        // Bounds check
        if( px < 0 ) pl = 0;
        if( px > width ) pl = 0;
        if( py < 0 ) pl = 0;
        if( py > height ) pl = 0;

        if( pl <= 0 ) {
            // It's dead
            emit_particle_at(e.x, e.y, p);
        } else {
            p.x = px;
            p.y = py;
            p.life = pl;
        }
    }
}

function emitter_render(e, context) {
    var i = e.particles.length;
    var p;

	context.fillStyle = e.colour;

    while(i--) {
        p = e.particles[i];
		context.fillRect(p.x, p.y, 1, 1);
        particle_count++;
	}
}

function create_emitter_at(x, y, colour, num_particles) {
	var e = {
		x:x,
		y:y,
		colour:colour,
		particles:new Array(num_particles),
	};
	
	for(var i = 0; i < e.particles.length; i++) {
		e.particles[i] = emit_particle_at(e.x, e.y, {});
	}
	
	return e;
}

function emit_particle_at(x, y, p) {
	p.x = x + -10 + (rand() * 20);
	p.y = y + -10 + (rand() * 20);
	
	p.vx = -10 + (rand() * 20);
	p.vy = -10 + (rand() * 20);
	
	p.life = 100 * rand();
	
	return p;
}