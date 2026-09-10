<?php
/**
 * Title: This week (fixtures, training, club rooms)
 * Slug: mentone/this-week
 * Categories: mentone
 * Description: Navy section with two cards — training times and club rooms. The weekend fixtures card was removed 2026-09-10 (it held fabricated sample matches); reinstate it as a dynamic block fed by fixtures.json rather than hand-edited rows.
 */
?>
<!-- wp:group {"metadata":{"name":"This week"},"className":"this-week","backgroundColor":"navy","textColor":"cream","style":{"spacing":{"padding":{"top":"var:preset|spacing|90","bottom":"var:preset|spacing|90","left":"var:preset|spacing|50","right":"var:preset|spacing|50"}}},"layout":{"type":"constrained","wideSize":"1240px"}} -->
<div class="wp-block-group this-week has-cream-color has-navy-background-color has-text-color has-background" style="padding-top:var(--wp--preset--spacing--90);padding-right:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--90);padding-left:var(--wp--preset--spacing--50)">

	<!-- wp:group {"align":"wide","className":"section-head","layout":{"type":"constrained","justifyContent":"left"}} -->
	<div class="wp-block-group alignwide section-head">
		<!-- wp:paragraph {"className":"eyebrow"} -->
		<p class="eyebrow">This Week at Mentone</p>
		<!-- /wp:paragraph -->
		<!-- wp:heading {"className":"section-title"} -->
		<h2 class="wp-block-heading section-title">What's on, <em>when</em>, and who's playing.</h2>
		<!-- /wp:heading -->
	</div>
	<!-- /wp:group -->

	<!-- wp:html -->
	<div class="week-grid week-grid--two alignwide">
		<div class="week-card">
			<div class="week-card-label">Training</div>
			<div class="week-card-title">Turn up, get stuck in</div>
			<p>Seniors train Tuesday and Thursday nights; juniors Tuesday and Thursday from 5pm. Everyone's welcome — grab a stick and come down.</p>
			<a href="/new-players/" class="week-link">Find your section →</a>
		</div>
		<div class="week-card">
			<div class="week-card-label">Club Rooms</div>
			<div class="week-card-title">Post-match &amp; socials</div>
			<p>Club rooms open after every home game. Come down for a drink, a feed, and a bit of a debrief. Best seat in the house for watching the next grade play.</p>
			<a href="/contact" class="week-link">Upcoming events →</a>
		</div>
	</div>
	<!-- /wp:html -->
</div>
<!-- /wp:group -->
