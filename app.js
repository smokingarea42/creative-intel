// Creative Intel - App Logic
(function () {
  'use strict';

  let reportsData = [];
  let skinsData = [];
  let currentTab = 'reports'; // 'reports' | 'skins'
  let currentFilter = 'all';

  // Game class mapping
  const gameClassMap = {
    'Apex Legends': 'apex',
    'CS2': 'cs2',
    'COD': 'cod',
    'Valorant': 'valorant',
    'Fortnite': 'fortnite'
  };

  function getGameClass(game) {
    return gameClassMap[game] || game.toLowerCase().replace(/\s+/g, '');
  }

  // Load data
  async function loadData() {
    try {
      const [reportsRes, skinsRes] = await Promise.all([
        fetch('data/reports.json'),
        fetch('data/skins.json')
      ]);
      reportsData = await reportsRes.json();
      skinsData = await skinsRes.json();
    } catch (e) {
      console.error('Failed to load data:', e);
    }
    render();
  }

  // Render
  function render() {
    renderFilters();
    if (currentTab === 'reports') {
      renderReports();
    } else {
      renderSkins();
    }
  }

  // Render filters
  function renderFilters() {
    const container = document.getElementById('filters');
    const games = ['all', 'Apex Legends', 'CS2', 'COD', 'Valorant', 'Fortnite'];
    const labels = { all: '全部', 'Apex Legends': 'Apex', CS2: 'CS2', COD: 'COD', Valorant: 'Valorant', Fortnite: 'Fortnite' };

    container.innerHTML = games.map(g =>
      `<button class="filter-btn ${currentFilter === g ? 'active' : ''}" data-filter="${g}">${labels[g]}</button>`
    ).join('');

    container.querySelectorAll('.filter-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        currentFilter = btn.dataset.filter;
        render();
      });
    });
  }

  // Render report cards
  function renderReports() {
    const container = document.getElementById('content');
    let filtered = reportsData;
    if (currentFilter !== 'all') {
      filtered = filtered.filter(r => r.game === currentFilter);
    }

    if (filtered.length === 0) {
      container.innerHTML = '<p style="color:var(--text-muted);text-align:center;padding:60px 0;">暂无数据</p>';
      return;
    }

    container.innerHTML = `<div class="cards-grid">${filtered.map(r => `
      <div class="report-card">
        <div class="card-header">
          <span class="card-date">${r.date}</span>
          <span class="card-game ${getGameClass(r.game)}">${r.game}</span>
        </div>
        <div class="card-title">${r.title}</div>
        <div class="card-highlights">${r.highlights}</div>
        <div class="card-section-title">设计拆解</div>
        <div class="card-analysis">${r.designAnalysis}</div>
        <div class="card-section-title">对BS启发</div>
        <div class="card-insight">${r.bsInsight}</div>
        <a class="card-source" href="${r.sourceUrl}" target="_blank" rel="noopener">来源 →</a>
      </div>
    `).join('')}</div>`;
  }

  // Render skins archive
  function renderSkins() {
    const container = document.getElementById('content');
    let filtered = skinsData;

    // Filter by game within each day
    let html = '<div class="skin-section">';
    filtered.forEach(day => {
      let entries = day.entries;
      if (currentFilter !== 'all') {
        entries = entries.filter(e => e.game === currentFilter);
      }
      if (entries.length === 0) return;

      html += `
        <div class="skin-date-group">
          <div class="skin-date-header">📅 ${day.date}</div>
          <div class="skin-list">
            ${entries.map(e => `
              <div class="skin-item">
                <span class="skin-game-tag ${getGameClass(e.game)}">${e.game}</span>
                <div class="skin-info">
                  <div class="skin-name">${e.skinName}</div>
                  <div class="skin-type">${e.type}</div>
                  <div class="skin-brief">${e.brief}</div>
                  <div class="skin-links">
                    <a class="skin-link source" href="${e.sourceUrl}" target="_blank" rel="noopener">🌐 海外来源</a>
                    <a class="skin-link bili" href="${e.biliSearch}" target="_blank" rel="noopener">📺 B站搜索</a>
                  </div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    });
    html += '</div>';

    if (html === '<div class="skin-section"></div>') {
      html = '<p style="color:var(--text-muted);text-align:center;padding:60px 0;">暂无数据</p>';
    }

    container.innerHTML = html;
  }

  // Tab switching
  function initTabs() {
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentTab = btn.dataset.tab;
        currentFilter = 'all';
        render();
      });
    });
  }

  // Init
  document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    loadData();
  });
})();
