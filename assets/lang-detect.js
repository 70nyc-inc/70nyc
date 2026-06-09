(function () {
  var KEY = '70nyc-lang';

  function normalizePath(pathname) {
    var path = pathname.replace(/\/index\.html$/, '');
    if (path.length > 1 && path.endsWith('/')) {
      path = path.slice(0, -1);
    }
    return path || '/';
  }

  function isEnglishPath(path) {
    return path === '/en' || path.indexOf('/en/') === 0;
  }

  function toEnglishPath(path) {
    if (path === '/') return '/en/';
    return '/en' + path;
  }

  function toChinesePath(path) {
    if (path === '/en') return '/';
    if (path.indexOf('/en/') === 0) return path.slice(3) || '/';
    return '/';
  }

  function prefersEnglish() {
    var saved = null;
    try {
      saved = localStorage.getItem(KEY);
    } catch (e) {}

    if (saved === 'en') return true;
    if (saved === 'zh') return false;

    var langs = navigator.languages && navigator.languages.length
      ? navigator.languages
      : [navigator.language || ''];
    var primary = (langs[0] || '').toLowerCase();

    if (/^zh/.test(primary)) return false;
    if (/^en/.test(primary)) return true;

    var hasZh = langs.some(function (l) {
      return /^zh/i.test(l);
    });
    var hasEn = langs.some(function (l) {
      return /^en/i.test(l);
    });

    if (hasZh && !hasEn) return false;
    if (hasEn && !hasZh) return true;
    return false;
  }

  var path = normalizePath(window.location.pathname);
  var onEnglish = isEnglishPath(path);
  var wantEnglish = prefersEnglish();
  var target = null;

  if (wantEnglish && !onEnglish) {
    target = toEnglishPath(path);
  } else if (!wantEnglish && onEnglish) {
    target = toChinesePath(path);
  }

  if (target && target !== path) {
    window.location.replace(target + window.location.search + window.location.hash);
  }
})();
