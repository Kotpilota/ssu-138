// Вариант B — «Industrial / Engineering»
// Ванильный JS: меню, счётчики, форма, fade-up

(function () {
  'use strict';

  // === HEADER sticky ===
  const header = document.querySelector('.site-header');
  window.addEventListener('scroll', function () {
    header.classList.toggle('scrolled', window.scrollY > 40);
  });

  // === MOBILE MENU ===
  const menuToggle = document.querySelector('.menu-toggle');
  const headerNav = document.querySelector('.header-nav');
  if (menuToggle && headerNav) {
    menuToggle.addEventListener('click', function () {
      headerNav.classList.toggle('open');
    });
    headerNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        headerNav.classList.remove('open');
      });
    });
  }

  // === FADE-UP on scroll ===
  const fadeEls = document.querySelectorAll('.fade-up');
  if (fadeEls.length) {
    const obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          obs.unobserve(e.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });
    fadeEls.forEach(function (el) { obs.observe(el); });
  }

  // === COUNTER ANIMATION ===
  function animateCount(el, target, duration) {
    var start = null;
    var suffix = el.dataset.suffix || '';
    function step(ts) {
      if (!start) start = ts;
      var prog = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - prog, 3);
      el.textContent = Math.floor(eased * target).toLocaleString('ru') + suffix;
      if (prog < 1) requestAnimationFrame(step);
      else el.textContent = target.toLocaleString('ru') + suffix;
    }
    requestAnimationFrame(step);
  }

  const counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    const obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          animateCount(e.target, parseInt(e.target.dataset.count, 10), 1500);
          obs.unobserve(e.target);
        }
      });
    }, { threshold: 0.3 });
    counters.forEach(function (el) { obs.observe(el); });
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

  // === SMOOTH SCROLL ===
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var target = document.querySelector(a.getAttribute('href'));
      if (target) {
        e.preventDefault();
        window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - 64, behavior: 'smooth' });
      }
    });
  });

  // === CTA arrow nudge ===
  document.querySelectorAll('.btn-outline-b').forEach(function (btn) {
    btn.addEventListener('mouseenter', function () {
      var arrow = btn.querySelector('.arrow');
      if (arrow) arrow.style.transform = 'translateX(4px)';
    });
    btn.addEventListener('mouseleave', function () {
      var arrow = btn.querySelector('.arrow');
      if (arrow) arrow.style.transform = '';
    });
  });

})();
