define([
	'jquery',
	'handlebars',
	'backbone',
	'text!templates/profile_view_template.html'
], function($, Handlebars, Backbone, ProfileViewTemplate) {

	var ProfileView = Backbone.View.extend({

		el: '#app-container',

		initialize: function() {

		},

		events: {

		},

		render: function() {
			var self = this;

			var userDeferred = $.get('/api/user');
			var postsDeferred = $.get('/api/posts')

			$.when(userDeferred, postsDeferred).done(function(userResponse, postResponse) {
				var userData = userResponse[0];
				var postData = postResponse[0];

				if(!userData.success) {
					Backbone.history.navigate('/login', {trigger: true});
					return;
				}

				var templateData = {
					user: userData.data,
					posts: postData
				};

				var compiledTemplate = Handlebars.compile(ProfileViewTemplate);

				var templateHtml = compiledTemplate(templateData);

				self.$el.html(templateHtml);
			});
		}

	});

	return ProfileView;
});