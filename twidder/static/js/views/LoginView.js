define([
	'jquery',
	'handlebars',
	'backbone',
	'text!templates/login_view_template.html'
], function($, Handlebars, Backbone, LoginViewTemplate) {
	
	var LoginView = Backbone.View.extend({

		el: '#welcome-view-container-target',

		render: function() {
			var loginHtml = $(LoginViewTemplate);

			loginHtml.hide();
			this.$el.html(loginHtml);
			loginHtml.fadeIn();

			var loginForm = this.$el.find('#login-view-form');

			loginForm.find('#email').focus();

			loginForm.validate({
				rules: {
					email: {
						required: true,
						email: true
					},
					password: {
						required: true,
						minlength: 8
					}
				},
				messages: {
					email: 'Please supply a valid email address.',
					password: {
						minlength: 'Invalid password.'
					}
				},
				submitHandler: this.onSubmitForm
			});
		},

		onSubmitForm: function(form, e) {
			e.preventDefault();
			
			var getValue = function(query) {
				return $(form).find(query).val();
			}


			var loginData = {
				email: getValue('#email'),
				password: getValue('#password')
			};

			$.ajax({
				url: '/api/sign_in',
				contentType: 'application/json',
				data: JSON.stringify(loginData),
				type: 'POST',
				success: function(response) {

					if(response.success) {
						localStorage.setItem('twidder-email', response.data.email);
						localStorage.setItem('twidder-token', response.data.token);
						Backbone.history.navigate('/profile', {trigger: true, replace: true});
					} else {
						// TODO: Handle.
					}
				}
			});
		}

	});

	return LoginView;
});