var ASSETS = "assets/";

var face_list = [
	ASSETS + 'guy_front.png',
	ASSETS + 'guy_right.png',
	ASSETS + 'guy_back.png',
	ASSETS + 'guy_left.png'
]

TILE = {
	GRASS: '.',
	WALL: 'o',
	STAR: '*',
}

var grass = PIXI.Texture.fromImage('assets/Grass Block.png');
var wall = PIXI.Texture.fromImage('assets/Wall Block.png');
var star = PIXI.Texture.fromImage('assets/Star.png');

function __draw_map(stage, scale, data) {

	var x = 0;
	var y = -50 * scale;
	var tail_x = 100 * scale;
	var tail_y = 80 * scale;

	$.each(data.content, function(_, line) {
		for (i=0; i < line.length; i++) {
			var element = line[i];
			if (element === TILE.WALL) {
				var tile = new PIXI.Sprite(wall);
			} else {
				var tile = new PIXI.Sprite(grass);
			}
			tile.position.x = x;
			tile.position.y = y;
			tile.scale.x = scale;
			tile.scale.y = scale;
			stage.addChild(tile);

			x += tail_x;
		}
		y += tail_y;
		x = 0;
	});
}

function __draw_stars(stage, scale, data) {

	var x = 0;
	var y = -80 * scale;
	var tail_x = 100 * scale;
	var tail_y = 80 * scale;

	$.each(data.content, function(_, line) {
		for (i=0; i < line.length; i++) {
			var element = line[i];
			if (element === TILE.STAR) {
				var tile = new PIXI.Sprite(star);
				tile.position.x = x;
				tile.position.y = y;
				tile.scale.x = scale;
				tile.scale.y = scale;
				stage.addChild(tile);
			}
			x += tail_x;
		}
		y += tail_y;
		x = 0;
	});

}



var GAME = function(data, element, editor) {
	var scale = element.width() / data.content.length / 100;

	var stage = new PIXI.Stage;
	var renderer = new PIXI.WebGLRenderer(element.width(), element.height());

	element.html(renderer.view)

	__draw_map(stage, scale, data);
	__draw_stars(stage, scale, data);

	requestAnimationFrame(animate);

    function animate() {
		renderer.render(stage);
        requestAnimationFrame(animate);
    }
};

