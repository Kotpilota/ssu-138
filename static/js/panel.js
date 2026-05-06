'use strict';

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
