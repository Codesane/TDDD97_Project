requirejs.config({
	baseUrl: 'js',
	paths: {
		'jquery': 'libs/jquery-2.1.3',
		'bootstrap': 'libs/bootstrap',
		'backbone': 'libs/backbone',
		'underscore': 'libs/underscore'
	},
	shim: {
		'jquery': {
			exports: '$'
		},
		'bootstrap': {
			deps: [ 'jquery' ]
		},
		'backbone': {
			deps: [ 'underscore', 'jquery' ]
		},
		'app': {
			deps: [
				'bootstrap',
				'backbone'
			]
		}
	}
});

require(['app'], function(App) {
	var app = new App();
	app.init();

	console.log('Started App.');
});