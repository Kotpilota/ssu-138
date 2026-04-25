// Вариант A — «Государственный подрядчик»
// Ванильный JS: меню, счётчики, форма, анимации

(function () {
  'use strict';

  // === HEADER: sticky class on scroll ===
  const header = document.querySelector('.site-header');
  window.addEventListener('scroll', function () {
    if (window.scrollY > 40) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });

  // === MOBILE MENU ===
  const menuToggle = document.querySelector('.menu-toggle');
  const headerNav = document.querySelector('.header-nav');
  if (menuToggle && headerNav) {
    menuToggle.addEventListener('click', function () {
      headerNav.classList.toggle('open');
      const expanded = headerNav.classList.contains('open');
      menuToggle.setAttribute('aria-expanded', expanded);
    });
    // Close menu on link click
    headerNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        headerNav.classList.remove('open');
      });
    });
  }

  // === FADE-UP ANIMATIONS on scroll ===
  const fadeEls = document.querySelectorAll('.fade-up');
  if (fadeEls.length) {
    const fadeObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            fadeObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );
    fadeEls.forEach(function (el) { fadeObserver.observe(el); });
  }

  // === COUNTER ANIMATION ===
  function animateCounter(el, target, duration) {
    var start = 0;
    var startTime = null;
    // Extract numeric prefix / suffix
    var suffix = el.dataset.suffix || '';
    var prefix = el.dataset.prefix || '';

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      var current = Math.floor(eased * target);
      el.textContent = prefix + current.toLocaleString('ru') + suffix;
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = prefix + target.toLocaleString('ru') + suffix;
      }
    }
    requestAnimationFrame(step);
  }

  const counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    const counterObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var el = entry.target;
            var target = parseInt(el.dataset.count, 10);
            animateCounter(el, target, 1200);
            counterObserver.unobserve(el);
          }
        });
      },
      { threshold: 0.3 }
    );
    counters.forEach(function (el) { counterObserver.observe(el); });
  }

  // === FORM SUBMIT ===
  const form = document.querySelector('.contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      alert('Заявка отправлена. Мы свяжемся с вами в течение рабочего дня.');
      form.reset();
    });
  }

  // === SMOOTH SCROLL for anchor links ===
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      var target = document.querySelector(link.getAttribute('href'));
      if (target) {
        e.preventDefault();
        var offset = 72;
        var top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top: top, behavior: 'smooth' });
      }
    });
  });

})();
