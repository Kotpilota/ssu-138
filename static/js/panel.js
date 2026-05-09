'use strict';

// === Mobile sidebar toggle ===
(function () {
  const sidebar  = document.getElementById('sidebar');
  const overlay  = document.getElementById('sidebarOverlay');
  const mobileBtn = document.getElementById('mobileHamburger');
  const desktopBtn = document.getElementById('sidebarToggle');

  function openSidebar() {
    sidebar?.classList.add('open');
    overlay?.classList.add('open');
  }
  function closeSidebar() {
    sidebar?.classList.remove('open');
    overlay?.classList.remove('open');
  }

  mobileBtn?.addEventListener('click', openSidebar);
  desktopBtn?.addEventListener('click', closeSidebar);
  overlay?.addEventListener('click', closeSidebar);

  // Close on nav link click (mobile)
  sidebar?.querySelectorAll('.sidebar-link').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 768) closeSidebar();
    });
  });
})();

// === Chart.js — инициализация (если есть данные на странице) ===
document.addEventListener('DOMContentLoaded', () => {
  // Line chart (заявки по дням)
  const lineEl = document.getElementById('chart-leads');
  if (lineEl && typeof Chart !== 'undefined') {
    const raw = JSON.parse(lineEl.dataset.chart || '[]');
    new Chart(lineEl, {
      type: 'line',
      data: {
        labels: raw.map(d => d.date),
        datasets: [{
          label: 'Заявки',
          data: raw.map(d => d.count),
          borderColor: '#F24D20',
          backgroundColor: 'rgba(242,77,32,0.1)',
          tension: 0.3,
          fill: true,
          pointBackgroundColor: '#F24D20',
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { ticks: { color: '#8A8F98', font: { family: 'JetBrains Mono', size: 10 } }, grid: { color: '#2A2F36' } },
          y: { ticks: { color: '#8A8F98', font: { family: 'JetBrains Mono', size: 10 }, stepSize: 1 }, grid: { color: '#2A2F36' }, beginAtZero: true },
        },
      },
    });
  }

  // Donut chart (статусы)
  const donutEl = document.getElementById('chart-statuses');
  if (donutEl && typeof Chart !== 'undefined') {
    const raw = JSON.parse(donutEl.dataset.statuses || '[]');
    new Chart(donutEl, {
      type: 'doughnut',
      data: {
        labels: raw.map(d => d.label),
        datasets: [{
          data: raw.map(d => d.count),
          backgroundColor: ['#F24D20', '#FFC107', '#4CAF50', '#2A2F36'],
          borderWidth: 0,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { color: '#8A8F98', font: { family: 'JetBrains Mono', size: 10 }, padding: 12 },
          },
        },
      },
    });
  }
});
