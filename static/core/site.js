(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const progress = document.querySelector('.scroll-progress span');
  const header = document.querySelector('.site-header');
  const globalBinaryCursor = document.querySelector('.global-binary-cursor');

  // A lightweight 10101 label follows the pointer across every page.
  // It remains hidden until pointer movement and is disabled for touch/reduced motion.
  if (globalBinaryCursor && !reduceMotion && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    let cursorX = 0, cursorY = 0, currentX = 0, currentY = 0, cursorFrame = 0;
    const animateGlobalCursor = () => {
      currentX += (cursorX - currentX) * 0.18;
      currentY += (cursorY - currentY) * 0.18;
      globalBinaryCursor.style.transform = `translate3d(${currentX + 16}px, ${currentY + 18}px, 0)`;
      if (Math.abs(cursorX - currentX) > 0.4 || Math.abs(cursorY - currentY) > 0.4) {
        cursorFrame = window.requestAnimationFrame(animateGlobalCursor);
      } else {
        cursorFrame = 0;
      }
    };
    window.addEventListener('pointermove', event => {
      if (event.pointerType !== 'mouse' && event.pointerType !== 'pen') return;
      cursorX = event.clientX;
      cursorY = event.clientY;
      globalBinaryCursor.classList.add('is-visible');
      if (!cursorFrame) cursorFrame = window.requestAnimationFrame(animateGlobalCursor);
    }, { passive: true });
    document.documentElement.addEventListener('pointerleave', () => globalBinaryCursor.classList.remove('is-visible'));
    document.addEventListener('pointerdown', () => globalBinaryCursor.classList.remove('is-visible'));
    document.addEventListener('pointerup', () => globalBinaryCursor.classList.add('is-visible'));
  }

  const art = document.querySelector('.hero-art');
  const circle = document.querySelector('.hero-art .art-circle');
  const stamp = document.querySelector('.hero-art .art-stamp');
  const binaryField = document.querySelector('.hero-art .binary-field');
  const binaryCursor = document.querySelector('.hero-art .binary-cursor');
  const binaryRuns = binaryField ? [...binaryField.querySelectorAll('.binary-run')] : [];

  // Cursor-reactive 01010 typography: each binary run eases toward a different
  // offset around the pointer, creating a subtle, magnetic data-field effect.
  if (art && binaryField && !reduceMotion && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    const targets = binaryRuns.map((el, index) => ({
      el,
      x: 0, y: 0, tx: 0, ty: 0,
      ox: [-100, 72, -52, 110, 10][index],
      oy: [-56, -28, 38, 60, 82][index],
      lag: 0.075 + index * 0.018
    }));
    let pointerInside = false;
    let pointerX = art.clientWidth / 2;
    let pointerY = art.clientHeight / 2;
    let binaryFrame = 0;

    const paintBinary = () => {
      targets.forEach(item => {
        item.x += (item.tx - item.x) * item.lag;
        item.y += (item.ty - item.y) * item.lag;
        item.el.style.transform = `translate3d(${item.x}px, ${item.y}px, 0)`;
      });
      if (binaryCursor) {
        binaryCursor.style.transform = `translate3d(${pointerX}px, ${pointerY}px, 0) translate(-50%, -50%)`;
      }
      if (pointerInside || targets.some(item => Math.abs(item.tx - item.x) > 0.5 || Math.abs(item.ty - item.y) > 0.5)) {
        binaryFrame = window.requestAnimationFrame(paintBinary);
      } else {
        binaryFrame = 0;
      }
    };

    const moveBinary = event => {
      const rect = art.getBoundingClientRect();
      pointerX = event.clientX - rect.left;
      pointerY = event.clientY - rect.top;
      targets.forEach(item => {
        item.tx = pointerX + item.ox;
        item.ty = pointerY + item.oy;
      });
      if (!binaryFrame) binaryFrame = window.requestAnimationFrame(paintBinary);
    };
    art.addEventListener('pointerenter', event => {
      pointerInside = true;
      binaryField.classList.add('is-active');
      moveBinary(event);
    });
    art.addEventListener('pointermove', moveBinary, { passive: true });
    art.addEventListener('pointerleave', () => {
      pointerInside = false;
      binaryField.classList.remove('is-active');
      targets.forEach(item => { item.tx = item.ox * 0.15; item.ty = item.oy * 0.15; });
      if (!binaryFrame) binaryFrame = window.requestAnimationFrame(paintBinary);
    });
  }

  // Add reveal motion to meaningful content blocks, not every tiny element.
  const revealTargets = document.querySelectorAll(
    '.hero > .eyebrow, .hero h1, .hero-bottom, .hero-art, .service-strip, .intro-section, .services-section, .work-section, .local-section, .process-section, .faq-section, .cta-band, .page-hero, .form-layout, .package-grid, .category-block, .project-grid, .screenshot-grid'
  );
  revealTargets.forEach((el, index) => {
    el.setAttribute('data-reveal', '');
    if (el.classList.contains('service-card') || el.classList.contains('project-card')) {
      el.style.setProperty('--reveal-delay', `${(index % 3) * 90}ms`);
    }
  });

  if ('IntersectionObserver' in window && !reduceMotion) {
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -45px 0px' });
    revealTargets.forEach(el => observer.observe(el));
  } else {
    revealTargets.forEach(el => el.classList.add('is-visible'));
  }

  let scheduled = false;
  const updateScroll = () => {
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    const amount = maxScroll > 0 ? window.scrollY / maxScroll : 0;
    if (progress) progress.style.transform = `scaleX(${Math.min(1, Math.max(0, amount))})`;
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 16);

    // A subtle scroll-scrubbed movement gives the hero artwork a cinematic feel.
    if (art && !reduceMotion) {
      const rect = art.getBoundingClientRect();
      const travel = Math.max(-1, Math.min(1, (window.innerHeight * 0.6 - rect.top) / (window.innerHeight + rect.height)));
      art.style.translate = `0 ${travel * 16}px`;
      if (circle) circle.style.transform = `translate3d(0, ${travel * -24}px, 0) rotate(${travel * 7}deg)`;
      if (stamp) stamp.style.transform = `translate3d(0, ${travel * 10}px, 0)`;
    }
    scheduled = false;
  };
  const onScroll = () => {
    if (!scheduled) {
      window.requestAnimationFrame(updateScroll);
      scheduled = true;
    }
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  updateScroll();

  // Smoothly reach the form when a project CTA includes #contact-form.
  if (window.location.hash === '#contact-form') {
    window.addEventListener('load', () => {
      const target = document.getElementById('contact-form');
      if (target) target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
    }, { once: true });
  }
})();
