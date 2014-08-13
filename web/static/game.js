TILE = {
	GRASS: '.',
	WALL: '#',
	STAR: '*',
	TREE: '^',
	ROCK: '@',
}

TILES = {
	guy0: '/static/assets/guy_back.png',
	guy1: '/static/assets/guy_right.png',
	guy2: '/static/assets/guy_front.png',
	guy3: '/static/assets/guy_left.png',

	grass: '/static/assets/Grass Block.png',
	wall: '/static/assets/Stone Block.png',
	star: '/static/assets/Star.png',
	tree: '/static/assets/Tree Short.png',
	rock: '/static/assets/Rock.png',
}

SOUNDS = {
	star : '/static/assets/music/star_pickup.wav',
	wrong : '/static/assets/music/wrong_move.wav'
}

var HEIGHT = 600;
var WIDTH = 600;
var TILE_HEIGHT = 83;
var TILE_WIDTH = 100;

var LAYER_1_Y_SHIFT = -5;
var LAYER_2_Y_SHIFT = -25;


var Game = function($level, world) {
	this.world = world;

	var scale = WIDTH / world.length / TILE_WIDTH;

	this.stage = new createjs.Stage($level.find('#render')[0]);
	this.stage.scaleX = scale;
	this.stage.scaleY = scale;

	this.layer1 = new createjs.Container();
	this.stage.addChild(this.layer1);

	this.layer2 = new createjs.Container();
	this.layer2.y = LAYER_2_Y_SHIFT;
	this.stage.addChild(this.layer2);

	this.resources = new createjs.LoadQueue();

	for (var key in TILES) {
		this.resources.loadFile({id:key, src:TILES[key]});
	}

	for (var key in SOUNDS) {
		createjs.Sound.registerSound(SOUNDS[key], key);
	}

	this.resources.on("complete", function() {

		this.drawMap();
		this.guy = this.drawGuy();
		this.stars = this.drawStars();

		createjs.Ticker.setFPS(80);
		createjs.Ticker.addEventListener("tick", this.stage);

		$level.show()

	}, this);
};

Game.prototype.drawTile = function(type, x, y, layer) {
	var tile = new createjs.Bitmap(this.resources.getItem(type).src);
	tile.x = x;
	tile.y = y;
	layer.addChild(tile);
	return tile;
}

Game.prototype.drawMap = function() {
	var x = 0;
	var y = 0;
	for(i=0; i < this.world.length; i++) {
		for (j=0; j < this.world[i].length; j++) {
			if (this.world[i][j] === TILE.WALL) {
				this.drawTile('grass', x, y, this.layer1);
			} else if (this.world[i][j] === TILE.ROCK) {
				this.drawTile('grass', x, y, this.layer1);
				this.drawTile('rock', x, y, this.layer2);
			} else if (this.world[i][j] === TILE.TREE) {
				this.drawTile('grass', x, y, this.layer1);
				this.drawTile('tree', x, y, this.layer2);
			} else {
				this.drawTile('grass', x, y, this.layer1);
			}
			x += TILE_WIDTH;
		}
		y += TILE_HEIGHT;
		x = 0;
	}

}

Game.prototype.drawGuy = function() {
	var x = 0;
	var y = 0;
	for(i=0; i < this.world.length; i++) {
		for (j=0; j < this.world[i].length; j++) {

			if (["0", "1", "2", "3"].indexOf(this.world[i][j]) !== -1) {
				var guy = this.drawTile('guy' + this.world[i][j], x, y, this.layer2);
				guy.direction = parseInt(this.world[i][j])
				return guy;
			}

			x += TILE_WIDTH;
		}
		y += TILE_HEIGHT;
		x = 0;
	}
};

Game.prototype.drawStars = function() {
	var x = 0;
	var y = 0;

	var stars = [];

	for(i=0; i < this.world.length; i++) {
		for (j=0; j < this.world[i].length; j++) {
			if (this.world[i][j] === TILE.STAR) {
				var star = this.drawTile('star', x, y, this.layer2);
				stars.push(star);

				createjs.Tween.get(star, {loop:true})
					.to({y:y-20}, 1500, createjs.Ease.linear)
					.to({y:y}, 1500, createjs.Ease.linear);

				// ToDo: shadows

			}
			x += TILE_WIDTH;
		}
		y += TILE_HEIGHT;
		x = 0;
	}

	return stars;
}


Game.prototype.reset = function() {
	for (i=0; i<this.stars.length; i++) {
		this.layer2.removeChild(this.stars[i]);
	}
	this.layer2.removeChild(this.guy);

	this.stars = this.drawStars();
	this.guy = this.drawGuy();
}


Game.prototype.walk = function(path) {
	self = this;

	var path_elements = path.split('');
	var tween = createjs.Tween.get(this.guy);

	var direction = this.guy.direction;
	var x = this.guy.x;
	var y = this.guy.y;

	while (element = path_elements.shift()) {
		if (["r", "l"].indexOf(element) !== -1) {
			element = path_elements.shift();
			direction = parseInt(element)
			tween
				.wait(30)
				.set({src: this.resources.getResult('guy'+direction).src}, this.guy.image);
		}
		if (element == 's') {
			if (direction == 0) {
				y -= TILE_HEIGHT;
				tween.to({y: y}, 160, createjs.Ease.linear)
			} else if (direction == 1) {
				x += TILE_WIDTH;
				tween.to({x: x}, 160, createjs.Ease.linear)
			} else if (direction == 2) {
				y += TILE_HEIGHT;
				tween.to({y: y}, 160, createjs.Ease.linear)
			} else if (direction == 3) {
				x -= TILE_WIDTH;
				tween.to({x: x}, 160, createjs.Ease.linear)
			}
			tween.call(function() {
				// Naive hit test
				for(i=0; i<self.stars.length; i++) {
					var star = self.stars[i];
					if ((Math.abs(star.x - self.guy.x) < TILE_HEIGHT / 2) &&
						(Math.abs(star.y - self.guy.y) < TILE_WIDTH / 2)) {
						self.layer2.removeChild(star)

						createjs.Sound.play('star')
					}
				}
			});
		}
		if (element == 'x') {

			var shift_x = 0;
			var shift_y = 0;

			if (direction == 0) {
				tween.to({y: y - TILE_HEIGHT / 4}, 100, createjs.Ease.linear)
			} else if (direction == 1) {
				tween.to({x: x + TILE_WIDTH / 4}, 100, createjs.Ease.linear)
			} else if (direction == 2) {
				tween.to({y: y + TILE_HEIGHT / 4}, 100, createjs.Ease.linear)
			} else if (direction == 3) {
				tween.to({x: x - TILE_WIDTH / 4}, 100, createjs.Ease.linear)
			}
			tween.call(function () {
				createjs.Sound.play('wrong')
			})
			tween.to({x: x, y: y}, 100, createjs.Ease.linear)

		}
	}

	return tween;
}
