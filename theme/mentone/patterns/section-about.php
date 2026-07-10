<?php
/**
 * Title: Section about (copy + contact card)
 * Slug: mentone/section-about
 * Categories: mentone
 * Description: Two-column split — section copy on the left, navy get-in-touch card with coordinator and training details on the right.
 */
?>
<!-- wp:group {"metadata":{"name":"About the section"},"style":{"spacing":{"padding":{"top":"var:preset|spacing|90","bottom":"var:preset|spacing|90","left":"var:preset|spacing|50","right":"var:preset|spacing|50"}}},"layout":{"type":"constrained","wideSize":"1240px"}} -->
<div class="wp-block-group" style="padding-top:var(--wp--preset--spacing--90);padding-right:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--90);padding-left:var(--wp--preset--spacing--50)">

	<!-- wp:group {"align":"wide","className":"page-section-split","layout":{"type":"default"}} -->
	<div class="wp-block-group alignwide page-section-split">

		<!-- wp:group {"layout":{"type":"constrained"}} -->
		<div class="wp-block-group">
			<!-- wp:paragraph {"className":"eyebrow"} -->
			<p class="eyebrow">About the section</p>
			<!-- /wp:paragraph -->
			<!-- wp:heading {"className":"section-title"} -->
			<h2 class="wp-block-heading section-title">A heading with <em>brand emphasis.</em></h2>
			<!-- /wp:heading -->
			<!-- wp:paragraph -->
			<p>First paragraph about the section — who plays, what levels, who is welcome.</p>
			<!-- /wp:paragraph -->
			<!-- wp:paragraph -->
			<p>Second paragraph — pathways, competitions, ambitions catered for.</p>
			<!-- /wp:paragraph -->
			<!-- wp:paragraph -->
			<p>Third paragraph — culture, mentoring, community.</p>
			<!-- /wp:paragraph -->
		</div>
		<!-- /wp:group -->

		<!-- wp:html -->
		<div class="info-card-navy">
			<div class="eyebrow" style="margin-bottom:20px;">Get in touch</div>
			<h4 style="margin-bottom:6px;">Coordinator</h4>
			<p style="margin-bottom:16px;">Coordinator name</p>
			<p><a href="mailto:secretary@mentonehockey.org.au">secretary@mentonehockey.org.au</a></p>
			<hr/>
			<div class="eyebrow" style="margin-bottom:16px;">Training</div>
			<p>Tuesday &amp; Thursday nights from <strong>6:30pm</strong><br/>Mentone Hockey Ground</p>
		</div>
		<!-- /wp:html -->
	</div>
	<!-- /wp:group -->
</div>
<!-- /wp:group -->
