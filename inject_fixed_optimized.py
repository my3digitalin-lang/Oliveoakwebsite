import re

with open(r'c:\tmp\Oliveoakk\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

optimized_js = """let imgs    = new Array(TOTAL);
  let loaded  = 0;
  let targetFrame = 0;   // The frame the user's scroll dictates
  let paintedFrame = -1; // The frame currently drawn on canvas
  let vDelta  = 0;      // virtual scroll delta
  let done    = false;  // hero animation finished
  let busy    = false;  // mid-transition (lock re-entry)

  // Wait until frame is fully decoded before returning it
  async function loadAndDecodeFrame(i) {
    return new Promise((resolve) => {
      const img = new Image();
      img.onload = () => {
        img.decode().then(() => {
          imgs[i-1] = img;
          resolve(img);
        }).catch(() => {
          imgs[i-1] = img;
          resolve(img);
        });
      };
      img.onerror = () => {
        imgs[i-1] = null;
        resolve(null);
      };
      img.src = FP(i);
    });
  }

  async function preload() {
    // Stage 1: Fetch and decode Frame 1 IMMEDIATELY
    const startTime = performance.now();
    await loadAndDecodeFrame(1);
    
    // Resize canvas and paint frame 1
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
    paint(0);
    
    // Stage 2: Buffer frames 2-15 before allowing scroll interaction
    const BUFFER_SIZE = Math.min(15, TOTAL);
    const bufferPromises = [];
    for (let i = 2; i <= BUFFER_SIZE; i++) {
      bufferPromises.push(loadAndDecodeFrame(i));
    }
    
    await Promise.all(bufferPromises);
    
    // Fade out loader
    const loader = document.querySelector('.loader-content');
    if (loader) loader.style.opacity = '0';
    setTimeout(() => {
      const bar = document.getElementById('hero-load-bar');
      if (bar) bar.style.display = 'none';
    }, 500);
    
    // Unlock UI visually
    const tFirstVisible = performance.now() - startTime;
    console.log(`[Perf] First visible frame painted in: ${tFirstVisible.toFixed(2)}ms`);
    
    // Unlock scrolling
    document.body.classList.add('unlocked');
    
    const tInteractive = performance.now() - startTime;
    console.log(`[Perf] Scroll became interactive in: ${tInteractive.toFixed(2)}ms`);
    
    // Stage 3: Sequentially load remaining frames in background
    for (let i = BUFFER_SIZE + 1; i <= TOTAL; i++) {
      if (done) {
        // Option: could stop loading if user skipped hero
      }
      await loadAndDecodeFrame(i);
      
      // If user is waiting for a frame that just loaded, paint it!
      if (targetFrame >= (i - 1) && paintedFrame < (i - 1)) {
        paint(i - 1);
      }
    }
  }

  /* Cache word reveal elements */
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
  const revEls = REVEALS.map(r => ({ node: document.querySelector(r.el), t: r.t }));

  window.addEventListener('resize', () => {
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
    if (paintedFrame !== -1) paint(paintedFrame);
  });

  function paint(i) {
    const img = imgs[i];
    if (!img || !img.naturalWidth) return; // Never paint undecoded/missing frames
    
    const cw=canvas.width, ch=canvas.height, iw=img.naturalWidth, ih=img.naturalHeight;
    const zoom = IS_MOBILE ? 1.15 : 1.0;
    const s = Math.max(cw/iw, ch/ih) * zoom;
    
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';
    ctx.clearRect(0,0,cw,ch);
    ctx.drawImage(img, (cw-iw*s)/2, (ch-ih*s)/2, iw*s, ih*s);
    
    paintedFrame = i;

    // Hide poster once canvas has painted -> seamless handoff
    const poster = document.getElementById('hero-poster');
    if (poster) poster.style.opacity = '0';
  }

  function getHighestAvailableFrame(target) {
    for (let i = target; i >= 0; i--) {
      if (imgs[i]) return i;
    }
    return 0;
  }

  function tick() {
    const t0 = performance.now();
    const p  = Math.min(Math.max(vDelta/RANGE, 0), 1);
    const fi = Math.min(Math.floor(p * TOTAL), TOTAL-1);
    targetFrame = fi;
    
    // Find the closest downloaded frame without flashing blank
    const safeFrame = getHighestAvailableFrame(targetFrame);
    
    if (safeFrame !== paintedFrame) { 
      paint(safeFrame); 
    }

    if (progress) progress.style.width = (p*100) + '%';
    
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
    targetFrame = 0;
    paintedFrame = -1;
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

  // Start the preload sequence immediately
  preload();
"""

# Match the old baseline block to replace it
match = re.search(r'(let imgs\s*=\s*new Array\(TOTAL\);.*?)(/\*\s*==============================================================\s*WHEEL)', html, re.DOTALL)
if match:
    new_html = html[:match.start()] + optimized_js + '\n  ' + html[match.end(2)-80:]
    # Fix the RANGE back to 4000
    new_html = new_html.replace('const RANGE   = IS_MOBILE ? 1800 : 6000;', 'const RANGE   = IS_MOBILE ? 4000 : 6000;')
    with open(r'c:\tmp\Oliveoakk\index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print('Successfully restored the highly optimized progressive load version.')
else:
    print('Failed to match the current script block for replacement.')
