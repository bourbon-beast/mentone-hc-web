<?php
/**
 * Title: Page hero (inner pages)
 * Slug: mentone/page-hero
 * Categories: mentone
 * Description: Navy inner-page hero with eyebrow, display heading with italic emphasis, and lead paragraph.
 */
?>
<!-- wp:group {"metadata":{"name":"Page hero"},"className":"hero","style":{"spacing":{"padding":{"top":"var:preset|spacing|70","bottom":"var:preset|spacing|80","left":"var:preset|spacing|50","right":"var:preset|spacing|50"}}},"layout":{"type":"constrained","wideSize":"1240px"}} -->
<div class="wp-block-group hero" style="padding-top:var(--wp--preset--spacing--70);padding-right:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--80);padding-left:var(--wp--preset--spacing--50)">
	<!-- wp:group {"align":"wide","layout":{"type":"default"}} -->
	<div class="wp-block-group alignwide">
		<!-- wp:paragraph {"className":"hero-tag"} -->
		<p class="hero-tag">Section name</p>
		<!-- /wp:paragraph -->

		<!-- wp:heading {"level":1,"textColor":"cream"} -->
		<h1 class="wp-block-heading has-cream-color has-text-color">Page title with <em>emphasis.</em></h1>
		<!-- /wp:heading -->

		<!-- wp:paragraph {"className":"lead"} -->
		<p class="lead">One or two sentences that set up the page — concrete, warm, plain-spoken.</p>
		<!-- /wp:paragraph -->
	</div>
	<!-- /wp:group -->
</div>
<!-- /wp:group -->
