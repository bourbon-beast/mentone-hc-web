<?php
/**
 * Title: Age group grid (4 tiles)
 * Slug: mentone/age-grid
 * Categories: mentone
 * Description: Blue-wash band with section head and four centred age-group tiles (display number, label, blurb).
 */
?>
<!-- wp:group {"metadata":{"name":"Age groups"},"backgroundColor":"blue-wash","style":{"spacing":{"padding":{"top":"var:preset|spacing|90","bottom":"var:preset|spacing|90","left":"var:preset|spacing|50","right":"var:preset|spacing|50"}}},"layout":{"type":"constrained","wideSize":"1240px"}} -->
<div class="wp-block-group has-blue-wash-background-color has-background" style="padding-top:var(--wp--preset--spacing--90);padding-right:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--90);padding-left:var(--wp--preset--spacing--50)">

	<!-- wp:group {"align":"wide","className":"section-head","layout":{"type":"default"}} -->
	<div class="wp-block-group alignwide section-head">
		<!-- wp:paragraph {"className":"eyebrow"} -->
		<p class="eyebrow">Age groups</p>
		<!-- /wp:paragraph -->
		<!-- wp:heading {"className":"section-title"} -->
		<h2 class="wp-block-heading section-title">A team for <em>every age.</em></h2>
		<!-- /wp:heading -->
		<!-- wp:paragraph {"className":"section-sub"} -->
		<p class="section-sub">We field junior teams across a full range of Hockey Victoria age-group competitions.</p>
		<!-- /wp:paragraph -->
	</div>
	<!-- /wp:group -->

	<!-- wp:html -->
	<div class="age-grid-4 alignwide">
		<div class="age-card">
			<div class="age-card-num">5–10</div>
			<div class="age-card-label">Hook in2</div>
			<p>Thursday afternoons. No experience needed — just turn up.</p>
		</div>
		<div class="age-card">
			<div class="age-card-num">U8 · U10</div>
			<div class="age-card-label">Mini Hockey</div>
			<p>Small-sided games introducing core skills and love of the game.</p>
		</div>
		<div class="age-card">
			<div class="age-card-num">U12 · U14</div>
			<div class="age-card-label">Juniors</div>
			<p>Full competition hockey with a focus on individual and team development.</p>
		</div>
		<div class="age-card">
			<div class="age-card-num">U16 · U18</div>
			<div class="age-card-label">Juniors</div>
			<p>Pathway to senior hockey. Senior players actively mentor this group.</p>
		</div>
	</div>
	<!-- /wp:html -->
</div>
<!-- /wp:group -->
