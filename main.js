(function () {
  document.documentElement.classList.add('js');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;

  /* ---- images fade in slowly once loaded and in view ---- */
  function reveal(el) {
    if (el.tagName !== 'IMG' || el.complete) el.classList.add('in');
    else el.addEventListener('load', function () { el.classList.add('in'); }, { once: true });
  }
  var faders = document.querySelectorAll('.fade');
  if (!hasIO) faders.forEach(reveal);
  else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { reveal(e.target); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -10% 0px' });
    faders.forEach(function (el) { io.observe(el); });
  }

  /* ---- gallery ---- */
  var gallery = document.querySelector('.gallery');
  if (!gallery) return;
  var viewport = gallery.querySelector('.viewport');
  var track = gallery.querySelector('.track');
  var imgs = Array.prototype.slice.call(gallery.querySelectorAll('.slide img'));
  var titleEl = gallery.querySelector('.now-title');
  var countEl = gallery.querySelector('.now-count');
  var n = imgs.length;
  var shown = 0;

  function label(i) {
    if (i === shown) return;
    shown = i;
    titleEl.textContent = imgs[i].getAttribute('data-title');
    countEl.textContent = (i + 1) + ' / ' + n;
  }

  // Images to the side are hidden by overflow, so lazy loading would leave them blank mid-slide:
  // load all of them as soon as the gallery comes near the screen.
  function loadAll() { imgs.forEach(function (img) { img.loading = 'eager'; }); }
  if (hasIO) {
    var near = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) { loadAll(); near.disconnect(); }
    }, { rootMargin: '600px 0px' });
    near.observe(gallery);
  } else loadAll();

  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (!finePointer) {
    // touch: native swipe; keep the caption in step
    viewport.addEventListener('scroll', function () {
      label(Math.round(viewport.scrollLeft / viewport.clientWidth));
    }, { passive: true });
    return;
  }

  // desktop: the cursor's horizontal position sets a target; the track eases towards it and stops when it arrives
  var current = 0, target = 0, frame = 0;
  var PARALLAX = 0.08; // how far each image drifts inside its frame (matches the 8% overhang in CSS)
  var EASE = 0.1;      // fraction of the remaining distance covered each frame

  function render() {
    var w = viewport.clientWidth;
    var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
    track.style.transform = 'translate3d(' + (-current * (w + gap)).toFixed(2) + 'px,0,0)';
    imgs.forEach(function (img, i) {
      var d = Math.max(-1, Math.min(1, current - i));
      img.style.transform = 'translate3d(' + (d * w * PARALLAX).toFixed(2) + 'px,0,0)';
    });
    label(Math.round(current));
  }
  function tick() {
    current += (target - current) * EASE;
    if (Math.abs(target - current) < 0.0005) { current = target; render(); frame = 0; return; }
    render();
    frame = requestAnimationFrame(tick);
  }
  function goTo(t) {
    target = Math.max(0, Math.min(n - 1, t));
    if (reduceMotion) { current = target; render(); return; }
    if (!frame) frame = requestAnimationFrame(tick);
  }

  viewport.addEventListener('mousemove', function (e) {
    var r = viewport.getBoundingClientRect();
    var x = (e.clientX - r.left) / r.width;
    goTo(((x - 0.08) / 0.84) * (n - 1)); // a small dead zone at each edge holds the first and last image
  });
  viewport.addEventListener('mouseleave', function () { goTo(Math.round(target)); }); // settle on a whole image
  viewport.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') { goTo(Math.round(target) + 1); e.preventDefault(); }
    if (e.key === 'ArrowLeft') { goTo(Math.round(target) - 1); e.preventDefault(); }
  });
  window.addEventListener('resize', render);
  render();
})();
