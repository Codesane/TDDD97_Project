define([
	'jquery',
	'handlebars',
	'Router'
], function($, Handlebars, Router) {

	var App = function() {  }

	App.prototype.init = function() {
		Handlebars.registerHelper('faGender', function(gender) {

			var male = 'fa-mars';
			var female = 'fa-venus';
			var defaultGender = 'fa-transgender'; // Yeah. If you're neither you're both.

			var genderMap = {
				'male': 'fa-mars',
				'female': 'fa-venus',
				'transgender': 'fa-transgender'
			};

			var faUse = genderMap[gender.toLowerCase()];
			if(typeof faUse === 'undefined') {
				faUse = 'fa-mercury'; // I don't know?
			}

			return faUse;
		});

		/* Starting the application router. */
		var appRouter = new Router();
		Backbone.history.start();
	}

	return App;
});