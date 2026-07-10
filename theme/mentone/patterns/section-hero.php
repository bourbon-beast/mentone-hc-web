<?php
/**
 * Title: Section hero (with actions)
 * Slug: mentone/section-hero
 * Categories: mentone
 * Description: Navy section-page hero — display heading with italic emphasis, lead paragraph, register + contact buttons.
 */
?>
<!-- wp:group {"metadata":{"name":"Section hero"},"className":"hero","style":{"spacing":{"padding":{"top":"var:preset|spacing|70","bottom":"var:preset|spacing|80","left":"var:preset|spacing|50","right":"var:preset|spacing|50"}}},"layout":{"type":"constrained","wideSize":"1240px"}} -->
<div class="wp-block-group hero" style="padding-top:var(--wp--preset--spacing--70);padding-right:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--80);padding-left:var(--wp--preset--spacing--50)">
	<!-- wp:group {"align":"wide","layout":{"type":"default"}} -->
	<div class="wp-block-group alignwide">
		<!-- wp:heading {"level":1,"textColor":"cream"} -->
		<h1 class="wp-block-heading has-cream-color has-text-color">Section name with <em>emphasis.</em></h1>
		<!-- /wp:heading -->

		<!-- wp:paragraph {"className":"lead"} -->
		<p class="lead">One or two sentences that set up the section — concrete, warm, plain-spoken.</p>
		<!-- /wp:paragraph -->

		<!-- wp:buttons {"style":{"spacing":{"margin":{"top":"var:preset|spacing|60"}}}} -->
		<div class="wp-block-buttons" style="margin-top:var(--wp--preset--spacing--60)">
			<!-- wp:button -->
			<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="https://www.revolutionise.com.au/mentonehockey/club-registrations">Register for 2026</a></div>
			<!-- /wp:button -->
			<!-- wp:button {"className":"is-style-ghost"} -->
			<div class="wp-block-button is-style-ghost"><a class="wp-block-button__link wp-element-button" href="mailto:secretary@mentonehockey.org.au">Contact the coordinator</a></div>
			<!-- /wp:button -->
		</div>
		<!-- /wp:buttons -->
	</div>
	<!-- /wp:group -->
</div>
<!-- /wp:group -->
