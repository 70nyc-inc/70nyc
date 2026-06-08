(function () {
  const header = document.getElementById('header');
  const nav = document.getElementById('nav');
  const menuToggle = document.getElementById('menuToggle');
  const hero = document.querySelector('.hero');
  const video = document.querySelector('.hero-video');

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var isMobilePerf = window.matchMedia('(max-width: 768px)').matches;
  var saveData = !!(navigator.connection && navigator.connection.saveData);
  var perfLite = isMobilePerf || saveData || reducedMotion;

  if (perfLite) {
    document.documentElement.classList.add('perf-lite');
  }

  if (video && hero) {
    video.muted = true;
    video.setAttribute('playsinline', '');
    video.setAttribute('webkit-playsinline', '');

    if (perfLite) {
      hero.classList.add('hero--static');
      video.removeAttribute('autoplay');
      video.preload = 'none';
      var videoSrc = video.getAttribute('src');
      if (videoSrc) {
        video.setAttribute('data-src', videoSrc);
        video.removeAttribute('src');
        video.load();
      }
    } else {
      function playHeroVideo() {
        var p = video.play();
        if (p && p.catch) {
          p.catch(function () {
            setTimeout(playHeroVideo, 300);
          });
        }
      }

      if (video.readyState >= 2) {
        playHeroVideo();
      } else {
        video.addEventListener('loadeddata', playHeroVideo, { once: true });
        video.addEventListener('canplay', playHeroVideo, { once: true });
      }
    }
  }

  function updateHeader() {
    const heroBottom = hero ? hero.offsetHeight : 0;
    const scrollY = window.scrollY;

    header.classList.toggle('scrolled', scrollY > 40);
    header.classList.toggle('on-light', scrollY > heroBottom - header.offsetHeight);
  }

  window.addEventListener('scroll', updateHeader, { passive: true });
  updateHeader();

  if (menuToggle && nav) {
    menuToggle.addEventListener('click', function () {
      const open = nav.classList.toggle('open');
      menuToggle.classList.toggle('open', open);
      menuToggle.setAttribute('aria-expanded', String(open));
    });

    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        nav.classList.remove('open');
        menuToggle.classList.remove('open');
        menuToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  const sections = document.querySelectorAll('section[id], main > section');
  const navLinks = document.querySelectorAll('.nav a');

  function normalizePath(pathname) {
    var path = pathname.replace(/\/index\.html$/, '');
    if (path.length > 1 && path.endsWith('/')) {
      path = path.slice(0, -1);
    }
    return path || '/';
  }

  function highlightNav() {
    if (document.body.classList.contains('page-sub')) {
      var currentPath = normalizePath(window.location.pathname);
      navLinks.forEach(function (link) {
        var href = link.getAttribute('href');
        if (!href || href.charAt(0) === '#') return;
        var linkPath;
        try {
          linkPath = normalizePath(new URL(href, window.location.origin).pathname);
        } catch (e) {
          return;
        }
        link.classList.toggle('active', linkPath === currentPath);
      });
      return;
    }

    let current = '';
    sections.forEach(function (section) {
      const top = section.offsetTop - 120;
      if (window.scrollY >= top) {
        current = section.id || (section.classList.contains('hero') ? 'home' : '');
      }
    });

    navLinks.forEach(function (link) {
      const dataNav = link.getAttribute('data-nav');
      const href = link.getAttribute('href') || '';
      const hashId = href.charAt(0) === '#' ? href.slice(1) : '';
      const matchId = dataNav || hashId;
      link.classList.toggle('active', matchId === current || (matchId === 'home' && (current === 'home' || !current)));
    });
  }

  window.addEventListener('scroll', highlightNav, { passive: true });
  highlightNav();

  var animSections = document.querySelectorAll(
    '.services-section, .about-section, .process-section, .industries-section, .why-section, .testimonials-section, .faq-section'
  );

  if ('IntersectionObserver' in window && animSections.length) {
    var animObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        entry.target.classList.toggle('anim-paused', !entry.isIntersecting);
      });
    }, { rootMargin: '80px 0px', threshold: 0 });

    animSections.forEach(function (section) {
      animObserver.observe(section);
    });
  }

  var aboutBg = document.querySelector('.about-bg');
  if (aboutBg) {
    aboutBg.querySelectorAll('.about-star').forEach(function (el, i) {
      var left = 2 + ((i * 23 + 11) % 96);
      var top = 4 + ((i * 31 + 7) % 88);
      var size = i % 5 === 0 ? 2.5 : i % 3 === 0 ? 1.5 : 2;
      var opacity = 0.35 + (i % 6) * 0.1;

      el.style.left = left + '%';
      el.style.top = top + '%';
      el.style.width = size + 'px';
      el.style.height = size + 'px';
      el.style.setProperty('--star-o', String(opacity));

      if (!reducedMotion) {
        el.style.animationDuration = (2.8 + (i % 5) * 1.1) + 's';
        el.style.animationDelay = (i % 8) * 0.45 + 's';
      }
    });

    var aboutHeight = aboutBg.offsetHeight || 600;

    aboutBg.querySelectorAll('.about-meteor').forEach(function (el, i) {
      var left = 12 + ((i * 29 + 17) % 76);
      var angle = -6 + ((i * 7 + 3) % 14);
      var rise = aboutHeight + 80;

      el.style.left = left + '%';
      el.style.setProperty('--meteor-angle', angle + 'deg');
      el.style.setProperty('--meteor-rise', '-' + rise + 'px');

      if (!reducedMotion) {
        el.style.animationDuration = (7 + (i % 4) * 1.5) + 's';
        el.style.animationDelay = (i * 1.4) + 's';
      }
    });
  }

  function initDandelionEmbers(container) {
    if (!container) return;

    var fallHeight = container.offsetHeight + 120;
    var embers = container.querySelectorAll('.ember');
    var emberLimit = perfLite ? 8 : embers.length;

    embers.forEach(function (el, i) {
      if (perfLite && i >= emberLimit) {
        el.style.display = 'none';
        return;
      }

      var left = 3 + ((i * 17 + 7) % 92);
      var duration = 16 + (i % 7) * 2.5 + (i % 3);
      var delay = (i % 11) * 1.1;
      var swayA = ((i % 7) - 3) * 16;
      var swayB = ((i % 5) - 2) * 20;
      var top = -3 + ((i * 11 + 5) % 6);

      el.style.setProperty('--fall', fallHeight + 'px');
      el.style.setProperty('--sway-a', swayA + 'px');
      el.style.setProperty('--sway-b', swayB + 'px');
      el.style.left = left + '%';
      el.style.top = top + '%';

      if (!reducedMotion) {
        el.style.animationDuration = duration + 's';
        el.style.animationDelay = delay + 's';
      }
    });
  }

  initDandelionEmbers(document.querySelector('.services-bg'));
  initDandelionEmbers(document.querySelector('.faq-bg'));

  if (window.location.search.indexOf('success=1') !== -1) {
    var formSuccess = document.getElementById('formSuccess');
    if (formSuccess) {
      formSuccess.hidden = false;
      if (window.history && window.history.replaceState) {
        window.history.replaceState(null, '', window.location.pathname + window.location.hash);
      }
    }
  }

  var revealEls = document.querySelectorAll('.testimonial-card.reveal');
  if (revealEls.length && 'IntersectionObserver' in window) {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var delay = parseInt(entry.target.getAttribute('data-delay') || '0', 10);
          setTimeout(function () {
            entry.target.classList.add('is-visible');
          }, delay);
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

    revealEls.forEach(function (el) {
      revealObserver.observe(el);
    });
  } else {
    revealEls.forEach(function (el) {
      el.classList.add('is-visible');
    });
  }
})();
