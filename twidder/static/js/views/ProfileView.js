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
			var compiledTemplate = Handlebars.compile(ProfileViewTemplate);

			var templateHtml = compiledTemplate();

			this.$el.html(templateHtml);
		}

	});

	return ProfileView;
});