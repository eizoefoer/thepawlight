(function pawlightTheme() {
  var STORAGE_KEY = 'pawlight-theme';

  function systemTheme() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function preferredTheme() {
    var saved = '';
    try {
      saved = window.localStorage.getItem(STORAGE_KEY) || '';
    } catch (error) {
      saved = '';
    }
    return saved === 'light' || saved === 'dark' ? saved : systemTheme();
  }

  function applyTheme(theme) {
    var normalized = theme === 'light' ? 'light' : 'dark';
    document.documentElement.dataset.theme = normalized;
    document.documentElement.style.colorScheme = normalized;
    document.querySelectorAll('[data-theme-toggle]').forEach(function (button) {
      var next = normalized === 'dark' ? 'light' : 'dark';
      button.setAttribute('aria-pressed', normalized === 'dark' ? 'true' : 'false');
      button.textContent = normalized === 'dark' ? 'Light mode' : 'Dark mode';
      button.title = 'Switch to ' + next + ' mode';
    });
  }

  function persistTheme(theme) {
    try {
      window.localStorage.setItem(STORAGE_KEY, theme);
    } catch (error) {
      // Ignore storage failures; the current page can still switch themes.
    }
  }

  applyTheme(preferredTheme());

  document.addEventListener('DOMContentLoaded', function () {
    applyTheme(preferredTheme());
    document.querySelectorAll('[data-theme-toggle]').forEach(function (button) {
      button.addEventListener('click', function () {
        var current = document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light';
        var next = current === 'dark' ? 'light' : 'dark';
        persistTheme(next);
        applyTheme(next);
      });
    });
  });

  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
      var saved = '';
      try {
        saved = window.localStorage.getItem(STORAGE_KEY) || '';
      } catch (error) {
        saved = '';
      }
      if (!saved) applyTheme(systemTheme());
    });
  }
})();
