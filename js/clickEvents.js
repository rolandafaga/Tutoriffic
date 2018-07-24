console.log("work?")
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
