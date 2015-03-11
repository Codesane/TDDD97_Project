define([
	'jquery',
	'handlebars',
	'backbone',
	'text!templates/login_view_template.html'
], function($, Handlebars, Backbone, LoginViewTemplate) {
	
	var LoginView = Backbone.View.extend({

		el: '#app-container',

		render: function() {

			var loginHtml = $(LoginViewTemplate);

			loginHtml.hide();
			this.$el.html(loginHtml);
			loginHtml.fadeIn();
		}
	});

	return LoginView;
});