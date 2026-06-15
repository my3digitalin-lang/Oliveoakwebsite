import re

def update_services():
    with open('c:\\tmp\\Oliveoakk\\index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the <section id="services"> block
    # It ends before the next <div class="gold-line"></div>
    # Let's use regex
    
    pattern = re.compile(r'(<section id="services">.*?</section>)', re.DOTALL)
    match = pattern.search(html)
    
    if not match:
        print("Could not find services section")
        return
        
    old_services = match.group(1)
    
    new_services = """<style>
  .svc-new-section {
    padding: 120px 60px;
    max-width: 1400px;
    margin: 0 auto;
    position: relative;
  }
  .svc-new-header {
    text-align: center;
    margin-bottom: 80px;
  }
  .svc-new-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
  }
  .svc-new-card {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    aspect-ratio: 3/4;
    display: flex;
    align-items: flex-end;
    text-decoration: none;
    background: var(--bg2);
    border: 1px solid rgba(200,169,126,0.1);
    transform: translateY(0);
    transition: transform 0.4s ease, border-color 0.4s ease;
  }
  .svc-new-card:hover {
    transform: translateY(-8px);
    border-color: rgba(200,169,126,0.4);
  }
  .svc-new-img {
    position: absolute;
    inset: 0;
    z-index: 1;
  }
  .svc-new-img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(0.6) saturate(0.8);
    transition: transform 0.7s cubic-bezier(0.19, 1, 0.22, 1), filter 0.7s;
  }
  .svc-new-card:hover .svc-new-img img {
    transform: scale(1.08);
    filter: brightness(0.3) saturate(1);
  }
  .svc-new-content {
    position: relative;
    z-index: 2;
    padding: 32px 24px;
    width: 100%;
    background: linear-gradient(to top, rgba(8,7,6,0.95), rgba(8,7,6,0.5) 70%, transparent);
    transition: transform 0.5s cubic-bezier(0.19, 1, 0.22, 1);
  }
  .svc-new-title {
    font-family: var(--f-display);
    font-size: 22px;
    color: var(--white);
    margin-bottom: 8px;
    line-height: 1.2;
    transition: transform 0.4s;
  }
  .svc-new-desc {
    font-family: var(--f-body);
    font-size: 13px;
    font-weight: 300;
    line-height: 1.6;
    color: rgba(255,255,255,0.7);
    opacity: 0;
    max-height: 0;
    overflow: hidden;
    transition: opacity 0.4s, max-height 0.4s;
  }
  .svc-new-card:hover .svc-new-desc {
    opacity: 1;
    max-height: 120px;
    margin-bottom: 16px;
    margin-top: 12px;
  }
  .svc-new-explore {
    font-family: var(--f-body);
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--gold);
    display: flex;
    align-items: center;
    gap: 8px;
    opacity: 0;
    transform: translateY(10px);
    transition: opacity 0.4s 0.1s, transform 0.4s 0.1s;
  }
  .svc-new-card:hover .svc-new-explore {
    opacity: 1;
    transform: none;
  }

  @media (max-width: 1100px) {
    .svc-new-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }
  @media (max-width: 900px) {
    .svc-new-grid {
      grid-template-columns: repeat(2, 1fr);
    }
    .svc-new-section {
      padding: 80px 24px;
    }
    .svc-new-card {
        aspect-ratio: 4/5;
    }
    .svc-new-desc {
        opacity: 1;
        max-height: 100px;
        margin-top: 8px;
        margin-bottom: 16px;
        font-size: 12px;
    }
    .svc-new-explore {
        opacity: 1;
        transform: none;
    }
    .svc-new-img img {
        filter: brightness(0.4) saturate(0.8);
    }
  }
  @media (max-width: 600px) {
    .svc-new-grid {
      grid-template-columns: 1fr;
    }
    .svc-new-card {
        aspect-ratio: 16/9;
    }
  }
</style>

<section id="services" class="svc-new-section">
  <div class="svc-new-header reveal">
    <span class="label">Our Services</span>
    <h2 class="display-h" style="margin-top: 16px;">Curated for Every<br><em>Space & Vision</em></h2>
  </div>

  <div class="svc-new-grid">
    <a href="services.html" class="svc-new-card reveal">
      <div class="svc-new-img">
        <img src="https://images.unsplash.com/photo-1503174971373-b1f69850bded?auto=format&fit=crop&w=1000&q=80" alt="Turnkey" loading="lazy">
      </div>
      <div class="svc-new-content">
        <h3 class="svc-new-title">Complete Turnkey Projects</h3>
        <p class="svc-new-desc">From concept to completion we manage every detail of your project so you can move in without the stress.</p>
        <span class="svc-new-explore">Explore <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg></span>
      </div>
    </a>

    <a href="services.html" class="svc-new-card reveal">
      <div class="svc-new-img">
        <img src="https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1000&q=80" alt="Residential" loading="lazy">
      </div>
      <div class="svc-new-content">
        <h3 class="svc-new-title">Residential Interiors</h3>
        <p class="svc-new-desc">Elegant, functional home interiors crafted around your lifestyle from apartments to independent villas.</p>
        <span class="svc-new-explore">Explore <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg></span>
      </div>
    </a>

    <a href="services.html" class="svc-new-card reveal">
      <div class="svc-new-img">
        <img src="https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1000&q=80" alt="Commercial" loading="lazy">
      </div>
      <div class="svc-new-content">
        <h3 class="svc-new-title">Commercial Interiors</h3>
        <p class="svc-new-desc">Inspiring workspaces, retail environments, and hospitality interiors that reflect your brand.</p>
        <span class="svc-new-explore">Explore <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg></span>
      </div>
    </a>

    <a href="services.html" class="svc-new-card reveal">
      <div class="svc-new-img">
        <img src="https://images.unsplash.com/photo-1600121848594-d8644e57abab?auto=format&fit=crop&w=1000&q=80" alt="Premium Living" loading="lazy">
      </div>
      <div class="svc-new-content">
        <h3 class="svc-new-title">Premium Living Interiors</h3>
        <p class="svc-new-desc">Luxury finishes, bespoke furniture, and curated aesthetics designed for those who expect the extraordinary.</p>
        <span class="svc-new-explore">Explore <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg></span>
      </div>
    </a>

    <a href="services.html" class="svc-new-card reveal">
      <div class="svc-new-img">
        <img src="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=1000&q=80" alt="Design Services" loading="lazy">
      </div>
      <div class="svc-new-content">
        <h3 class="svc-new-title">Design Services</h3>
        <p class="svc-new-desc">Full-spectrum interior design: concept development, mood boards, material selection, and 3D visualization.</p>
        <span class="svc-new-explore">Explore <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg></span>
      </div>
    </a>

    <a href="services.html" class="svc-new-card reveal">
      <div class="svc-new-img">
        <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=1000&q=80" alt="Consultation" loading="lazy">
      </div>
      <div class="svc-new-content">
        <h3 class="svc-new-title">Design Consultation</h3>
        <p class="svc-new-desc">One-on-one sessions with our expert designers to clarify your vision and explore possibilities.</p>
        <span class="svc-new-explore">Explore <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg></span>
      </div>
    </a>

    <a href="services.html" class="svc-new-card reveal">
      <div class="svc-new-img">
        <img src="https://images.unsplash.com/photo-1600210492493-0946911123ea?auto=format&fit=crop&w=1000&q=80" alt="Space Planning" loading="lazy">
      </div>
      <div class="svc-new-content">
        <h3 class="svc-new-title">Space Planning</h3>
        <p class="svc-new-desc">Intelligent layouts that maximise flow, natural light, and usability, making every square foot work beautifully.</p>
        <span class="svc-new-explore">Explore <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg></span>
      </div>
    </a>

    <a href="services.html" class="svc-new-card reveal">
      <div class="svc-new-img">
        <img src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=1000&q=80" alt="Quality" loading="lazy">
      </div>
      <div class="svc-new-content">
        <h3 class="svc-new-title">Quality Consultation</h3>
        <p class="svc-new-desc">Rigorous material and finish evaluation ensuring every element meets our premium standards.</p>
        <span class="svc-new-explore">Explore <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg></span>
      </div>
    </a>
  </div>
</section>"""

    html = html.replace(old_services, new_services)
    
    # Remove GSAP ScrollTrigger for services if it exists
    gsap_pattern = re.compile(r'\s*// ScrollTrigger for Services images.*?(?=\n\s*// Parallax for hero|\n\s*// Reveal on scroll|\n\s*// CTA parallax|\n\s*</script>)', re.DOTALL)
    html = gsap_pattern.sub('', html)
    
    # Also another ScrollTrigger pattern that might be there
    gsap_pattern2 = re.compile(r'\s*ScrollTrigger\.create\(\{[\s\S]*?trigger:\s*\'\.svc-wrap\'[\s\S]*?\}\);', re.DOTALL)
    html = gsap_pattern2.sub('', html)
    
    with open('c:\\tmp\\Oliveoakk\\index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Services section completely redesigned in index.html")

update_services()
