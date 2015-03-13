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
			'click #user-post-message': 'postMessage',
			'keyup #user-post-content': 'onMessageChange'
		},

		render: function() {
			var self = this;

			var userDeferred = $.get('/api/user');
			var postsDeferred = $.get('/api/posts');

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
			}).fail(function() {
				Backbone.history.navigate('/login', {trigger: true, replace: true});
			});
		},

		postMessage: function() {
			var self = this;
			
			var messageBox = this.$el.find('#user-post-content');

			var message = messageBox.val();
			if(message.lenght == 0) return;
			messageBox.val('');
			
			// /api/post
			$.ajax({
				url: '/api/post',
				contentType: 'application/json',
				data: JSON.stringify({
					message: message
				}),
				type: 'POST',
				success: function(response) {
					if(response.success) {
						
					} else {
						console.log('Post failed.');
					}
					self.$el.find('#user-post-message').prop('disabled', true);
				}
			});
		},

		onMessageChange: function() {
			this.$el.find('#user-post-message').prop('disabled', 
				this.$el.find('#user-post-content').val().length === 0
			);
		}
	});
	return ProfileView;
});