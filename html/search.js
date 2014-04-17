$(document).ready(function() {
	var
	leftDelimiter = String.fromCharCode(128),
	rightDelimiter = String.fromCharCode(129),
	input = $('input'),
	results = $('section#results'),
	dialog = $('div#modal'),
	
	// Return a jQuery object representing a dynamically generated loading image
	ajaxLoader = $('<article>', {
		html: $('<img>', {
			src: 'ajax-loader.gif',
			alt: 'Loading...',
			title: 'Loading...'
		})
	}),
	
	// Perform a search based on input from the text input
	search = function() {
		results.html(ajaxLoader);
		
		$.ajax({
			type: 'POST',
			url: 'search.php',
			dataType: 'json',
			cache: false,
			data: {
				'q': input.val(),
				'action': 'search'
			}
		}).done(function(json) {
			results.html('');
			
			$.each(json, function(i, doc) {
				var article = $('<article>');
				article.append($('<h2>', { html: doc.title }));
				article.append($('<h3>', { html: doc.author }));
				article.append($('<a>', { href: doc.file, html: 'expand' }));
				
				results.append(article);
			});
			
			if (results.find('article').length == 0) {
				results.html('<article><h2>No Results to Display...</h2></article>');
			}
		}).fail(function() {
			results.html('<article><h2>Unable to Connect to Remote Server...</h2></article>');
		});
	};
	
	// Bind the search method for both button click and the enter key press in the search box
	$('section#search').find('button').bind('click', search);
	input.bind('keypress', function(event) {
		if (event.which == 13) {
			event.preventDefault();
			search();
		}
	});
	
	// Bind the expansion element in an article to open a highlighted full text view
	results.on('click', 'a', function() {
		function highlightText(str) {
			var highlightedText = str,
				query = input.val()
					.replace(/(AND|-|OR|NOT|[^\w])/, ' ')
					.replace(/ {2,}/, ' ')
					.split(' ');
			
			$.each(query, function(i, word) {
				highlightedText = highlightedText
					.replace(new RegExp(word, 'gi'), leftDelimiter + word + rightDelimiter);
			});
			
			highlightedText = highlightedText
				.replace(new RegExp(leftDelimiter, 'g'), '<span class="highlight">')
				.replace(new RegExp(rightDelimiter, 'g'), '</span>');
			
			return highlightedText;
		}
		
		$('body').addClass('dialogIsOpen');
		$.ajax({
			type: 'POST',
			url: 'search.php',
			cache: false,
			data: {
				'q': input.val(),
				'action': 'expand',
				'doc': $(this).attr('href')
			}
		}).done(function(response) {
			var html = $(response);
			dialog.find('h2').html(highlightText(html.find('TITLE').html()));
			dialog.find('h3').html(highlightText(html.find('AUTHOR').html()));
			dialog.find('h4').html(highlightText(html.find('BIBLIO').html()));
			dialog.find('p').html(highlightText(html.find('TEXT').html()));
		}).fail(function() {
			
		});
		return false;
	});
	
	dialog.find('button').click(function() {
		$('body').removeClass('dialogIsOpen');
	});
});