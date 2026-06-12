import re

with open(r'c:\tmp\Oliveoakk\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

original_js = """let imgs    = new Array(TOTAL);
  let loaded  = 0;
  let frame   = 0;
  let vDelta  = 0;      // virtual scroll delta
  let done    = false;  // hero animation finished
  let busy    = false;  // mid-transition (lock re-entry)

  const canvas   = document.getElementById('canvas');
  const ctx      = canvas.getContext('2d');
  const hero     = document.getElementById('hero');
  const heroText = document.getElementById('hero-text');
  const hint     = document.getElementById('scroll-hint');
  const progress = document.getElementById('hero-progress');
  const main     = document.getElementById('main');
  const nav      = document.getElementById('nav');
  const backHint = document.getElementById('back-hint');

  /* Word reveal schedule: [elementId/class, progress threshold] */
  const REVEALS = [
    { el: '.hero-eyebrow',       t: 0.04 },
    { el: '.hw[data-t="0.05"]', t: 0.05 },
    { el: '.hw[data-t="0.10"]', t: 0.10 },
    { el: '.hw[data-t="0.15"]', t: 0.15 },
    { el: '.hw[data-t="0.20"]', t: 0.20 },
    { el: '.hw[data-t="0.25"]', t: 0.25 },
    { el: '.hw[data-t="0.30"]', t: 0.30 },
    { el: '.hero-cta-row',       t: 0.85 }
  ];

  /* Cache the DOM elements once */
  const revEls = REVEALS.map(r => ({ node: document.querySelector(r.el), t: r.t }));

  /* Preload images sequentially */
  for (let i = 1; i <= TOTAL; i++) {
    let img = new Image();
    img.onload = () => {
      imgs[i-1] = img;
      loaded++;
      
      progress.style.width = (loaded / TOTAL * 100) + '%';
      
      if (loaded === TOTAL) {
        /* All loaded -> unlock scrolling and show first frame */
        setTimeout(() => {
          document.body.classList.add('unlocked');
          document.querySelector('.loader-content').style.opacity = '0';
          setTimeout(() => document.getElementById('hero-load-bar').style.display = 'none', 500);
          canvas.width  = window.innerWidth;
          canvas.height = window.innerHeight;
          paint(0);
        }, 500);
      }
    };
    img.src = FP(i);
  }

  /* Handle resize */
  window.addEventListener('resize', () => {
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
    if (imgs[frame]) paint(frame);
  });

  function paint(i) {
    if (!imgs[i]) return;
    const img = imgs[i];
    const cw=canvas.width, ch=canvas.height, iw=img.naturalWidth, ih=img.naturalHeight;
    const zoom = IS_MOBILE ? 1.15 : 1.0;
    const s = Math.max(cw/iw, ch/ih) * zoom;
    
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';
    ctx.clearRect(0,0,cw,ch);
    ctx.drawImage(img, (cw-iw*s)/2, (ch-ih*s)/2, iw*s, ih*s);
    
    // Hide poster once canvas has painted -> seamless handoff
    const poster = document.getElementById('hero-poster');
    if (poster) poster.style.opacity = '0';
  }

  function tick() {
    const p  = Math.min(Math.max(vDelta/RANGE, 0), 1);
    frame = Math.min(Math.floor(p * TOTAL), TOTAL-1);
    
    paint(frame);

    /* Progress bar */
    progress.style.width = (p*100) + '%';
    
    /* Reveal text elements dynamically */
    revEls.forEach(({ node, t }) => {
      if (!node) return;
      if (p > t && !node.classList.contains('show')) {
        node.classList.add('show');
      } else if (p <= t && node.classList.contains('show')) {
        node.classList.remove('show');
      }
    });

    /* Exit Hero Animation Threshold */
    if (p >= 1 && !done && !busy) {
      done = true;
      exitHero();
    }
  }

  function exitHero() {
    busy = true;

    /* Pause on last frame   but cancel if user scrolled back */
    setTimeout(() => {
      if (vDelta < RANGE * 0.98) {   /* user scrolled back during delay */
        busy = false;
        return;
      }
      hero.style.transition = 'opacity .8s var(--ease)';
      hero.style.opacity    = '0';
      
      main.classList.add('visible');
      
      setTimeout(() => {
        hero.style.pointerEvents = 'none';
        if(backHint) backHint.classList.add('visible');
        busy = false;
        document.body.classList.add('unlocked');
      }, 800);
    }, 150);
  }

  function reEnterHero() {
    if (busy) return;
    busy = true;

    if(backHint) backHint.classList.remove('visible');
    main.classList.remove('visible');
    
    hero.style.pointerEvents = 'all';
    hero.style.transition = 'none';
    
    /* Reset to start of hero sequence */
    vDelta = 0;
    frame = 0;
    done = false;
    
    /* Clear all word reveals so they animate in fresh */
    revEls.forEach(({ node }) => { if (node) node.classList.remove('show'); });

    /* Reset progress bar and paint frame 1 */
    if(progress) progress.style.width = '0%';
    paint(0);

    document.body.classList.remove('unlocked');
    document.body.style.overflow = 'hidden';

    requestAnimationFrame(() => {
      hero.style.transition = 'opacity .6s ease';
      hero.style.opacity    = '1';
      
      setTimeout(() => {
        document.body.classList.add('unlocked');
        document.body.style.overflow = '';
        busy = false;
      }, 600);
    });
  }
"""

match = re.search(r'(let imgs\s*=\s*new Array\(TOTAL\);.*?)(/\*\s*RAF batching)', html, re.DOTALL)
if match:
    new_html = html[:match.start()] + original_js + '\n  ' + html[match.end(2)-15:]
    new_html = new_html.replace('const RANGE   = IS_MOBILE ? 4000 : 6000;', 'const RANGE   = IS_MOBILE ? 1800 : 6000;')
    with open(r'c:\tmp\Oliveoakk\index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print('Successfully restored local codebase to match 2sj9vp4hn.')
else:
    print('Failed to match the current script block for replacement.')
