<?php
/**
 * Title: Awards & records promo
 * Slug: mentone/awards-promo
 * Categories: mentone
 * Description: Navy split — heritage copy and yellow CTA on the left, four stat tiles linking to awards pages on the right.
 */
?>
<!-- wp:group {"metadata":{"name":"Awards & records"},"backgroundColor":"navy","textColor":"cream","style":{"spacing":{"padding":{"top":"var:preset|spacing|80","bottom":"var:preset|spacing|80","left":"var:preset|spacing|50","right":"var:preset|spacing|50"}}},"layout":{"type":"constrained","wideSize":"1240px"}} -->
<div class="wp-block-group has-cream-color has-navy-background-color has-text-color has-background" style="padding-top:var(--wp--preset--spacing--80);padding-right:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--80);padding-left:var(--wp--preset--spacing--50)">

	<!-- wp:columns {"align":"wide","verticalAlignment":"center","className":"awards-split","style":{"spacing":{"blockGap":{"left":"var:preset|spacing|70"}}}} -->
	<div class="wp-block-columns alignwide are-vertically-aligned-center awards-split">
		<!-- wp:column {"verticalAlignment":"center"} -->
		<div class="wp-block-column is-vertically-aligned-center">
			<!-- wp:paragraph {"className":"eyebrow","style":{"elements":{"link":{"color":{"text":"var:preset|color|yellow"}}}},"textColor":"yellow"} -->
			<p class="eyebrow has-yellow-color has-text-color has-link-color">Awards &amp; Records</p>
			<!-- /wp:paragraph -->
			<!-- wp:heading {"textColor":"cream"} -->
			<h2 class="wp-block-heading has-cream-color has-text-color">Life Members. Best &amp; Fairest. <em>Legends.</em></h2>
			<!-- /wp:heading -->
			<!-- wp:paragraph {"textColor":"blue-soft"} -->
			<p class="has-blue-soft-color has-text-color">From life members to Best &amp; Fairest winners and club awards — explore the records behind everyone who's worn the Panther jersey.</p>
			<!-- /wp:paragraph -->
			<!-- wp:buttons -->
			<div class="wp-block-buttons">
				<!-- wp:button -->
				<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="/history">Explore Awards &amp; Records</a></div>
				<!-- /wp:button -->
			</div>
			<!-- /wp:buttons -->
		</div>
		<!-- /wp:column -->

		<!-- wp:column {"verticalAlignment":"center"} -->
		<div class="wp-block-column is-vertically-aligned-center">
			<!-- wp:html -->
			<div class="awards-tiles">
				<a href="/history/life-members" class="awards-tile"><div class="awards-tile-num">20+</div><div class="awards-tile-label">Life Members</div></a>
				<a href="/history/best-and-fairest" class="awards-tile"><div class="awards-tile-num">20</div><div class="awards-tile-label">Best &amp; Fairest</div></a>
				<a href="/history/club-awards" class="awards-tile"><div class="awards-tile-num">35+</div><div class="awards-tile-label">Years of Awards</div></a>
				<a href="/history/25th-anniversary-team" class="awards-tile"><div class="awards-tile-num">2001</div><div class="awards-tile-label">Anniversary Team</div></a>
			</div>
			<!-- /wp:html -->
		</div>
		<!-- /wp:column -->
	</div>
	<!-- /wp:columns -->
</div>
<!-- /wp:group -->
