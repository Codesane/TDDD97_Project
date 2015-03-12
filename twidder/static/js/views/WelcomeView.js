define([
	'jquery',
	'backbone',
	'views/RegisterView',
	'views/LoginView',
	'text!templates/welcome_view_template.html'
], function($, Backbone, RegisterView, LoginView, WelcomeViewTemplate) {

	var WelcomeView = Backbone.View.extend({

		el: '#app-container',

		initialize: function() {
			var self = this;

			this.pages = {
				register: RegisterView,
				login: LoginView
			};
		},

		render: function(options) {
			var self = this;

			var _render = function(page) {
				new self.pages[page]().render();
			}

			if(this.$el.find('#welcome-view-container').length == 0) {
				var template = $(WelcomeViewTemplate);

				template.hide();
				this.$el.html(template);
				
				template.fadeIn(function() {
					_render(options.page);
				});
			} else {
				_render(options.page);
			}
		}
	});

	return WelcomeView;
});