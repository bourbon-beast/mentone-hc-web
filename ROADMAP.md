# Mentone Hockey Club — Website Roadmap

Working doc for iterative site development. Strategy: **get live first, then improve in phases.**

Tracking: [Trello board](https://trello.com/b/7p58DMLL/mentone-website) · Platform: [WordPress migration plan](docs/wordpress-migration.md) · Hub: [docs/PROJECT.md](docs/PROJECT.md)

---

## 2026-07 member feedback (3 survey responses — see docs/feedback/2026-07-08-tally.csv)

**Note: responses predate the rebuild (April 2026)** — re-survey after launch. Already answered by the rebuild: awards/trophies (Awards & Records section), training times + contacts (section pages), uniforms page, club history, juniors detail, mobile-friendliness, "home base" IA, click depth.

**Shipped from this feedback (2026-07-08):** Registration & fees explainer with full 2026 fee table + Majestri/HV two-step (`/new-players/#registration`), and the `/resources/` links library (players/parents · managers/volunteers · policies) — interim home for the Phase-2 policy links until the governance section is built.

**Ranked remainder:**
- *Tier 1 (blocked on club input):* season key-dates strip (⚑ start/end, holiday breaks), premierships page (⚑ no real data exists — legacy page was placeholder junk).
- *Tier 2 (content depth):* junior programs beyond H2H (roadshows, Nov/Dec clinic, U8/U10 comp ⚑), RVL explainer + points-jobs list ⚑, governance/policy library (Phase 2), photo/video refresh ⚑, representative players page.
- *Tier 3 (features):* fixtures/upcoming games all sections (parked GCP side project — 2 of 3 respondents want it), social feed embeds, email signup, sponsors showcase, members-only area (team lists, rosters, process docs — needs auth decision; interim channel = news posts + announce bar).
- *Ops, not build:* team vacancies, ball-kid roster, social calendar, big-match promotion.

⚑ also outstanding: should site-wide Register buttons point at Majestri (`mentonehockey.majestri.com.au/2026-winter-season`) instead of revolutionise `club-registrations`?

---

## Phase 0 — Go live (pre-launch blockers)

- [ ] Confirm all pages load without broken links or missing assets
- [ ] Check fixtures data is current for 2026 season
- [ ] Confirm registration links (Revolutionise) are correct and active
- [ ] Review contact details are up to date on all pages
- [ ] Test on mobile (nav, cards, fixtures table)
- [ ] Set up domain / hosting / DNS
- [ ] Smoke test partials.js nav injection on every page

---

## Phase 1 — First iteration (content depth)

*Committee priorities — reduce member questions, improve onboarding.*

**Section pages (Juniors, Women's, Men's, Masters)**
- [x] Add training timetable to each section page *(2026-07-07 — Training block in each section's Get in touch card; source of truth per docs/site-qa-backlog.md)*
- [ ] Add coaches & team managers listing to each section page
- [x] Add section co-ordinator contact to each section page *(2026-07-07 — Get in touch cards)*
- [ ] Add "Come & Try / New Players Wanted" CTA to each section page
- [ ] Juniors: add individual age-group sub-pages (U8, U10, U12, U14, U16, U18)
- [ ] Juniors: add JSC, SSV, HV State Representation info
- [ ] Men's & Women's: add selection policy wording
- [ ] Masters: split into Men's Masters & Women's Masters sub-pages with grade/day/time detail

**New Players / Player Info**
- [x] Add welcome blurb to New Players page *(2026-07-07 — page live with hero, FAQ, section picker, join steps)*
- [ ] Add email signup with topic tick-boxes (juniors, seniors, masters, volunteers, etc.)
- [ ] Add injuries, insurance & first aid section/page
- [x] Add Registration & Fees breakdown (HV fee vs MHC fee) *(2026-07-08 — /new-players/#registration: Majestri + HV two-step, full 2026 fee table, key dates)*

**About section**
- [ ] Add Our People page (committee positions with contact details)
- [ ] Add Our History page (Old Mentonians → Mordialloc Women's Club → Mentone HC)

**News & events**
- [ ] Add club calendar (training schedule, events, social) — separate from fixtures
- [ ] Review/improve news story format

---

## Phase 2 — Heritage & governance

**Club heritage (under About)**
- [ ] Club Premierships page (all grades, all years)
- [ ] Representative Players page (Australian, State, Representative)
- [x] Honours page (Best & Fairest, honour boards) *(2026-07-07 — /history/: 35 honour boards + Best & Fairest + Club Awards)*
- [x] Life Members page *(2026-07-07 — /history/life-members/)*
- [x] Club Song page *(2026-07-07 — /history/club-song/)*

**Governance (new top-level section)**
- [ ] Constitution page (link/embed MHC Club Constitution)
- [ ] By-Laws page
- [ ] Strategy & Annual Reports page
- [ ] Policy library: *(interim: the HA policy set — code of conduct, member protection, safe hockey/concussion/weather — is reachable via the HA hub cards on /resources/ since 2026-07-08; the items below stay open until each gets its own deep link here)*
  - [ ] Child Safety Standards
  - [ ] Volunteer and Employee Policy
  - [ ] Selection Policy (Open Age + Junior)
  - [ ] Fees & Purchases / Refund Policy
  - [ ] Financial Policy
  - [ ] HV Privacy Policy (link)
  - [ ] HV Social Media Policy (link)
  - [ ] HV Inclusion Policy (link)
  - [ ] HA Code of Conduct (link)
  - [ ] HA Member Protection Policy (link)
  - [ ] HA Safe Hockey Policies (link)
  - [ ] HA Weather Policy (link)
  - [ ] HA Concussion Policy (link)
- [ ] Member Protection section (MPIO contacts, Inclusion Policy, Diversity Statement)

---

## Phase 3 — Growth & engagement

**Sponsorship (new top-level section)**
- [ ] Club Sponsorship page
- [ ] Individual Player Sponsorship page
- [ ] Fundraising page (stubby holders, Australian Sports Foundation)
- [ ] Affiliate Programs page (Container Deposit Scheme, Ritchies Community Benefit)

**News & comms**
- [ ] Richer news story template/format
- [ ] Email list integration (tied to signup from Phase 1)

---

## Phase 4 — Lower priority / nice to have

- [ ] Skills & Drills section (drills by age group, drills to practice at home, GK-only section)
- [ ] Coaching Resources hub
- [ ] Team Manager Resources hub
- [ ] Umpire & Officials Resources hub
- [ ] Overseas Players dedicated page
- [ ] School Roadshows info page
- [ ] MHC Summer Series & Indoor Hockey pages

---

## Notes & reference sites

| Site | URL | What it does well |
|------|-----|-------------------|
| Doncaster HC | https://www.doncasterhockeyclub.com.au/ | Governance/resources depth, affiliate programs, Skills & Drills, overseas players, clear "New Players" nav |
| Greensborough HC | https://greensboroughhockeyclub.com.au/start-playing-hockey/ | New player onboarding flow, plain language, progressive commitment (ask a question before registering), knowledge base |
| TEM Hockey | https://www.temhockey.com/club-premierships | Premierships page format |
| Waverley HC | https://waverleyhc.org.au/the-club/representative-players/ | Representative players page |
| MCC Hockey | https://www.mcchockey.org.au/womens/award-recipients/ | Honours/awards page |
| Footscray HC | https://footscrayhockey.com.au/juniors/#summer | Juniors age-group pages (U8, U14 examples) |
| Werribee HC | https://www.werribeehockey.club/sponsors | Sponsors page layout |
| Camberwell HC | https://www.camberwell.hockey/resources | Governance/policies layout |

---

*Last updated: 2026-07-08*
