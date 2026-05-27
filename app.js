// Creative Intel - App Logic
(function () {
  'use strict';

  let reportsData = [];
  let skinsData = [];
  let currentTab = 'reports'; // 'reports' | 'skins'
  let currentCategory = 'all'; // 'all' | 'FPS' | 'MOBA' | 'RPG' | etc.
  let currentGame = 'all';

  // Game class mapping (for CSS styling)
  const gameClassMap = {
    'Apex Legends': 'apex',
    'CS2': 'cs2',
    'COD': 'cod',
    'Valorant': 'valorant',
    'Fortnite': 'fortnite',
    'PUBG': 'pubg',
    'Overwatch 2': 'overwatch',
    'Rainbow Six Siege': 'r6',
    'Genshin Impact': 'genshin',
    'Honor of Kings': 'hok',
    'League of Legends': 'lol',
    'Naraka': 'naraka',
    'Destiny 2': 'destiny',
    'The Finals': 'thefinals',
    'Marvel Rivals': 'marvelrivals'
  };

  // Category mapping - which games belong to which category
  const categoryMap = {
    'FPS': ['Apex Legends', 'CS2', 'COD', 'Valorant', 'Fortnite', 'PUBG', 'Overwatch 2', 'Rainbow Six Siege', 'Destiny 2', 'The Finals', 'Marvel Rivals'],
    'MOBA': ['Honor of Kings', 'League of Legends'],
    'RPG': ['Genshin Impact'],
    '\u52a8\u4f5c\u7ade\u6280': ['Naraka']
  };

  function getGameClass(game) {
    return gameClassMap[game] || game.toLowerCase().replace(/[^a-z0-9]/g, '');
  }

  function getGameCategory(game) {
    for (const [cat, games] of Object.entries(categoryMap)) {
      if (games.includes(game)) return cat;
    }
    return '\u5176\u4ed6';
  }

  // Get all categories present in current data
  function getActiveCategories(data) {
    const cats = new Set();
    if (currentTab === 'reports') {
      data.forEach(r => cats.add(r.category || getGameCategory(r.game)));
    } else {
      data.forEach(day => day.entries.forEach(e => cats.add(getGameCategory(e.game))));
    }
    return Array.from(cats);
  }

  // Get all games for a given category in current data
  function getActiveGames(data, category) {
    const games = new Set();
    if (currentTab === 'reports') {
      data.forEach(r => {
        const cat = r.category || getGameCategory(r.game);
        if (category === 'all' || cat === category) games.add(r.game);
      });
    } else {
      data.forEach(day => day.entries.forEach(e => {
        const cat = getGameCategory(e.game);
        if (category === 'all' || cat === category) games.add(e.game);
      }));
    }
    return Array.from(games);
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

  // Render two-tier filters
  function renderFilters() {
    const container = document.getElementById('filters');
    const data = currentTab === 'reports' ? reportsData : skinsData;
    const activeCategories = getActiveCategories(data);
    const activeGames = getActiveGames(data, currentCategory);

    // Tier 1: Category filter
    let html = '<div class="filter-row filter-categories">';
    html += `<button class="filter-btn category-btn ${currentCategory === 'all' ? 'active' : ''}" data-category="all">\u5168\u90e8\u54c1\u7c7b</button>`;
    activeCategories.forEach(cat => {
      html += `<button class="filter-btn category-btn ${currentCategory === cat ? 'active' : ''}" data-category="${cat}">${cat}</button>`;
    });
    html += '</div>';

    // Tier 2: Game filter (only show if there are multiple games)
    if (activeGames.length > 1) {
      html += '<div class="filter-row filter-games">';
      html += `<button class="filter-btn game-btn ${currentGame === 'all' ? 'active' : ''}" data-game="all">\u5168\u90e8\u6e38\u620f</button>`;
      activeGames.forEach(game => {
        html += `<button class="filter-btn game-btn ${currentGame === game ? 'active' : ''}" data-game="${game}">${game}</button>`;
      });
      html += '</div>';
    }

    container.innerHTML = html;

    // Event listeners - Category
    container.querySelectorAll('.category-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        currentCategory = btn.dataset.category;
        currentGame = 'all'; // reset game filter when category changes
        render();
      });
    });

    // Event listeners - Game
    container.querySelectorAll('.game-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        currentGame = btn.dataset.game;
        render();
      });
    });
  }

  // Filter logic helper
  function matchesFilter(game) {
    const cat = getGameCategory(game);
    if (currentCategory !== 'all' && cat !== currentCategory) return false;
    if (currentGame !== 'all' && game !== currentGame) return false;
    return true;
  }

  // Render report cards
  function renderReports() {
    const container = document.getElementById('content');
    let filtered = reportsData.filter(r => matchesFilter(r.game));

    if (filtered.length === 0) {
      container.innerHTML = '<p style="color:var(--text-muted);text-align:center;padding:60px 0;">\u6682\u65e0\u6570\u636e</p>';
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
        <div class="card-section-title">\u8bbe\u8ba1\u62c6\u89e3</div>
        <div class="card-analysis">${r.designAnalysis}</div>
        <div class="card-section-title">\u5bf9BS\u542f\u53d1</div>
        <div class="card-insight">${r.bsInsight}</div>
        <a class="card-source" href="${r.sourceUrl}" target="_blank" rel="noopener">\u6765\u6e90 \u2192</a>
      </div>
    `).join('')}</div>`;
  }

  // Render skins archive
  function renderSkins() {
    const container = document.getElementById('content');

    let html = '<div class="skin-section">';
    skinsData.forEach(day => {
      let entries = day.entries.filter(e => matchesFilter(e.game));
      if (entries.length === 0) return;

      html += `
        <div class="skin-date-group">
          <div class="skin-date-header">\ud83d\udcc5 ${day.date}</div>
          <div class="skin-list">
            ${entries.map(e => `
              <div class="skin-item">
                <span class="skin-game-tag ${getGameClass(e.game)}">${e.game}</span>
                <div class="skin-info">
                  <div class="skin-name">${e.skinName}</div>
                  <div class="skin-type">${e.type}</div>
                  <div class="skin-brief">${e.brief}</div>
                  <div class="skin-links">
                    <a class="skin-link source" href="${e.sourceUrl}" target="_blank" rel="noopener">\ud83c\udf10 \u6d77\u5916\u6765\u6e90</a>
                    <a class="skin-link bili" href="${e.biliSearch}" target="_blank" rel="noopener">\ud83d\udcfa B\u7ad9\u641c\u7d22</a>
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
      html = '<p style="color:var(--text-muted);text-align:center;padding:60px 0;">\u6682\u65e0\u6570\u636e</p>';
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
        currentCategory = 'all';
        currentGame = 'all';
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
