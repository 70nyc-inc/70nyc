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
  var skipHeroVideo = saveData || reducedMotion;

  if (perfLite) {
    document.documentElement.classList.add('perf-lite');
  }

  function heroVideoSrc() {
    if (window.innerWidth <= 768) {
      return '/assets/mobile.mp4';
    }
    if ((window.devicePixelRatio || 1) >= 1.5) {
      return '/assets/hero-nyc-1080.mp4';
    }
    return '/assets/hero-nyc.mp4';
  }

  if (video && hero) {
    video.muted = true;
    video.setAttribute('playsinline', '');
    video.setAttribute('webkit-playsinline', '');

    if (!skipHeroVideo) {
      var chosenSrc = heroVideoSrc();
      video.src = chosenSrc;
      if (chosenSrc.indexOf('mobile') !== -1) {
        hero.classList.add('hero--mobile-video');
      }
    }

    function enableStaticHero() {
      hero.classList.add('hero--static');
      video.removeAttribute('autoplay');
      video.preload = 'none';
      var videoSrc = video.getAttribute('src');
      if (videoSrc) {
        video.setAttribute('data-src', videoSrc);
        video.removeAttribute('src');
        video.load();
      }
    }

    var playAttempts = 0;

    function playHeroVideo() {
      var p = video.play();
      if (p && p.catch) {
        p.catch(function () {
          playAttempts += 1;
          if (playAttempts < 4) {
            setTimeout(playHeroVideo, 300);
            return;
          }
          enableStaticHero();
        });
      }
    }

    if (skipHeroVideo) {
      enableStaticHero();
    } else {
      if (video.readyState >= 2) {
        playHeroVideo();
      } else {
        video.addEventListener('loadeddata', playHeroVideo, { once: true });
        video.addEventListener('canplay', playHeroVideo, { once: true });
      }
    }
  }

  const pageSeoHero = document.querySelector('.page-seo-hero');

  function updateHeader() {
    const topSection = hero || pageSeoHero;
    const sectionBottom = topSection ? topSection.offsetHeight : 0;
    const scrollY = window.scrollY;

    header.classList.toggle('scrolled', scrollY > 40);
    header.classList.toggle('on-light', topSection && scrollY > sectionBottom - header.offsetHeight);
  }

  window.addEventListener('scroll', updateHeader, { passive: true });
  updateHeader();

  function getHeaderOffset() {
    return (header ? header.offsetHeight : 76) + 32;
  }

  function scrollToTarget(el, behavior) {
    if (!el) return;
    var top = el.getBoundingClientRect().top + window.pageYOffset - getHeaderOffset();
    window.scrollTo({ top: Math.max(0, top), behavior: behavior || 'smooth' });
  }

  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href^="#"]');
    if (!link) return;
    var hash = link.getAttribute('href');
    if (!hash || hash.length < 2) return;
    var target = document.querySelector(hash);
    if (!target) return;
    e.preventDefault();
    scrollToTarget(target, reducedMotion ? 'auto' : 'smooth');
    if (window.history && window.history.replaceState) {
      window.history.replaceState(null, '', hash);
    }
    if (nav && nav.classList.contains('open')) {
      closeMobileNav();
    }
  });

  if (window.location.hash) {
    var hashTarget = document.querySelector(window.location.hash);
    if (hashTarget) {
      requestAnimationFrame(function () {
        scrollToTarget(hashTarget, 'auto');
      });
    }
  }

  function closeMobileNav() {
    if (!nav) return;
    nav.classList.remove('open');
    if (menuToggle) {
      menuToggle.classList.remove('open');
      menuToggle.setAttribute('aria-expanded', 'false');
    }
    var dropdown = nav.querySelector('.nav-item--dropdown');
    if (dropdown) {
      dropdown.classList.remove('is-open');
      var toggle = dropdown.querySelector('.nav-dropdown-toggle');
      if (toggle) toggle.setAttribute('aria-expanded', 'false');
    }
  }

  function initServicesDropdown() {
    if (!nav) return;
    var servicesLink = nav.querySelector('a[data-nav="services"]');
    if (!servicesLink || servicesLink.closest('.nav-item--dropdown')) return;

    var isEn = /^\/en(\/|$)/.test(window.location.pathname);
    var prefix = isEn ? '/en' : '';
    var items = isEn
      ? [
          { href: prefix + '/services/web-design/', label: 'Web Design & Development' },
          { href: prefix + '/services/seo/', label: 'SEO' },
          { href: prefix + '/services/google-ads/', label: 'Digital Advertising' },
          { href: prefix + '/services/social-media/', label: 'Social Media' },
          { href: prefix + '/services/mobile-app/', label: 'Mobile App Development' }
        ]
      : [
          { href: '/services/web-design/', label: '网页设计与网站开发' },
          { href: '/services/seo/', label: 'SEO 优化' },
          { href: '/services/google-ads/', label: '专业广告推广' },
          { href: '/services/social-media/', label: '社交媒体管理' },
          { href: '/services/mobile-app/', label: '手机应用开发' }
        ];
    var allLabel = isEn ? 'All Services' : '查看全部服务';
    var isMobileNav = window.matchMedia('(max-width: 1100px)').matches;
    var toggleLabel = isEn ? 'Show service menu' : '展开服务菜单';

    var wrapper = document.createElement('div');
    wrapper.className = 'nav-item nav-item--dropdown';

    var row = document.createElement('div');
    row.className = 'nav-item-row';

    servicesLink.parentNode.insertBefore(wrapper, servicesLink);
    row.appendChild(servicesLink);

    if (!isMobileNav) {
      var toggle = document.createElement('button');
      toggle.type = 'button';
      toggle.className = 'nav-dropdown-toggle';
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-controls', 'nav-services-menu');
      toggle.setAttribute('aria-label', toggleLabel);
      toggle.innerHTML = '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2.5 4.5 6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
      row.appendChild(toggle);

      toggle.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var open = wrapper.classList.toggle('is-open');
        toggle.setAttribute('aria-expanded', String(open));
      });
    }
    wrapper.appendChild(row);

    var dropdown = document.createElement('div');
    dropdown.className = 'nav-dropdown';
    dropdown.id = 'nav-services-menu';
    items.forEach(function (item) {
      var link = document.createElement('a');
      link.href = item.href;
      link.textContent = item.label;
      dropdown.appendChild(link);
    });
    var allLink = document.createElement('a');
    allLink.href = prefix + '/services/';
    allLink.className = 'nav-dropdown-all';
    allLink.textContent = allLabel;
    dropdown.appendChild(allLink);
    wrapper.appendChild(dropdown);
  }

  initServicesDropdown();

  if (menuToggle && nav) {
    menuToggle.addEventListener('click', function () {
      const open = nav.classList.toggle('open');
      menuToggle.classList.toggle('open', open);
      menuToggle.setAttribute('aria-expanded', String(open));
    });

    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeMobileNav();
    });
  }

  function saveLangFromSwitch(link) {
    var href = link.getAttribute('href') || '';
    var paramMatch = href.match(/[?&]lang=(zh|en)(?:&|$)/);
    try {
      if (paramMatch) {
        localStorage.setItem('70nyc-lang', paramMatch[1]);
        return;
      }
      localStorage.setItem('70nyc-lang', /\/en(\/|$)/.test(href) ? 'en' : 'zh');
    } catch (e) {}
  }

  document.querySelectorAll('.lang-switch').forEach(function (link) {
    link.addEventListener('mousedown', function () {
      saveLangFromSwitch(link);
    });
    link.addEventListener('touchstart', function () {
      saveLangFromSwitch(link);
    }, { passive: true });
  });

  const sections = document.querySelectorAll('section[id], main > section');

  function normalizePath(pathname) {
    var path = pathname.replace(/\/index\.html$/, '');
    if (path.length > 1 && path.endsWith('/')) {
      path = path.slice(0, -1);
    }
    return path || '/';
  }

  function isServicesPath(path) {
    return path === '/services' || path.indexOf('/services/') === 0 ||
      path === '/en/services' || path.indexOf('/en/services/') === 0;
  }

  function highlightNav() {
    var navLinks = document.querySelectorAll('.nav a');

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
        var isServicesNav = link.getAttribute('data-nav') === 'services' && isServicesPath(currentPath);
        link.classList.toggle('active', linkPath === currentPath || isServicesNav);
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
      var scrollTarget = document.getElementById('contact') || formSuccess;
      requestAnimationFrame(function () {
        scrollToTarget(scrollTarget, reducedMotion ? 'auto' : 'smooth');
      });
      if (window.history && window.history.replaceState) {
        window.history.replaceState(null, '', window.location.pathname + '#contact');
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
