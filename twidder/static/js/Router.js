define([
	'backbone',
	'views/RegisterView',
	'views/LoginView'
], function(Backbone, RegisterView, LoginView) {

	var AppRouter = Backbone.Router.extend({
		routes: {
			'': 'register',
			'register': 'register',
			'login': 'login'
		},

		register: function() {
			if(typeof this.registerView === 'undefined') {
				this.registerView = new RegisterView();
			}
			this.registerView.render();
		},

		login: function() {
			console.log('loginview');
			if(typeof this.loginView === 'undefined') {
				this.loginView = new LoginView();
			}
			this.loginView.render();
		}
	});

	return AppRouter;
});