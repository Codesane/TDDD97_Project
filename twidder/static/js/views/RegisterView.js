define([
	'jquery',
	'handlebars',
	'backbone',
	'text!templates/register_view_template.html'
], function($, Handlebars, Backbone, RegisterViewTemplate) {
	
	var RegisterView = Backbone.View.extend({

		el: '#app-container',

		render: function() {
			var self = this;

			var registerHtml = $(RegisterViewTemplate);

			registerHtml.hide();
			
			self.$el.html(registerHtml);
			registerHtml.fadeIn();
		}
	});

	return RegisterView;
});