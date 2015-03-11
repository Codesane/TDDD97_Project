define([
	'backbone'
], function(Backbone) {

	var AppRouter = Backbone.Router.extend({
		routes: {
			'': 'index'
		},

		index: function() {
			console.log('Index route.');
		}

	});

	return AppRouter;
});