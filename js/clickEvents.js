window.onload = function() {
			// Show or hide the sticky footer button
			$(window).scroll(function() {
				if ($(this).scrollTop() > 200) {
					$('.backtotop').fadeIn(200);
				} else {
					$('.backtotop').fadeOut(200);
				}
			});

			// Animate the scroll to top
			$('.backtop').click(function(event) {
				event.preventDefault();

				$('html, body').animate({scrollTop: 0}, 300);
			})
		};

function mailSent() {
	alert('Your message is sending. You should see the message in your inbox.');
}

function ifNone() {
	document.write("Sorry, it looks like there are no matches at this point in time :( Please check back later!");

	if (len(clients) == 0) {
		document.write("Sorry, it looks like there are no matches at this point in time :( Please check back later!");
	}
	else {
		document.write(clients);
	}
}
