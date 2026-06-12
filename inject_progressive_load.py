import re
import os

HTML_DIR = r"C:\tmp\Oliveoakk"
index_file = os.path.join(HTML_DIR, 'index.html')

with open(index_file, 'r', encoding='utf-8') as f:
    html = f.read()

# The new JS logic block
new_js = '''let imgs    = new Array(TOTAL);
  let loaded  = 0;
  let targetFrame = 0;   // The frame the user's scroll dictates
  let paintedFrame = -1; // The frame currently drawn on canvas
  let vDelta  = 0;      // virtual scroll delta
  let done    = false;  // hero animation finished
  let busy    = false;  // mid-transition (lock re-entry)

  // Wait until frame is fully decoded before returning it
  async function loadAndDecodeFrame(i) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.src = FP(i);
      img.decode().then(() => {
        imgs[i-1] = img;
        resolve(img);
      }).catch(err => {
        // Fallback if decode() fails (e.g., unsupported or network issue)
        img.onload = () => { imgs[i-1] = img; resolve(img); };
        img.onerror = () => { imgs[i-1] = null; resolve(null); }; // resolve null so sequence continues
      });
    });
  }

  function resize() {
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
    if (paintedFrame >= 0) paint(paintedFrame);
  }

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

    // Hide poster once canvas has painted ?" seamless handoff
    const poster = document.getElementById('hero-poster');
    if (poster) poster.style.opacity = '0';
  }

  /* ==============================================================
     PRELOAD  ?" Progressive decoding
  ============================================================== */
  const heroLoadBar = document.getElementById('hero-load-bar');
  
  function updateLoaderProgress(pct) {
    if (heroLoadBar) {
      heroLoadBar.style.width = pct + '%';
      const pctText = document.getElementById('loader-pct');
      if (pctText) pctText.innerText = pct + '%';
    }
  }

  // 1. Unlock instantly after Frame 1
  function unlockWebsite() {
    const loader = document.getElementById('loader');
    if (loader) loader.classList.add('hidden');
    // We add 'unlocked' later after buffer fills, BUT user sees site immediately
  }

  async function preload() {
    // Stage 1: Fetch and decode Frame 1 IMMEDIATELY
    const startTime = performance.now();
    await loadAndDecodeFrame(1);
    
    // Resize canvas and paint frame 1
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
    paint(0);
    
    // Unlock UI visually
    unlockWebsite();
    updateLoaderProgress(10);
    
    const tFirstVisible = performance.now() - startTime;
    console.log(`[Perf] First visible frame painted in: ${tFirstVisible.toFixed(2)}ms`);

    // Stage 2: Buffer frames 2-15 before allowing scroll interaction
    const BUFFER_SIZE = Math.min(15, TOTAL);
    const bufferPromises = [];
    for (let i = 2; i <= BUFFER_SIZE; i++) {
      bufferPromises.push(loadAndDecodeFrame(i));
    }
    
    await Promise.all(bufferPromises);
    
    // Unlock scrolling
    document.body.classList.add('unlocked');
    updateLoaderProgress(20);
    
    const tInteractive = performance.now() - startTime;
    console.log(`[Perf] Scroll became interactive in: ${tInteractive.toFixed(2)}ms`);

    // Stage 3: Sequentially load remaining frames in background
    for (let i = BUFFER_SIZE + 1; i <= TOTAL; i++) {
      await loadAndDecodeFrame(i);
      
      const pct = Math.round((i / TOTAL) * 100);
      updateLoaderProgress(pct);

      // If user is waiting for a frame that just loaded, paint it!
      if (targetFrame >= (i - 1) && paintedFrame < (i - 1)) {
        paint(i - 1);
      }
    }
    
    // Complete
    if (heroLoadBar) heroLoadBar.style.opacity = '0';
  }

  /* ==============================================================
     TICK   update frame + UI from vDelta
  ============================================================== */
  /* Word reveal schedule: [elementId/class, progress threshold] */
  const REVEALS = [
    { el: '.hero-eyebrow',       t: 0.04 },
    { el: '.hw[data-t="0.05"]', t: 0.05 },
    { el: '.hw[data-t="0.09"]', t: 0.09 },
    { el: '.hw[data-t="0.14"]', t: 0.14 },
    { el: '.hero-divider',       t: 0.20 },
    { el: '.hero-sub',           t: 0.26 },
    { el: '.hero-cta-row',       t: 0.32 },
  ];
  
  /* Cache the DOM elements once */
  const revEls = REVEALS.map(r => ({ node: document.querySelector(r.el), t: r.t }));

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
    
    const renderTime = performance.now() - t0;
    if (renderTime > 16) {
      console.warn(`[Perf] Frame drop: render took ${renderTime.toFixed(2)}ms`);
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
        backHint.classList.add('visible');
        busy = false;
      }, 800);
    }, 150);
  }

  function enterHero() {
    if (busy) return;
    busy = true;

    hero.style.pointerEvents = 'auto';
    main.classList.remove('visible');

    /* Reset to BEGINNING   user scrolls down to replay forward */
    done   = false;
    vDelta = 0;          /* frame 1, p = 0 */
    targetFrame = 0;

    /* Hide scroll-back hint */
    backHint.classList.remove('visible');
    
    /* Clear all word reveals so they animate in fresh */
    revEls.forEach(({ node }) => { if (node) node.classList.remove('show'); });

    /* Reset progress bar and paint frame 1 */
    progress.style.width = '0%';
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

  /* ==============================================================
     WHEEL   drives animation (both directions)
  ============================================================== */
  /* RAF batching   one canvas paint per animation frame */
  '''

# Replace the old JS logic block using regex
# We will match from `let imgs    = new Array(TOTAL);` all the way to the end of `function enterHero()`
# Wait, enterHero is right before `let rafPending = false;`
# Wait, let's just find the exact slice.

match = re.search(r'(let imgs\s*=\s*new Array\(TOTAL\);.*?)(/\*\s*RAF batching)', html, re.DOTALL)
if match:
    html = html[:match.start()] + new_js + html[match.end(2)-18:]
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Injected progressive loading and strict decode logic")
else:
    print("Regex failed to match JS logic block!")
