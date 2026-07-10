<?php
/**
 * Title: Competition grid (3 cards)
 * Slug: mentone/comp-grid
 * Categories: mentone
 * Description: Blue-wash band with section head and three competition cards (accent bar, title, blurb).
 */
?>
<!-- wp:group {"metadata":{"name":"Competitions"},"backgroundColor":"blue-wash","style":{"spacing":{"padding":{"top":"var:preset|spacing|90","bottom":"var:preset|spacing|90","left":"var:preset|spacing|50","right":"var:preset|spacing|50"}}},"layout":{"type":"constrained","wideSize":"1240px"}} -->
<div class="wp-block-group has-blue-wash-background-color has-background" style="padding-top:var(--wp--preset--spacing--90);padding-right:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--90);padding-left:var(--wp--preset--spacing--50)">

	<!-- wp:group {"align":"wide","className":"section-head","layout":{"type":"default"}} -->
	<div class="wp-block-group alignwide section-head">
		<!-- wp:paragraph {"className":"eyebrow"} -->
		<p class="eyebrow">Competitions</p>
		<!-- /wp:paragraph -->
		<!-- wp:heading {"className":"section-title"} -->
		<h2 class="wp-block-heading section-title">Teams for <em>every</em> level.</h2>
		<!-- /wp:heading -->
		<!-- wp:paragraph {"className":"section-sub"} -->
		<p class="section-sub">From Premier League through to Metro — find the right grade for where you're at.</p>
		<!-- /wp:paragraph -->
	</div>
	<!-- /wp:group -->

	<!-- wp:html -->
	<div class="comp-grid-3 alignwide">
		<div class="comp-card">
			<div class="comp-card-bar"></div>
			<h4>Premier League</h4>
			<p>The top tier of Hockey Victoria competition.</p>
		</div>
		<div class="comp-card">
			<div class="comp-card-bar"></div>
			<h4>Pennant</h4>
			<p>Strong competition below Premier League with a clear pathway upward.</p>
		</div>
		<div class="comp-card">
			<div class="comp-card-bar"></div>
			<h4>Metro</h4>
			<p>Competitive and social hockey for players at all stages.</p>
		</div>
	</div>
	<!-- /wp:html -->
</div>
<!-- /wp:group -->
