var canvas;

var width;
var height;
var context;

var blur;

var fps = 30;
var timerID;

var stats_rate = fps;
var stats_limiter = stats_rate;
var stats_time_lastTick = 0;
var stats_time_preRender = 0;
var stats_time_postRender = 0;
var stats_acc_ticks = 0;
var stats_acc_renderTime = 0;
var stats_acc_updateTime = 0;
var stats_acc_tickTime = 0;

function aquire() {
	var jq_canvas = $("#graphics");
	
	canvas = jq_canvas[0];
	context = canvas.getContext("2d");
	
	width = canvas.width;
	height = canvas.height;
}

function initialise() {
	particle_init(canvas, context);
}
function update() {
	particle_update();
}

function render() {
	if(blur) {
		context.fillStyle = "#000000";
		context.globalAlpha = 0.2;
		context.fillRect(0, 0, width, height);
		context.globalAlpha = 1;
	} else {
		context.fillStyle = "#000000";
		context.fillRect(0, 0, width, height);
	}

	particle_render(context);
}

function updateStats() {
	var avgFPS = 1000 / (stats_acc_tickTime / stats_acc_ticks);
	var avgUpdateTime = stats_acc_updateTime / stats_acc_ticks;
	var avgRenderTime = stats_acc_renderTime / stats_acc_ticks;
	var potentialFPS = 1000 / (avgRenderTime + avgUpdateTime);
	
	var out = "<b>Average FPS:</b>" + avgFPS.toFixed(1) + "&nbsp;";
	out += "<b>Potential FPS:</b>" + potentialFPS.toFixed(1) + "&nbsp;";
	out += "<b>Average update:</b>" + avgUpdateTime.toFixed(1) + "ms&nbsp;";
	out += "<b>Average render:</b>" + avgRenderTime.toFixed(1) + "ms&nbsp;";
	out += "<b>Particles:</b>" + get_rendered_particle_count();
	
	$("#stats").html(out);
	
	// Reset the accumulators
	stats_acc_ticks = 0;
	stats_acc_updateTime = 0;
	stats_acc_renderTime = 0;
	stats_acc_tickTime = 0;
	
	// Reset the stat limiter
	stats_limiter = stats_rate;
}

function tick() {
	stats_acc_ticks += 1;

	stats_time_preUpdate = new Date().getTime();
	update();
	stats_time_postUpdate = new Date().getTime();

	stats_time_preRender = stats_time_postUpdate;
	render();
	stats_time_postRender = new Date().getTime();

	stats_acc_renderTime += stats_time_postRender - stats_time_preRender;
	stats_acc_updateTime += stats_time_postUpdate - stats_time_preUpdate;

	stats_acc_tickTime += stats_time_preUpdate - stats_time_lastTick;
	stats_time_lastTick = stats_time_preUpdate;

	if(--stats_limiter < 1) {
		updateStats();
	}
}

function updateBlur() {
	blur = $('#blur').is(':checked');
}

$(document).ready(function() {
	$('#blur').click(updateBlur);
	updateBlur();
	
	aquire();
	initialise();
	stats_time_lastTick = new Date().getTime();
	timerID = setInterval(tick, 1000/fps);
});
