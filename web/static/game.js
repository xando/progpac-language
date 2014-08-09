TILE = {
	GRASS: '.',
	WALL: 'o',
	STAR: '*',
}

var grass = 'assets/Grass Block.png';
var wall = 'assets/Wall Block.png';
var star = 'assets/Star.png';

var guy = {
	'0': 'assets/guy_back.png',
	'1': 'assets/guy_right.png',
	'2': 'assets/guy_front.png',
	'3': 'assets/guy_left.png',
}

var HEIGHT = 580;
var WIDTH = 600;
var TILE_HEIGHT = 83;
var TILE_WIDTH = 100;

var LAYER_1_Y_SHIFT = -50;
var LAYER_2_Y_SHIFT = -70;


var Game = function(element, world) {
	this.stage = new createjs.Stage("render");
	this.scaleX = WIDTH / world.length / TILE_WIDTH;
	this.scaleY = HEIGHT / world.length / TILE_HEIGHT;

	this.world = world;

	this.drawWorld();
	this.stars = this.drawStars();
	this.guy = this.drawGuy();

	createjs.Ticker.setFPS(20);
	createjs.Ticker.addEventListener("tick", this.stage);
};

Game.prototype.drawWorld = function() {
	var x = 0;
	var y = LAYER_1_Y_SHIFT * this.scaleY;
	var tile_x = TILE_WIDTH * this.scaleX;
	var tile_y = TILE_HEIGHT * this.scaleY;

	for(i=0; i < this.world.length; i++) {
		for (j=0; j < this.world[i].length; j++) {
			if (this.world[i][j] === TILE.WALL) {
				var tile = new createjs.Bitmap(wall);
			} else {
				var tile = new createjs.Bitmap(grass);
			}
			tile.x = x;
			tile.y = y;
			tile.scaleX = this.scaleX;
			tile.scaleY = this.scaleY;
			this.stage.addChild(tile);

			x += tile_x;
		}
		y += tile_y;
		x = 0;
	}
};

Game.prototype.drawGuy = function() {
	var tile_x = TILE_WIDTH * this.scaleX;
	var tile_y = TILE_HEIGHT * this.scaleY;

	for(i=0; i < this.world.length; i++) {
		for (j=0; j < this.world[i].length; j++) {
			if (["0", "1", "2", "3"].indexOf(this.world[i][j]) !== -1) {
				var tile = new createjs.Bitmap(guy[this.world[i][j]]);
				tile.x = tile_x * j;
				tile.y = LAYER_2_Y_SHIFT + tile_y * i;
				tile.scaleX = this.scaleX;
				// TODO: wrong scaling
				tile.scaleY = this.scaleX;
				tile.direction = this.world[i][j];
				this.stage.addChild(tile);
				return tile;
			}
		}
	}
};

Game.prototype.drawStars = function() {
	var x = 0;
	var y = LAYER_2_Y_SHIFT * this.scaleY;
	var tile_x = TILE_WIDTH * this.scaleX;
	var tile_y = TILE_HEIGHT * this.scaleY;

	var stars = [];

	for(i=0; i < this.world.length; i++) {
		for (j=0; j < this.world[i].length; j++) {
			if (this.world[i][j] === TILE.STAR) {
				var tile = new createjs.Bitmap(star);
				tile.x = x;
				tile.y = y;
				tile.scaleX = this.scaleX;
				// TODO: wrong scaling
				tile.scaleY = this.scaleX;
				this.stage.addChild(tile);

				createjs.Tween.get(tile, {loop:true})
					.to({y:y-20}, 1500, createjs.Ease.linear)
					.to({y:y}, 1500, createjs.Ease.linear);

				var shadow = new createjs.Shape();
				shadow.graphics.beginFill("black").drawEllipse(x, y, 20, 10);
				shadow.regX = 10;
				shadow.regy = 5;
				// shadow.alpha = 0.4

				this.stage.addChild(shadow);

				stars.push(tile);
				// debugger
				// createjs.Tween.get(shadow, {loop:true})
				// .to({alpha:0.2}, 1500, createjs.Ease.linear);
					// .to({scaleX:1.1, alpha:0.4}, 1500, createjs.Ease.linear)
					// .to({h:15}, 1500, createjs.Ease.linear);

			}
			x += tile_x;
		}
		y += tile_y;
		x = 0;
	}

	return stars;
}


Game.prototype.reset = function() {
	for (i=0; i<this.stars.length; i++) {
		this.stage.removeChild(this.stars[i]);
	}
	this.stage.removeChild(this.guy);

	this.stars = this.drawStars();
	this.guy = this.drawGuy();
}


Game.prototype.walk = function(path) {
	self = this;

	var tile_x = TILE_WIDTH * this.scaleX;
	var tile_y = TILE_HEIGHT * this.scaleY;

	var tween = createjs.Tween.get(this.guy);

	var direction = this.guy.direction;
	var x = this.guy.x;
	var y = this.guy.y;

	var path_elements = path.split('');

	while (element = path_elements.shift()) {

		if (["0", "1", "2", "3"].indexOf(element) !== -1) {
			direction = parseInt(element)
			element = path_elements.shift();
			tween.wait(200);
			tween.set({src: guy[direction]}, this.guy.image);
		}
		if (element == 's') {
			if (direction == 0) {
				y -= tile_y;
				tween.to({y: y}, 300, createjs.Ease.linear)
			} else if (direction == 1) {
				x -= tile_x;
				tween.to({x: x}, 300, createjs.Ease.linear)
			} else if (direction == 2) {
				y += tile_y;
				tween.to({y: y}, 300, createjs.Ease.linear)
			} else if (direction == 3) {
				x -= tile_x;
				tween.to({x: x}, 300, createjs.Ease.linear)
			}
			tween.call(function() {
				// Naive hit test
				for(i=0; i<self.stars.length; i++) {
					var star = self.stars[i];
					if ((Math.abs(star.x - self.guy.x) < TILE_HEIGHT / 2) &&
						(Math.abs(star.y - self.guy.y) < TILE_WIDTH / 2)) {
						self.stage.removeChild(star)
					}
				}
			});
		}
	}
}
