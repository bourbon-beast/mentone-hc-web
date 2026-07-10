# Mentone HC Website — Project Hub

Quick orientation for anyone (or any Claude session) landing in this repo.

## The three places

| Place | Carries | Link |
|---|---|---|
| **This repo** | Code, design system, build backlog, migration plan | [ROADMAP.md](../ROADMAP.md) · [docs/wordpress-migration.md](wordpress-migration.md) · [README.md](../README.md) (design system) |
| **Obsidian vault** | Why, decisions, open questions, session logs | `Obsidian/Projects/Side Projects/Mentone Website.md` |
| **Trello** | Day-to-day to-dos, in-progress tracking | [trello.com/b/7p58DMLL](https://trello.com/b/7p58DMLL/mentone-website) |

Rule of thumb: decisions get recorded in the vault page, work items live on Trello, and anything structural (phases, migration steps) stays in this repo's markdown so it travels with the code.

## Current state (2026-07-06)

- Redesign built as static HTML/CSS; design system complete and tokenized (`colors_and_type.css`)
- Replaces the club's **existing WordPress site** — the static build is the design spec, WordPress is the destination. No hard deadline.
- **Decision:** custom block theme (not a page builder) — see [wordpress-migration.md](wordpress-migration.md)
- Next up: audit the old WP site (access, plugins, content worth keeping), then start the theme skeleton

## Suggested Trello lists

To mirror the roadmap: `Backlog` · `Phase 0 — Go live` · `WordPress migration` · `Doing` · `Done`. Cards for content phases 1–4 can sit in Backlog and be pulled forward.
