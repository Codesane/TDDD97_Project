define([
	'jquery',
	'underscore',
	'handlebars',
	'backbone',
	'text!templates/register_view_template.html'
], function($, _, Handlebars, Backbone, RegisterViewTemplate) {
	
	var RegisterView = Backbone.View.extend({

		el: '#welcome-view-container-target',

		initialize: function() {
			_.bindAll(this, 'onSubmitForm');
		},

		events: {
			
		},

		render: function() {

			var registerHtml = $(RegisterViewTemplate);

			registerHtml.hide();
			this.$el.html(registerHtml);

			registerHtml.fadeIn();

			var registerViewForm = this.$el.find('#register-view-form');

			registerViewForm.find('#first_name').focus();

			registerViewForm.validate({
				rules: {
					first_name: 'required',
					family_name: 'required',
					city: 'required',
					country: 'required',
					email: {
						required: true,
						email: true
					},
					password: {
						required: true,
						minlength: 8
					},
					repeat_password: {
						required: true,
						minlength: 8,
						equalTo: '#password'
					}
				},
				messages: {
					password: {
						minlength: 'Your password must contain at least 8 characters.'
					},
					repeat_password: {
						minlength: 'Your password must contain at least 8 characters.',
						equalTo: 'Your passwords do not match.'
					}
				},
				submitHandler: this.onSubmitForm
			});
		},

		onSubmitForm: function(form, e) {
			var self = this;
			e.preventDefault();

			var getValue = function(query) {
				return $(form).find(query).val();
			}

			var signUpData = {
				firstname: 	getValue('#first_name'),
				familyname: getValue('#family_name'),
				gender: 	getValue('#gender'),
				city: 		getValue('#city'),
				country: 	getValue('#country'),
				email: 		getValue('#email'),
				password: 	getValue('#password')
			};

			$.ajax({
				url: '/api/sign_up',
				contentType: 'application/json',
				data: JSON.stringify(signUpData),
				type: 'POST',
				success: function(response) {
					if(response.success) {
						require(['text!templates/register_success_template.html'], function(successTemplate) {
							self.$el.html($(successTemplate));
							setTimeout(function() {
								Backbone.history.navigate('/login', {trigger: true});
							}, 2000);
						});
					} else {
						console.log('Registration failed server-side.');
					}
				}
			});
		}
	});

	return RegisterView;
});






















