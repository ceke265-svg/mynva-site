(function () {
  document.documentElement.classList.add('js');

  /* images fade in once loaded and in view */
  var images = document.querySelectorAll('.fade');
  function show(img) {
    if (img.complete) img.classList.add('in');
    else img.addEventListener('load', function () { img.classList.add('in'); }, { once: true });
  }
  if (!('IntersectionObserver' in window)) {
    images.forEach(show);
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { show(e.target); io.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -10% 0px' });
  images.forEach(function (img) { io.observe(img); });
})();
