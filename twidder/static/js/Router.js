define([
	'backbone',
	'views/WelcomeView',
	'views/RegisterView',
	'views/LoginView',
	'views/ProfileView'
], function(Backbone, WelcomeView, RegisterView, LoginView, ProfileView) {

	var AppRouter = Backbone.Router.extend({

		initialize: function() {
			this.welcomeView = new WelcomeView();
		},

		routes: {
			'': 'register',
			'login': 'login',
			'register': 'register',
			'profile': 'profile'
		},

		register: function() {
			this.welcomeView.render({
				page: 'register'
			});
		},

		login: function() {
			this.welcomeView.render({
				page: 'login'
			});
		},

		profile: function() {
			var profileView = new ProfileView();
			profileView.render();
		}

	});

	return AppRouter;
});