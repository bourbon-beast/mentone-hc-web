<?php
/**
 * Title: Section team cards
 * Slug: mentone/team-cards
 * Categories: mentone
 * Description: Four-up team cards (Men's, Women's, Juniors, Masters) with gradient backgrounds and hover arrows. Add photos by setting a background-image on each card's team-card-bg div.
 */
?>
<!-- wp:group {"metadata":{"name":"Our sections"},"backgroundColor":"cream","style":{"spacing":{"padding":{"top":"var:preset|spacing|90","bottom":"var:preset|spacing|90","left":"var:preset|spacing|50","right":"var:preset|spacing|50"}}},"layout":{"type":"constrained","wideSize":"1240px"}} -->
<div class="wp-block-group has-cream-background-color has-background" style="padding-top:var(--wp--preset--spacing--90);padding-right:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--90);padding-left:var(--wp--preset--spacing--50)">

	<!-- wp:group {"align":"wide","className":"section-head","layout":{"type":"constrained","justifyContent":"left"}} -->
	<div class="wp-block-group alignwide section-head">
		<!-- wp:paragraph {"className":"eyebrow"} -->
		<p class="eyebrow">Our Sections</p>
		<!-- /wp:paragraph -->
		<!-- wp:heading {"className":"section-title"} -->
		<h2 class="wp-block-heading section-title">A team for <em>every</em> player, at every stage.</h2>
		<!-- /wp:heading -->
		<!-- wp:paragraph {"className":"section-sub"} -->
		<p class="section-sub">From kids picking up a stick for the first time, through to Premier League — find your place at Mentone.</p>
		<!-- /wp:paragraph -->
	</div>
	<!-- /wp:group -->

	<!-- wp:html -->
	<div class="sections-grid alignwide">
		<a href="/mens" class="team-card" data-team="mens">
			<div class="team-card-bg"></div>
			<div class="team-card-inner"><div><div class="team-card-name">Men's</div><div class="team-count">Premier League → Metro</div></div></div>
			<div class="team-card-arrow"><svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 7h8M7 3l4 4-4 4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
		</a>
		<a href="/womens" class="team-card" data-team="womens">
			<div class="team-card-bg"></div>
			<div class="team-card-inner"><div><div class="team-card-name">Women's</div><div class="team-count">Premier League → Metro</div></div></div>
			<div class="team-card-arrow"><svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 7h8M7 3l4 4-4 4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
		</a>
		<a href="/juniors" class="team-card" data-team="juniors">
			<div class="team-card-bg"></div>
			<div class="team-card-inner"><div><div class="team-card-name">Juniors</div><div class="team-count">Hook in2 → U18</div></div></div>
			<div class="team-card-arrow"><svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 7h8M7 3l4 4-4 4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
		</a>
		<a href="/masters" class="team-card" data-team="masters">
			<div class="team-card-bg"></div>
			<div class="team-card-inner"><div><div class="team-card-name">Masters</div><div class="team-count">Men's &amp; Women's</div></div></div>
			<div class="team-card-arrow"><svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 7h8M7 3l4 4-4 4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
		</a>
	</div>
	<!-- /wp:html -->
</div>
<!-- /wp:group -->
