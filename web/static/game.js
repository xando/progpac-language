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
var guy = PIXI.Texture.fromImage('assets/guy_front.png');
var guy_back = PIXI.Texture.fromImage('assets/guy_back.png');


var TILE_HEIGHT = 100;
var TILE_WIDTH = 80;

var LAYER_1_Y_SHIFT = -50;
var LAYER_2_Y_SHIFT = -80;


function __draw_map(stage, scale, data) {

	var x = 0;
	var y = LAYER_1_Y_SHIFT * scale;
	var tile_x = TILE_HEIGHT * scale;
	var tile_y = TILE_WIDTH * scale;

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

			x += tile_x;
		}
		y += tile_y;
		x = 0;
	});
}

function __draw_stars(stage, scale, data) {

	var x = 0;
	var y = LAYER_2_Y_SHIFT * scale;
	var tile_x = TILE_HEIGHT * scale;
	var tile_y = TILE_WIDTH * scale;

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
			x += tile_x;
		}
		y += tile_y;
		x = 0;
	});

}

function __draw_guy(stage, scale, data) {
	var x = 0;
	var y = LAYER_2_Y_SHIFT * scale;
	var tile_x = TILE_HEIGHT * scale;
	var tile_y = TILE_WIDTH * scale;

	for (i=0; i < data.content.length; i++) {
		for (j=0; j < data.content.length; j++) {
			if (["0", "1", "2", "3"].indexOf(data.content[i][j]) !== -1) {
				var tile = new PIXI.Sprite(guy);
				tile.position.x = x;
				tile.position.y = y;
				tile.scale.x = scale;
				tile.scale.y = scale;
				stage.addChild(tile);
				return tile;
			}
			x += tile_x;
		}
		y += tile_y;
		x = 0;
	}
}


var GAME = function(data, element, editor) {
	var scale = element.width() / data.content.length / 100;

	var stage = new PIXI.Stage;
	var renderer = new PIXI.WebGLRenderer(element.width(), element.height());

	element.html(renderer.view)

	__draw_map(stage, scale, data);
	__draw_stars(stage, scale, data);
	var guy = __draw_guy(stage, scale, data);

	renderer.render(stage);
	// requestAnimationFrame(animate);

    // function animate() {
        // requestAnimationFrame(animate);
		// guy.setTexture(guy_back);
    // }
};

