$(document).ready(function() {
	var
	query,
	results = $("section#results"),
	
	// Return a jQuery object representing a dynamically generating loading image
	ajaxLoader = function(props) {
		props = $.extend({
			src: 'ajax-loader.gif',
			alt: 'Loading...',
			title: 'Loading...'
		}, props);
		return $('<img>', props);
	},
	
	// Perform a search based on input from the text input
	search = function() {
		query = $('input').val();
		results.html(ajaxLoader());
		
		$.ajax({
			type: 'POST',
			url: 'search.php',
			dataType: 'json',
			cache: false,
			data: {
				'q': query,
				'action': 'search'
			}
		}).done(function(json) {
			console.log(json);
			
			if (json.length == 0) {
				results.html('<h2>No Results to Display</h2>');
			}
			else {
				results.html('');
				$.each(json, function(i, doc) {
					var article = $('<article>', { 'data-file': doc.file });
					article.append($('<h2>', { html: doc.title }));
					article.append($('<h3>', { html: doc.author }));
					article.append($('<a>', { href: '#', html: 'expand' }));
					results.append(article);
				});
			}
		}).fail(function() {
			console.log('Connection Failure');
			results.html('<h2>No Results to Display</h2>');
		});
		
	};
	
	// Bind the search method for both button click and the enter key press in the search box
	$('button').bind('click', search);
	$('input').bind('keypress', function(event) {
		if (event.which == 13) {
			event.preventDefault();
			search();
		}
	});
	
	// Bind the expansion element in an article to open a highlighted full text view
	results.on('click', 'a', function() {
		console.log('show file: ' + $(this).closest('article').attr('data-file'));
		return false;
	});
});