(function () {
  var root = document.documentElement;
  root.classList.add('js');

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- nav background after leaving the top ---- */
  var nav = document.querySelector('.nav');
  function onScroll() { if (nav) nav.classList.toggle('scrolled', window.scrollY > 40); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---- scroll reveal: fade in + rise ~18px ---- */
  var items = document.querySelectorAll('.reveal');
  if (reduceMotion || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---- hero video: still image first; video only on larger screens without reduced motion.
         To enable, set data-src on .hero-video to a short (8–12 s) seamless loop, e.g. assets/video/reel-loop.mp4 ---- */
  var video = document.querySelector('.hero-video');
  var sound = document.querySelector('.sound-toggle');
  var src = video && video.getAttribute('data-src');
  if (video && src && !reduceMotion && window.matchMedia('(min-width: 761px)').matches) {
    window.addEventListener('load', function () {
      video.src = src;
      video.muted = true;
      video.addEventListener('canplay', function () {
        video.classList.add('ready');
        video.play().catch(function () {});
        if (sound) sound.hidden = false;
      }, { once: true });
    });
    if (sound) {
      sound.addEventListener('click', function () {
        video.muted = !video.muted;
        sound.setAttribute('aria-pressed', String(!video.muted));
        sound.textContent = video.muted ? 'Sound off' : 'Sound on';
      });
    }
  }

  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
