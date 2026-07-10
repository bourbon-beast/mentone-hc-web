<?php
/**
 * Title: Section culture (navy split + tiles)
 * Slug: mentone/section-culture
 * Categories: mentone
 * Description: Navy band — club-culture copy on the left, 2×2 grid of social-event tiles on the right.
 */
?>
<!-- wp:group {"metadata":{"name":"Off the field"},"backgroundColor":"navy","style":{"spacing":{"padding":{"top":"var:preset|spacing|90","bottom":"var:preset|spacing|90","left":"var:preset|spacing|50","right":"var:preset|spacing|50"}}},"layout":{"type":"constrained","wideSize":"1240px"}} -->
<div class="wp-block-group has-navy-background-color has-background" style="padding-top:var(--wp--preset--spacing--90);padding-right:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--90);padding-left:var(--wp--preset--spacing--50)">

	<!-- wp:group {"align":"wide","className":"page-section-split page-section-split--center","layout":{"type":"default"}} -->
	<div class="wp-block-group alignwide page-section-split page-section-split--center">

		<!-- wp:group {"layout":{"type":"constrained"}} -->
		<div class="wp-block-group">
			<!-- wp:paragraph {"className":"eyebrow"} -->
			<p class="eyebrow">Off the field</p>
			<!-- /wp:paragraph -->
			<!-- wp:heading {"className":"section-title","textColor":"cream"} -->
			<h2 class="wp-block-heading section-title has-cream-color has-text-color">More than just <em>the hockey.</em></h2>
			<!-- /wp:heading -->
			<!-- wp:paragraph {"style":{"color":{"text":"rgba(246,241,230,0.75)"}}} -->
			<p class="has-text-color" style="color:rgba(246,241,230,0.75)">First paragraph about the social side of the section.</p>
			<!-- /wp:paragraph -->
			<!-- wp:paragraph {"style":{"color":{"text":"rgba(246,241,230,0.75)"}}} -->
			<p class="has-text-color" style="color:rgba(246,241,230,0.75)">Second paragraph — club rooms, events, belonging.</p>
			<!-- /wp:paragraph -->
		</div>
		<!-- /wp:group -->

		<!-- wp:html -->
		<div class="off-field-mini-grid">
			<div class="mini-tile">
				<div class="mini-tile-word">BBQs</div>
				<div class="mini-tile-label">After every home game</div>
			</div>
			<div class="mini-tile">
				<div class="mini-tile-word">Trips</div>
				<div class="mini-tile-label">Annual club events</div>
			</div>
			<div class="mini-tile">
				<div class="mini-tile-word">Trivia</div>
				<div class="mini-tile-label">Club nights</div>
			</div>
			<div class="mini-tile">
				<div class="mini-tile-word">Pres.</div>
				<div class="mini-tile-label">Presentation night</div>
			</div>
		</div>
		<!-- /wp:html -->
	</div>
	<!-- /wp:group -->
</div>
<!-- /wp:group -->
