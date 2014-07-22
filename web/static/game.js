var ASSETS = "assets/";

var face_list = [
	ASSETS + 'guy_front.png',
	ASSETS + 'guy_right.png',
	ASSETS + 'guy_back.png',
	ASSETS + 'guy_left.png'
]

var start_level = function(data, element) {

	var game = new Phaser.Game(element.width(), element.height(), Phaser.AUTO, 'render', {
		preload: preload,
		create: create,
		update: update
	});

	function preload() {
		game.load.image('grass', 'assets/Grass Block.png');
		game.load.image('wall', 'assets/Wall Block.png');
	}

	function create() {
		element.width();
		element.height()

		var x = 0;
		var y = 0;
		var tile_x = 100;
		var scale_x = element.width() / data.content.split('\n')[0].length;

		$.each(data.content.split('\n'), function(_, line) {
			for (i = 0; i < line.length; i++) {
				var tile = game.add.sprite(x, y, 'grass');
				tile.scale.x = scale_x;
				// x += scale_x * tile_x;
			}
			y += 80;
			x = 0;
		})
	}

	function update() {

	}
};

