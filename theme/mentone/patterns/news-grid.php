<?php
/**
 * Title: Club news grid
 * Slug: mentone/news-grid
 * Categories: mentone
 * Description: Blue-wash section pulling the three latest posts as news cards with category pill, date, title and excerpt.
 */
?>
<!-- wp:group {"metadata":{"name":"Club news"},"backgroundColor":"blue-wash","style":{"spacing":{"padding":{"top":"var:preset|spacing|90","bottom":"var:preset|spacing|90","left":"var:preset|spacing|50","right":"var:preset|spacing|50"}}},"layout":{"type":"constrained","wideSize":"1240px"}} -->
<div class="wp-block-group has-blue-wash-background-color has-background" style="padding-top:var(--wp--preset--spacing--90);padding-right:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--90);padding-left:var(--wp--preset--spacing--50)">

	<!-- wp:group {"align":"wide","layout":{"type":"flex","flexWrap":"wrap","justifyContent":"space-between","verticalAlignment":"bottom"}} -->
	<div class="wp-block-group alignwide">
		<!-- wp:group {"className":"section-head","style":{"spacing":{"margin":{"bottom":"0"}}},"layout":{"type":"constrained","justifyContent":"left"}} -->
		<div class="wp-block-group section-head" style="margin-bottom:0">
			<!-- wp:paragraph {"className":"eyebrow"} -->
			<p class="eyebrow">Club News</p>
			<!-- /wp:paragraph -->
			<!-- wp:heading {"className":"section-title"} -->
			<h2 class="wp-block-heading section-title">Wins, milestones &amp; <em>moments.</em></h2>
			<!-- /wp:heading -->
		</div>
		<!-- /wp:group -->
		<!-- wp:buttons -->
		<div class="wp-block-buttons">
			<!-- wp:button {"className":"is-style-navy"} -->
			<div class="wp-block-button is-style-navy"><a class="wp-block-button__link wp-element-button" href="/news">All news</a></div>
			<!-- /wp:button -->
		</div>
		<!-- /wp:buttons -->
	</div>
	<!-- /wp:group -->

	<!-- wp:spacer {"height":"var:preset|spacing|70"} -->
	<div style="height:var(--wp--preset--spacing--70)" aria-hidden="true" class="wp-block-spacer"></div>
	<!-- /wp:spacer -->

	<!-- wp:query {"query":{"perPage":3,"postType":"post","order":"desc","orderBy":"date"},"align":"wide"} -->
	<div class="wp-block-query alignwide">
		<!-- wp:post-template {"layout":{"type":"grid","columnCount":3}} -->
			<!-- wp:group {"className":"news-card mentone-card","backgroundColor":"white","style":{"border":{"radius":"4px"},"spacing":{"blockGap":"0"}},"layout":{"type":"constrained"}} -->
			<div class="wp-block-group news-card mentone-card has-white-background-color has-background" style="border-radius:4px">
				<!-- wp:post-featured-image {"aspectRatio":"3/2","isLink":true} /-->
				<!-- wp:group {"style":{"spacing":{"padding":{"top":"var:preset|spacing|40","bottom":"var:preset|spacing|40","left":"var:preset|spacing|40","right":"var:preset|spacing|40"}}},"layout":{"type":"constrained"}} -->
				<div class="wp-block-group" style="padding-top:var(--wp--preset--spacing--40);padding-right:var(--wp--preset--spacing--40);padding-bottom:var(--wp--preset--spacing--40);padding-left:var(--wp--preset--spacing--40)">
					<!-- wp:post-date {"fontSize":"small","textColor":"muted"} /-->
					<!-- wp:post-title {"isLink":true,"className":"news-title","fontSize":"large"} /-->
					<!-- wp:post-excerpt {"excerptLength":22,"className":"news-excerpt"} /-->
				</div>
				<!-- /wp:group -->
			</div>
			<!-- /wp:group -->
		<!-- /wp:post-template -->
	</div>
	<!-- /wp:query -->
</div>
<!-- /wp:group -->
