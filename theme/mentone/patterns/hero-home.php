<?php
/**
 * Title: Home hero (mascot + stats)
 * Slug: mentone/hero-home
 * Categories: mentone
 * Description: Navy hero with eyebrow, display heading, lead, buttons, panther mascot stage and four-stat strip.
 */
$mascot = esc_url( get_theme_file_uri( 'assets/images/panther-mascot.png' ) );
?>
<!-- wp:group {"metadata":{"name":"Home hero"},"className":"hero","style":{"spacing":{"padding":{"top":"var:preset|spacing|70","bottom":"var:preset|spacing|80","left":"var:preset|spacing|50","right":"var:preset|spacing|50"}}},"layout":{"type":"constrained","wideSize":"1240px"}} -->
<div class="wp-block-group hero" style="padding-top:var(--wp--preset--spacing--70);padding-right:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--80);padding-left:var(--wp--preset--spacing--50)">

	<!-- wp:columns {"align":"wide","verticalAlignment":"center","style":{"spacing":{"blockGap":{"left":"var:preset|spacing|70"}}}} -->
	<div class="wp-block-columns alignwide are-vertically-aligned-center">
		<!-- wp:column {"verticalAlignment":"center","width":"55%"} -->
		<div class="wp-block-column is-vertically-aligned-center" style="flex-basis:55%">
			<!-- wp:paragraph {"className":"hero-tag"} -->
			<p class="hero-tag">Est. 1976 · Bayside</p>
			<!-- /wp:paragraph -->

			<!-- wp:heading {"level":1} -->
			<h1 class="wp-block-heading">Engage. Inspire. <em>Guide.</em> Develop.</h1>
			<!-- /wp:heading -->

			<!-- wp:paragraph {"className":"lead"} -->
			<p class="lead">A family-friendly hockey club on the Bayside, fielding teams across every level of Hockey Victoria's winter, summer and indoor competitions — including Premier League programs in both Men's and Women's sections.</p>
			<!-- /wp:paragraph -->

			<!-- wp:buttons -->
			<div class="wp-block-buttons">
				<!-- wp:button -->
				<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="https://www.revolutionise.com.au/mentonehockey/club-registrations">Register for 2026</a></div>
				<!-- /wp:button -->
				<!-- wp:button {"className":"is-style-ghost"} -->
				<div class="wp-block-button is-style-ghost"><a class="wp-block-button__link wp-element-button">New to hockey?</a></div>
				<!-- /wp:button -->
			</div>
			<!-- /wp:buttons -->
		</div>
		<!-- /wp:column -->

		<!-- wp:column {"verticalAlignment":"center","width":"45%"} -->
		<div class="wp-block-column is-vertically-aligned-center" style="flex-basis:45%">
			<!-- wp:html -->
			<div class="hero-mascot-stage">
				<div class="hero-mascot-ring"></div>
				<div class="hero-mascot-ring inner"></div>
				<div class="hero-mascot-img"><img src="<?php echo $mascot; ?>" alt="Mentone panther mascot"/></div>
				<div class="hero-mascot-pin">50 years<strong>1976–2026</strong></div>
			</div>
			<!-- /wp:html -->
		</div>
		<!-- /wp:column -->
	</div>
	<!-- /wp:columns -->

	<!-- wp:spacer {"height":"var:preset|spacing|80"} -->
	<div style="height:var(--wp--preset--spacing--80)" aria-hidden="true" class="wp-block-spacer"></div>
	<!-- /wp:spacer -->

	<!-- wp:html -->
	<div class="hero-stats alignwide">
		<div class="stat"><div class="stat-num">50</div><div class="stat-label">Years of hockey</div></div>
		<div class="stat"><div class="stat-num">30+</div><div class="stat-label">Teams fielded</div></div>
		<div class="stat"><div class="stat-num">5</div><div class="stat-label">Sections</div></div>
		<div class="stat"><div class="stat-num">160+</div><div class="stat-label">Junior players</div></div>
	</div>
	<!-- /wp:html -->
</div>
<!-- /wp:group -->
