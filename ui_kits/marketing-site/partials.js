// Shared chrome + tweaks for the Mentone UI kit
(function(){
  const here = location.pathname.split('/').pop() || 'index.html';

  const NAV_ITEMS = [
    ['mens.html', "Men's"],
    ['womens.html', "Women's"],
    ['juniors.html', 'Juniors'],
    ['masters.html', 'Masters'],
    ['new-players.html', 'New Players'],
    ['fixtures.html', 'Fixtures'],
    ['news.html', 'News'],
    ['contact.html', 'Contact'],
  ];

  const CLUB_REGISTRATIONS_URL = 'https://www.revolutionise.com.au/mentonehockey/club-registrations';

  function injectAnnounce() {
    return `<div class="announce">
      <strong>2026 Season</strong> registrations are now open
      <a href="${CLUB_REGISTRATIONS_URL}" target="_blank" rel="noopener noreferrer">Register now →</a>
    </div>`;
  }

  function brand(isFooter) {
    return `<a href="index.html" class="brand">
      <div class="brand-mark" aria-hidden="true"><img src="../../assets/club-logo.png" alt="" /></div>
      <div class="brand-text">
        <div class="name">Mentone Hockey Club</div>
        <div class="sub">Est. 1976 · Bayside</div>
      </div>
    </a>`;
  }

  function injectNav(active) {
    const links = NAV_ITEMS.map(([href, label]) => {
      const cls = (href === here || active === href) ? ' class="active"' : '';
      return `<li><a href="${href}"${cls}>${label}</a></li>`;
    }).join('');
    return `<nav class="nav"><div class="wrap nav-inner">
      ${brand()}
      <ul class="nav-links">${links}</ul>
      <a href="${CLUB_REGISTRATIONS_URL}" target="_blank" rel="noopener noreferrer" class="nav-cta">Register
        <svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 7h8M7 3l4 4-4 4" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </a>
    </div></nav>`;
  }

  function injectCTA() {
    return `<section class="cta-band">
      <div class="wrap"><div class="cta-band-inner">
        <h3>Ready to grab a stick? <em>Come down</em> — or register online for 2026.</h3>
        <div style="display:flex; gap:14px; flex-wrap:wrap;">
          <a href="${CLUB_REGISTRATIONS_URL}" target="_blank" rel="noopener noreferrer" class="btn btn-primary">Register for 2026</a>
          <a href="contact.html" class="btn btn-ghost">Contact the club</a>
        </div>
      </div></div>
    </section>`;
  }

  function injectFooter() {
    return `<footer><div class="wrap">
      <div class="foot-grid">
        <div class="foot-brand">
          ${brand(true)}
          <p>A family-friendly hockey club on Melbourne's Bayside. Engage, inspire, guide, and develop — every player, every season.</p>
        </div>
        <div class="foot-col">
          <h5>Sections</h5>
          <ul>
            <li><a href="mens.html">Men's</a></li>
            <li><a href="womens.html">Women's</a></li>
            <li><a href="juniors.html">Juniors</a></li>
            <li><a href="masters.html">Masters</a></li>
          </ul>
        </div>
        <div class="foot-col">
          <h5>The Club</h5>
          <ul>
            <li><a href="new-players.html">New Players</a></li>
            <li><a href="fixtures.html">Fixtures &amp; Results</a></li>
            <li><a href="news.html">News</a></li>
            <li><a href="sponsors.html">Sponsors</a></li>
            <li><a href="${CLUB_REGISTRATIONS_URL}" target="_blank" rel="noopener noreferrer">Registration</a></li>
          </ul>
        </div>
        <div class="foot-col">
          <h5>Contact</h5>
          <ul>
            <li><a href="mailto:secretary@mentonehockey.org.au">secretary@mentonehockey.org.au</a></li>
            <li><a href="tel:0413886851">0413 886 851</a></li>
            <li>Mentone Hockey Ground<br/>Mentone, Victoria</li>
          </ul>
        </div>
      </div>
      <div class="acknowledgement">
        Mentone Hockey Club acknowledges the Traditional Owners of the lands on which we play, the Boon Wurrung people of the Kulin Nation, and pays respect to their Elders past, present and emerging.
      </div>
      <div class="foot-bottom">
        <div>© 2026 Mentone Hockey Club. Proudly affiliated with Hockey Victoria.</div>
        <div class="foot-social">
          <a href="#" aria-label="Facebook"><svg viewBox="0 0 14 14" fill="currentColor"><path d="M8.5 14V7.5h2l.3-2.3H8.5V3.7c0-.7.2-1.1 1.1-1.1H11V.6C10.5.5 9.8.5 9.1.5 7.5.5 6.4 1.4 6.4 3.3v1.9H4.5v2.3h1.9V14h2.1z"/></svg></a>
          <a href="https://www.instagram.com/mentone_hc/" target="_blank" rel="noopener noreferrer" aria-label="Instagram"><svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.2"><rect x="1.5" y="1.5" width="11" height="11" rx="3"/><circle cx="7" cy="7" r="2.5"/><circle cx="10.5" cy="3.5" r="0.5" fill="currentColor"/></svg></a>
        </div>
      </div>
    </div></footer>`;
  }

  // Mount chrome
  function mount() {
    const anc = document.getElementById('site-announce');
    if (anc) anc.outerHTML = injectAnnounce();
    const nav = document.getElementById('site-nav');
    if (nav) nav.outerHTML = injectNav();
    const cta = document.getElementById('site-cta');
    if (cta) cta.outerHTML = injectCTA();
    const foot = document.getElementById('site-footer');
    if (foot) foot.outerHTML = injectFooter();
  }

  // ============ TWEAKS ============
  const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
    "vibe": "mascot",
    "hero": "split"
  }/*EDITMODE-END*/;

  let state = { ...TWEAK_DEFAULTS };
  try {
    const saved = JSON.parse(localStorage.getItem('mhc-tweaks') || '{}');
    state = { ...state, ...saved };
  } catch(e){}

  function applyTweaks() {
    document.body.setAttribute('data-vibe', state.vibe);
    document.body.setAttribute('data-hero', state.hero);
    // Update active states in panel
    document.querySelectorAll('.tweak-opt').forEach(b => {
      const group = b.dataset.group;
      b.classList.toggle('active', state[group] === b.dataset.value);
    });
  }

  function setTweak(group, value) {
    state[group] = value;
    localStorage.setItem('mhc-tweaks', JSON.stringify(state));
    applyTweaks();
    try {
      window.parent.postMessage({type:'__edit_mode_set_keys', edits:{[group]: value}}, '*');
    } catch(e){}
  }

  function mountTweaks() {
    const panel = document.createElement('div');
    panel.className = 'tweaks-panel';
    panel.id = 'tweaks-panel';
    panel.innerHTML = `
      <div class="tweaks-head"><h4>Tweaks</h4></div>
      <div class="tweak-group">
        <label>Vibe preset</label>
        <div class="tweak-options">
          <button class="tweak-opt" data-group="vibe" data-value="mascot">Mascot-led · bold &amp; dark</button>
          <button class="tweak-opt" data-group="vibe" data-value="editorial">Editorial · calm &amp; cream</button>
          <button class="tweak-opt" data-group="vibe" data-value="energetic">High-energy · poster-loud</button>
        </div>
      </div>
      <div class="tweak-group">
        <label>Hero layout</label>
        <div class="tweak-options">
          <button class="tweak-opt" data-group="hero" data-value="split">Split · copy + mascot</button>
          <button class="tweak-opt" data-group="hero" data-value="centered">Centered · mascot behind</button>
          <button class="tweak-opt" data-group="hero" data-value="poster">Poster · giant type</button>
        </div>
      </div>`;
    document.body.appendChild(panel);
    panel.querySelectorAll('.tweak-opt').forEach(b => {
      b.addEventListener('click', () => setTweak(b.dataset.group, b.dataset.value));
    });
    applyTweaks();
  }

  // Parent message protocol
  window.addEventListener('message', (e) => {
    const d = e.data || {};
    if (d.type === '__activate_edit_mode') document.getElementById('tweaks-panel')?.classList.add('open');
    else if (d.type === '__deactivate_edit_mode') document.getElementById('tweaks-panel')?.classList.remove('open');
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => { mount(); mountTweaks(); window.parent.postMessage({type:'__edit_mode_available'}, '*'); });
  } else {
    mount(); mountTweaks(); window.parent.postMessage({type:'__edit_mode_available'}, '*');
  }
})();
