'use strict';

// === Header sticky ===
const header = document.querySelector('.site-header');
if (header) {
  window.addEventListener('scroll', () => {
    header.classList.toggle('scrolled', window.scrollY > 40);
  }, { passive: true });
}

// === Mobile menu ===
const menuToggle = document.querySelector('.menu-toggle');
const headerNav = document.querySelector('.header-nav');
if (menuToggle && headerNav) {
  menuToggle.addEventListener('click', () => headerNav.classList.toggle('open'));
  headerNav.querySelectorAll('a').forEach(a =>
    a.addEventListener('click', () => headerNav.classList.remove('open'))
  );
}

// === Fade-up on scroll ===
const fadeEls = document.querySelectorAll('.fade-up');
if (fadeEls.length) {
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -24px 0px' });
  fadeEls.forEach(el => obs.observe(el));
}

// === Counter animation ===
function animateCount(el, target, duration) {
  let start = null;
  const suffix = el.dataset.suffix || '';
  function step(ts) {
    if (!start) start = ts;
    const prog = Math.min((ts - start) / duration, 1);
    const eased = 1 - Math.pow(1 - prog, 3);
    el.textContent = Math.floor(eased * target).toLocaleString('ru') + suffix;
    if (prog < 1) requestAnimationFrame(step);
    else el.textContent = target.toLocaleString('ru') + suffix;
  }
  requestAnimationFrame(step);
}
const counters = document.querySelectorAll('[data-count]');
if (counters.length) {
  const cObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        animateCount(e.target, parseInt(e.target.dataset.count, 10), 1500);
        cObs.unobserve(e.target);
      }
    });
  }, { threshold: 0.3 });
  counters.forEach(el => cObs.observe(el));
}

// === Contact method toggle ===
const methodRadios = document.querySelectorAll('[name="contact_method"]');
const emailField = document.getElementById('email-field');
const emailInput = document.getElementById('email');
if (methodRadios.length && emailField) {
  methodRadios.forEach(radio => {
    radio.addEventListener('change', () => {
      const isEmail = radio.value === 'email' && radio.checked;
      emailField.hidden = !isEmail;
      if (emailInput) emailInput.required = isEmail;
      document.querySelectorAll('.method-option').forEach(el => el.classList.remove('method-option--active'));
      radio.closest('.method-option')?.classList.add('method-option--active');
    });
  });
}

// === Lead form (AJAX) ===
const form = document.getElementById('lead-form');
if (form) {
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const statusEl = document.getElementById('form-status');
    const btn = form.querySelector('button[type="submit"]');

    const privacy = form.querySelector('[name="privacy"]');
    if (privacy && !privacy.checked) {
      setStatus(statusEl, 'error', 'Необходимо согласие на обработку персональных данных.');
      return;
    }

    btn.disabled = true;
    setStatus(statusEl, '', 'Отправка...');

    const data = Object.fromEntries(new FormData(form));

    try {
      const r = await fetch('/api/leads/submit/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(data),
      });
      const json = await r.json();
      if (json.ok) {
        setStatus(statusEl, 'success', 'Спасибо! Мы свяжемся с вами в течение рабочего дня.');
        form.reset();
      } else {
        const firstErr = json.errors ? Object.values(json.errors)[0] : 'Ошибка. Попробуйте ещё раз.';
        setStatus(statusEl, 'error', firstErr);
      }
    } catch {
      setStatus(statusEl, 'error', 'Ошибка соединения. Позвоните нам напрямую.');
    } finally {
      btn.disabled = false;
    }
  });
}

function setStatus(el, type, text) {
  if (!el) return;
  el.textContent = text;
  el.className = type ? `form-status--${type}` : '';
}

function getCookie(name) {
  const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return v ? v.pop() : '';
}

// === Smooth scroll ===
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - 72, behavior: 'smooth' });
    }
  });
});

// === CTA button arrow nudge ===
document.querySelectorAll('.btn-outline').forEach(btn => {
  const arrow = btn.querySelector('.arrow');
  if (!arrow) return;
  btn.addEventListener('mouseenter', () => arrow.style.transform = 'translateX(4px)');
  btn.addEventListener('mouseleave', () => arrow.style.transform = '');
});

// === Cookie consent ===
const cookieBanner = document.getElementById('cookie-banner');
if (cookieBanner && !getCookie('cookie_consent')) {
  cookieBanner.hidden = false;
  const setConsent = (val) => {
    document.cookie = `cookie_consent=${val}; max-age=31536000; path=/; SameSite=Lax`;
    cookieBanner.hidden = true;
  };
  document.getElementById('cookie-accept')?.addEventListener('click', () => setConsent('accepted'));
  document.getElementById('cookie-decline')?.addEventListener('click', () => setConsent('declined'));
}
