<?php
/**
 * Mentone Hockey Club — block theme setup.
 *
 * Design tokens live in theme.json; behavioural CSS in style.css.
 * Fonts load from Google Fonts for now (same import as the static build) —
 * self-host under assets/fonts/ before launch if we want to drop the dependency.
 */

// Fraunces (display) + Inter (body) — front end and editor iframe.
add_action( 'enqueue_block_assets', function () {
	wp_enqueue_style(
		'mentone-fonts',
		'https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,300;1,9..144,400&family=Inter:wght@400;500;600;700&display=swap',
		array(),
		null
	);
} );

// style.css is not auto-enqueued for block themes — load it on the front end
// and inside the editor so previews match.
add_action( 'wp_enqueue_scripts', function () {
	$ver = wp_get_theme()->get( 'Version' );
	wp_enqueue_style( 'mentone-style', get_stylesheet_uri(), array(), $ver );

	// Honour boards / awards section (history pages). Loaded site-wide: it's
	// ~19KB, cache-friendly, and saves a per-page conditional that breaks the
	// editor preview.
	wp_enqueue_style( 'mentone-club-history', get_theme_file_uri( 'assets/club-history.css' ), array( 'mentone-style' ), $ver );
	wp_enqueue_script( 'mentone-club-history', get_theme_file_uri( 'assets/club-history.js' ), array(), $ver, true );
} );

add_action( 'after_setup_theme', function () {
	add_editor_style( 'style.css' );
} );

add_action( 'init', function () {
	// Keep the pattern inserter focused on our own patterns.
	remove_theme_support( 'core-block-patterns' );

	register_block_pattern_category( 'mentone', array(
		'label' => __( 'Mentone', 'mentone' ),
	) );

	// Button variants from the design system (default button is yellow via theme.json).
	register_block_style( 'core/button', array(
		'name'  => 'navy',
		'label' => __( 'Navy', 'mentone' ),
	) );
	register_block_style( 'core/button', array(
		'name'  => 'ghost',
		'label' => __( 'Ghost (on navy)', 'mentone' ),
	) );
} );
