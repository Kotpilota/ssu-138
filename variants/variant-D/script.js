// Вариант D — «Конверсионный B2B-лендинг»
// Ванильный JS: меню, форма, счётчики, 4-шаговый калькулятор, модалка, scroll-top

(function () {
  'use strict';

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
    }, { threshold: 0.1 });
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

  // === MAIN FORM SUBMIT ===
  const mainForm = document.querySelector('.contact-form');
  if (mainForm) {
    mainForm.addEventListener('submit', function (e) {
      e.preventDefault();
      alert('Заявка отправлена. Мы свяжемся с вами в течение рабочего дня.');
      mainForm.reset();
    });
  }

  // === CALCULATOR (4 steps) ===
  var calcState = {
    currentStep: 1,
    totalSteps: 4,
    objectType: '',
    area: 1000,
    floors: 3,
    services: [],
    name: '',
    phone: '',
    email: ''
  };

  function updateProgressBar() {
    var bar = document.querySelector('.calc-progress-bar');
    if (bar) {
      bar.style.width = ((calcState.currentStep - 1) / (calcState.totalSteps - 1) * 100) + '%';
    }
  }

  function updateStepNav() {
    var navItems = document.querySelectorAll('.calc-step-nav');
    navItems.forEach(function (item, idx) {
      var step = idx + 1;
      item.classList.remove('active', 'done');
      if (step < calcState.currentStep) item.classList.add('done');
      else if (step === calcState.currentStep) item.classList.add('active');
    });
    // Update circles for done steps
    document.querySelectorAll('.calc-step-nav.done .step-circle').forEach(function (c) {
      c.textContent = '✓';
    });
    document.querySelectorAll('.calc-step-nav:not(.done) .step-circle').forEach(function (c, idx) {
      if (!c.closest('.done')) c.textContent = idx + 1;
    });
    // Restore numbers
    navItems.forEach(function (item, idx) {
      var circle = item.querySelector('.step-circle');
      if (!item.classList.contains('done')) {
        circle.textContent = idx + 1;
      } else {
        circle.textContent = '✓';
      }
    });
  }

  function showStep(n) {
    document.querySelectorAll('.calc-step').forEach(function (s) {
      s.classList.remove('active');
    });
    var target = document.querySelector('.calc-step[data-step="' + n + '"]');
    if (target) target.classList.add('active');
    calcState.currentStep = n;
    updateProgressBar();
    updateStepNav();
    updateBackBtn();
  }

  function updateBackBtn() {
    var backBtn = document.querySelector('.btn-back');
    if (backBtn) {
      backBtn.style.visibility = calcState.currentStep > 1 ? 'visible' : 'hidden';
    }
  }

  // Area slider
  var areaSlider = document.getElementById('area-slider');
  var areaDisplay = document.getElementById('area-display');
  if (areaSlider) {
    areaSlider.addEventListener('input', function () {
      calcState.area = parseInt(this.value, 10);
      if (areaDisplay) areaDisplay.textContent = calcState.area.toLocaleString('ru') + ' м²';
    });
  }

  // Floors slider
  var floorsSlider = document.getElementById('floors-slider');
  var floorsDisplay = document.getElementById('floors-display');
  if (floorsSlider) {
    floorsSlider.addEventListener('input', function () {
      calcState.floors = parseInt(this.value, 10);
      if (floorsDisplay) floorsDisplay.textContent = this.value;
    });
  }

  // Radio cards
  document.querySelectorAll('.radio-card').forEach(function (card) {
    card.addEventListener('click', function () {
      document.querySelectorAll('.radio-card').forEach(function (c) { c.classList.remove('selected'); });
      card.classList.add('selected');
      calcState.objectType = card.dataset.value;
    });
  });

  // Checkbox services
  document.querySelectorAll('.service-checkbox').forEach(function (cb) {
    cb.addEventListener('change', function () {
      if (cb.checked) {
        if (!calcState.services.includes(cb.value)) calcState.services.push(cb.value);
      } else {
        calcState.services = calcState.services.filter(function (s) { return s !== cb.value; });
      }
    });
  });

  // Next button
  var nextBtn = document.querySelector('.btn-next');
  if (nextBtn) {
    nextBtn.addEventListener('click', function () {
      if (calcState.currentStep < calcState.totalSteps) {
        showStep(calcState.currentStep + 1);
      }
    });
  }

  // Back button
  var backBtn = document.querySelector('.btn-back');
  if (backBtn) {
    backBtn.addEventListener('click', function () {
      if (calcState.currentStep > 1) {
        showStep(calcState.currentStep - 1);
      }
    });
  }

  // Calculator form submit
  var calcForm = document.querySelector('.calc-form');
  if (calcForm) {
    calcForm.addEventListener('submit', function (e) {
      e.preventDefault();
      // Show result message
      var resultMsg = document.querySelector('.calc-result-msg');
      if (resultMsg) resultMsg.style.display = 'block';
      // Change button text
      var submitCalcBtn = calcForm.querySelector('.btn-submit-calc');
      if (submitCalcBtn) {
        submitCalcBtn.textContent = 'Заявка принята';
        submitCalcBtn.disabled = true;
        submitCalcBtn.style.background = '#1E9D5C';
      }
    });
  }

  // Hero "Start calc" button
  var startCalcBtn = document.querySelector('.btn-start-calc');
  if (startCalcBtn) {
    startCalcBtn.addEventListener('click', function () {
      var calcSection = document.getElementById('calculator');
      if (calcSection) {
        window.scrollTo({ top: calcSection.getBoundingClientRect().top + window.scrollY - 72, behavior: 'smooth' });
      }
    });
  }

  // "Рассчитать стоимость" CTA
  document.querySelectorAll('[data-scroll-to="calculator"]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var target = document.getElementById('calculator');
      if (target) {
        window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - 72, behavior: 'smooth' });
      }
    });
  });

  // Init calculator
  showStep(1);

  // === FLOATING CALLBACK BUTTON + MODAL ===
  var callbackBtn = document.querySelector('.btn-callback');
  var modalOverlay = document.querySelector('.modal-overlay');
  var modalClose = document.querySelector('.modal-close');

  if (callbackBtn && modalOverlay) {
    callbackBtn.addEventListener('click', function () {
      modalOverlay.classList.add('open');
    });
    if (modalClose) {
      modalClose.addEventListener('click', function () {
        modalOverlay.classList.remove('open');
      });
    }
    modalOverlay.addEventListener('click', function (e) {
      if (e.target === modalOverlay) modalOverlay.classList.remove('open');
    });
  }

  // Modal form submit
  var modalForm = document.querySelector('.modal-form');
  if (modalForm) {
    modalForm.addEventListener('submit', function (e) {
      e.preventDefault();
      alert('Заявка отправлена. Мы свяжемся с вами в течение рабочего дня.');
      modalForm.reset();
      if (modalOverlay) modalOverlay.classList.remove('open');
    });
  }

  // === SCROLL TOP BUTTON ===
  var scrollTopBtn = document.querySelector('.btn-scroll-top');
  window.addEventListener('scroll', function () {
    if (scrollTopBtn) {
      scrollTopBtn.classList.toggle('visible', window.scrollY > 600);
    }
  });
  if (scrollTopBtn) {
    scrollTopBtn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // === SMOOTH SCROLL for all anchors ===
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (id === '#') return;
      var target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - 72, behavior: 'smooth' });
      }
    });
  });

})();
