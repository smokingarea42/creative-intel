// Creative Intel - App Logic v2
(function () {
  'use strict';

  let reportsData = [];
  let skinsData = [];
  let activitiesData = [];
  let currentTab = 'reports'; // 'reports' | 'skins' | 'activities' | 'favorites'
  let currentCategory = 'all';
  let currentGame = 'all';
  let favorites = { reports: [], skins: [], activities: [] }; // stored in localStorage

  // Load favorites from localStorage
  function loadFavorites() {
    try {
      const saved = localStorage.getItem('creative-intel-favorites');
      if (saved) {
        const parsed = JSON.parse(saved);
        favorites.reports = parsed.reports || [];
        favorites.skins = parsed.skins || [];
        favorites.activities = parsed.activities || [];
      }
    } catch (e) { /* ignore */ }
  }
  function saveFavorites() {
    localStorage.setItem('creative-intel-favorites', JSON.stringify(favorites));
  }
  function isFavorited(type, id) {
    return (favorites[type] || []).includes(id);
  }
  function toggleFavorite(type, id) {
    const idx = favorites[type].indexOf(id);
    if (idx === -1) { favorites[type].push(id); } else { favorites[type].splice(idx, 1); }
    saveFavorites();
    render();
  }

  // Game class mapping (for CSS styling)
  const gameClassMap = {
    'Apex Legends': 'apex',
    'CS2': 'cs2',
    'COD': 'cod',
    'CODM': 'codm',
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
    'Marvel Rivals': 'marvelrivals',
    '\u9006\u6218\u672a\u6765': 'nzwl',
    '\u7a7f\u8d8a\u706b\u7ebf': 'cf',
    '\u6697\u533a\u7a81\u56f4': 'aqtw',
    '\u706b\u5f71\u5fcd\u8005\u624b\u6e38': 'naruto',
    '\u738b\u8005\u8363\u8000': 'hok2',
    '\u548c\u5e73\u7cbe\u82f1': 'pubgm2',
    '\u4e09\u89d2\u6d32\u884c\u52a8': 'deltaforce',
    'CFM': 'cfm'
  };

  // Category mapping
  const categoryMap = {
    'FPS': ['Apex Legends', 'CS2', 'COD', 'CODM', 'CFM', 'Valorant', 'Fortnite', 'PUBG', 'Overwatch 2', 'Rainbow Six Siege', 'Destiny 2', 'The Finals', 'Marvel Rivals', '\u9006\u6218\u672a\u6765', '\u7a7f\u8d8a\u706b\u7ebf', '\u6697\u533a\u7a81\u56f4', '\u4e09\u89d2\u6d32\u884c\u52a8', '\u548c\u5e73\u7cbe\u82f1'],
    'MOBA': ['Honor of Kings', 'League of Legends', 'MLBB', 'MLBB (Mobile Legends)', 'Mobile Legends'],
    'RPG': ['Genshin Impact'],
    '\u4f11\u95f2/\u7b56\u7565': ['Monopoly Go', 'Monopoly Go (Scopely)'],
    '\u5f00\u653e\u4e16\u754c': ['Neverness to Everness', 'Neverness to Everness (\u6c38\u65e0\u6b62\u5883)'],
    '\u52a8\u4f5c\u7ade\u6280': ['Naraka', '\u6c38\u52ab\u65e0\u95f4']
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

  function getActiveCategories(data) {
    const cats = new Set();
    if (currentTab === 'reports' || currentTab === 'favorites') {
      const list = currentTab === 'favorites' ? data.filter(r => isFavorited('reports', r.id)) : data;
      list.forEach(r => cats.add(r.category || getGameCategory(r.game)));
    } else {
      data.forEach(day => day.entries.forEach(e => cats.add(getGameCategory(e.game))));
    }
    return Array.from(cats);
  }

  function getActiveGames(data, category) {
    const games = new Set();
    if (currentTab === 'reports' || currentTab === 'favorites') {
      const list = currentTab === 'favorites' ? data.filter(r => isFavorited('reports', r.id)) : data;
      list.forEach(r => {
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
    const bust = Date.now();
    try {
      const [reportsRes, skinsRes, activitiesRes] = await Promise.all([
        fetch('data/reports.json?v=' + bust),
        fetch('data/skins.json?v=' + bust),
        fetch('data/activities.json?v=' + bust)
      ]);
      reportsData = await reportsRes.json();
      skinsData = await skinsRes.json();
      activitiesData = await activitiesRes.json();
      // Sort by date descending (newest first)
      reportsData.sort((a, b) => b.date.localeCompare(a.date));
      activitiesData.sort((a, b) => b.date.localeCompare(a.date));
      skinsData.sort((a, b) => b.date.localeCompare(a.date));
    } catch (e) {
      console.error('Failed to load data:', e);
    }
    render();
  }

  function render() {
    renderFilters();
    if (currentTab === 'reports') {
      renderReports();
      applyHighlights();
    } else if (currentTab === 'skins') {
      renderSkins();
    } else if (currentTab === 'activities') {
      renderActivities();
    } else if (currentTab === 'favorites') {
      renderFavorites();
      applyHighlights();
    }
  }

  // Two-tier filters
  function renderFilters() {
    const container = document.getElementById('filters');
    if (currentTab !== 'skins') {
      container.innerHTML = '';
      return;
    }
    const data = skinsData;
    const activeCategories = getActiveCategories(data);
    const activeGames = getActiveGames(data, currentCategory);

    let html = '<div class="filter-row filter-categories">';
    html += `<button class="filter-btn category-btn ${currentCategory === 'all' ? 'active' : ''}" data-category="all">\u5168\u90e8\u54c1\u7c7b</button>`;
    activeCategories.forEach(cat => {
      html += `<button class="filter-btn category-btn ${currentCategory === cat ? 'active' : ''}" data-category="${cat}">${cat}</button>`;
    });
    html += '</div>';

    if (activeGames.length > 1) {
      html += '<div class="filter-row filter-games">';
      html += `<button class="filter-btn game-btn ${currentGame === 'all' ? 'active' : ''}" data-game="all">\u5168\u90e8\u6e38\u620f</button>`;
      activeGames.forEach(game => {
        html += `<button class="filter-btn game-btn ${currentGame === game ? 'active' : ''}" data-game="${game}">${game}</button>`;
      });
      html += '</div>';
    }

    container.innerHTML = html;

    container.querySelectorAll('.category-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        currentCategory = btn.dataset.category;
        currentGame = 'all';
        render();
      });
    });
    container.querySelectorAll('.game-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        currentGame = btn.dataset.game;
        render();
      });
    });
  }

  function matchesFilter(game) {
    const cat = getGameCategory(game);
    if (currentCategory !== 'all' && cat !== currentCategory) return false;
    if (currentGame !== 'all' && game !== currentGame) return false;
    return true;
  }

  // Format title: split at dash into two lines
  function formatTitle(title) {
    const separators = [' \u2014 ', ' �?', ' - '];
    for (const sep of separators) {
      const idx = title.indexOf(sep);
      if (idx > 0) {
        return `<span class="card-title-main">${title.substring(0, idx)}</span><span class="card-title-sub">${title.substring(idx + sep.length)}</span>`;
      }
    }
    return `<span class="card-title-main">${title}</span>`;
  }

  // Render report cards
  function renderReports() {
    const container = document.getElementById('content');
    let filtered = reportsData;

    if (filtered.length === 0) {
      container.innerHTML = '<p style="color:var(--text-muted);text-align:center;padding:60px 0;">\u6682\u65e0\u6570\u636e</p>';
      return;
    }

    container.innerHTML = `<div class="cards-grid">${filtered.map(r => `
      <div class="report-card">
        <div class="card-header">
          <span class="card-date">${r.date}</span>
          <div class="card-header-right">
            <span class="card-game ${getGameClass(r.game)}">${r.game}</span>
            <button class="fav-btn ${isFavorited('reports', r.id) ? 'active' : ''}" data-type="reports" data-id="${r.id}" title="\u6536\u85cf">\u2605</button>
          </div>
        </div>
        <div class="card-title">${formatTitle(r.title)}</div>
        <div class="card-highlights">${r.highlights}</div>
        <div class="card-section-title">\u8bbe\u8ba1\u62c6\u89e3</div>
        <div class="card-analysis">${r.designAnalysis}</div>
        <div class="card-section-title">\u5bf9BS\u542f\u53d1</div>
        <div class="card-insight">${r.bsInsight}</div>
        <a class="card-source" href="${r.sourceUrl}" target="_blank" rel="noopener">\u6765\u6e90 \u2192</a>
      </div>
    `).join('')}</div>`;

    bindFavButtons();
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
            ${entries.map(e => {
              const skinId = `${day.date}-${e.game}-${e.skinName}`;
              const thumb = e.imageUrl ? `<div class="skin-thumb"><img src="${e.imageUrl}" alt="${e.skinName}" loading="lazy"></div>` : '';
              return `
              <div class="skin-item">
                ${thumb}
                <button class="fav-btn ${isFavorited('skins', skinId) ? 'active' : ''}" data-type="skins" data-id="${skinId}" title="\u6536\u85cf">\u2605</button>
                <div class="skin-body">
                  <span class="skin-game-tag ${getGameClass(e.game)}">${e.game}</span>
                  <div class="skin-info">
                    <div class="skin-name">${e.skinName}</div>
                    <div class="skin-type">${e.type}${e.releaseDate ? ' · ' + e.releaseDate : ''}</div>
                    <div class="skin-brief">${e.brief}</div>
                    <div class="skin-links">
                      <a class="skin-link source" href="${e.sourceUrl}" target="_blank" rel="noopener">\ud83c\udf10 \u6d77\u5916\u6765\u6e90</a>
                      <a class="skin-link bili" href="${e.biliSearch}" target="_blank" rel="noopener">\ud83d\udcfa B\u7ad9\u641c\u7d22</a>
                    </div>
                  </div>
                </div>
              </div>`;
            }).join('')}
          </div>
        </div>
      `;
    });
    html += '</div>';

    if (html === '<div class="skin-section"></div>') {
      html = '<p style="color:var(--text-muted);text-align:center;padding:60px 0;">\u6682\u65e0\u6570\u636e</p>';
    }

    container.innerHTML = html;
    bindFavButtons();
  }

  // Render activities
  function renderActivities() {
    const container = document.getElementById('content');
    let filtered = activitiesData;

    if (filtered.length === 0) {
      container.innerHTML = '<p style="color:var(--text-muted);text-align:center;padding:60px 0;">\u6682\u65e0\u6570\u636e</p>';
      return;
    }

    container.innerHTML = `<div class="cards-grid">${filtered.map(a => `
      <div class="report-card activity-card">
        <div class="card-header">
          <span class="card-date">${a.date}</span>
          <div class="card-header-right">
            <span class="card-game ${getGameClass(a.game)}">${a.game}</span>
            <span class="mechanism-tag">${a.mechanismType}</span>
            <span class="activity-tag ${a.tag.includes('\u8ba8\u8bba') ? 'hot' : 'new'}">${a.tag}</span>
            <button class="fav-btn ${isFavorited('activities', a.id) ? 'active' : ''}" data-type="activities" data-id="${a.id}" title="\u6536\u85cf">\u2605</button>
          </div>
        </div>
        <div class="card-title activity-title">${formatTitle(a.title)}</div>
        <div class="activity-heat">${a.heat}</div>
        <div class="card-section-title">\u6838\u5fc3\u673a\u5236</div>
        <div class="card-analysis">${a.mechanism.replace(/\n/g, '<br>')}</div>
        <div class="card-section-title">\u4e3a\u4ec0\u4e48\u706b</div>
        <div class="card-analysis">${a.whyHot.replace(/\n/g, '<br>')}</div>
        <div class="card-section-title">\u7b56\u5212\u89c6\u89d2</div>
        <div class="card-insight">${a.insight.replace(/\n/g, '<br>')}</div>
        <a class="card-source" href="${a.sourceUrl}" target="_blank" rel="noopener">\u89c6\u9891\u6765\u6e90 \u2192</a>
      </div>
    `).join('')}</div>`;

    bindFavButtons();
  }
  function renderFavorites() {
    const container = document.getElementById('content');
    let html = '';

    // Favorite reports
    const favReports = reportsData.filter(r => isFavorited('reports', r.id));
    html += '<h2 class="fav-section-title">\ud83d\udccc \u6536\u85cf\u7684\u60c5\u62a5</h2>';
    if (favReports.length === 0) {
      html += '<p class="fav-empty">\u6682\u65e0\u6536\u85cf\u7684\u60c5\u62a5</p>';
    } else {
      html += `<div class="cards-grid">${favReports.map(r => `
        <div class="report-card">
          <div class="card-header">
            <span class="card-date">${r.date}</span>
            <div class="card-header-right">
              <span class="card-game ${getGameClass(r.game)}">${r.game}</span>
              <button class="fav-btn active" data-type="reports" data-id="${r.id}" title="\u53d6\u6d88\u6536\u85cf">\u2605</button>
            </div>
          </div>
          <div class="card-title">${formatTitle(r.title)}</div>
          <div class="card-highlights">${r.highlights}</div>
          <div class="card-section-title">\u8bbe\u8ba1\u62c6\u89e3</div>
          <div class="card-analysis">${r.designAnalysis}</div>
          <div class="card-section-title">\u5bf9BS\u542f\u53d1</div>
          <div class="card-insight">${r.bsInsight}</div>
          <a class="card-source" href="${r.sourceUrl}" target="_blank" rel="noopener">\u6765\u6e90 \u2192</a>
        </div>
      `).join('')}</div>`;
    }

    // Favorite skins
    html += '<h2 class="fav-section-title" style="margin-top:40px;">\ud83c\udfa8 \u6536\u85cf\u7684\u76ae\u80a4</h2>';
    const favSkinIds = favorites.skins;
    let favSkins = [];
    skinsData.forEach(day => {
      day.entries.forEach(e => {
        const skinId = `${day.date}-${e.game}-${e.skinName}`;
        if (favSkinIds.includes(skinId)) {
          favSkins.push({ ...e, date: day.date, skinId });
        }
      });
    });

    if (favSkins.length === 0) {
      html += '<p class="fav-empty">\u6682\u65e0\u6536\u85cf\u7684\u76ae\u80a4</p>';
    } else {
      html += '<div class="skin-list">';
      favSkins.forEach(e => {
        const thumb = e.imageUrl ? `<div class="skin-thumb"><img src="${e.imageUrl}" alt="${e.skinName}" loading="lazy"></div>` : '';
        html += `
          <div class="skin-item">
            ${thumb}
            <button class="fav-btn active" data-type="skins" data-id="${e.skinId}" title="\u53d6\u6d88\u6536\u85cf">\u2605</button>
            <div class="skin-body">
              <span class="skin-game-tag ${getGameClass(e.game)}">${e.game}</span>
              <div class="skin-info">
                <div class="skin-name">${e.skinName}</div>
                <div class="skin-type">${e.type} \u00b7 ${e.date}</div>
                <div class="skin-brief">${e.brief}</div>
                <div class="skin-links">
                  <a class="skin-link source" href="${e.sourceUrl}" target="_blank" rel="noopener">\ud83c\udf10 \u6d77\u5916\u6765\u6e90</a>
                  <a class="skin-link bili" href="${e.biliSearch}" target="_blank" rel="noopener">\ud83d\udcfa B\u7ad9\u641c\u7d22</a>
                </div>
              </div>
            </div>
          </div>`;
      });
      html += '</div>';
    }

    // Favorite activities
    html += '<h2 class="fav-section-title" style="margin-top:40px;">\ud83d\udcb0 \u6536\u85cf\u7684\u6d3b\u52a8</h2>';
    const favActivities = activitiesData.filter(a => isFavorited('activities', a.id));
    if (favActivities.length === 0) {
      html += '<p class="fav-empty">\u6682\u65e0\u6536\u85cf\u7684\u6d3b\u52a8</p>';
    } else {
      html += `<div class="cards-grid">${favActivities.map(a => `
        <div class="report-card activity-card">
          <div class="card-header">
            <span class="card-date">${a.date}</span>
            <div class="card-header-right">
              <span class="card-game ${getGameClass(a.game)}">${a.game}</span>
              <span class="mechanism-tag">${a.mechanismType}</span>
              <button class="fav-btn active" data-type="activities" data-id="${a.id}" title="\u53d6\u6d88\u6536\u85cf">\u2605</button>
            </div>
          </div>
          <div class="card-title">${formatTitle(a.title)}</div>
          <div class="activity-heat">${a.heat}</div>
          <div class="card-section-title">\u6838\u5fc3\u673a\u5236</div>
          <div class="card-analysis">${a.mechanism.replace(/\n/g, '<br>')}</div>
          <div class="card-section-title">\u7b56\u5212\u89c6\u89d2</div>
          <div class="card-insight">${a.insight.replace(/\n/g, '<br>')}</div>
          <a class="card-source" href="${a.sourceUrl}" target="_blank" rel="noopener">\u89c6\u9891\u6765\u6e90 \u2192</a>
        </div>
      `).join('')}</div>`;
    }

    container.innerHTML = html;
    bindFavButtons();
  }

  // Bind favorite button clicks
  function bindFavButtons() {
    document.querySelectorAll('.fav-btn').forEach(btn => {
      btn.addEventListener('click', (ev) => {
        ev.stopPropagation();
        toggleFavorite(btn.dataset.type, btn.dataset.id);
      });
    });
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

  // ========== TEXT HIGHLIGHT SYSTEM ==========
  let highlights = []; // { cardId, text }

  function loadHighlights() {
    try {
      const saved = localStorage.getItem('creative-intel-highlights');
      if (saved) highlights = JSON.parse(saved);
    } catch (e) { /* ignore */ }
  }
  function saveHighlights() {
    localStorage.setItem('creative-intel-highlights', JSON.stringify(highlights));
  }

  // Apply stored highlights to rendered report cards
  function applyHighlights() {
    document.querySelectorAll('.report-card').forEach(card => {
      const cardId = card.querySelector('.fav-btn')?.dataset?.id;
      if (!cardId) return;
      const cardHighlights = highlights.filter(h => h.cardId === cardId);
      if (cardHighlights.length === 0) return;

      // Only highlight within these specific areas
      const areas = card.querySelectorAll('.card-highlights, .card-analysis, .card-insight');
      areas.forEach(area => {
        let html = area.textContent; // use textContent to avoid nesting issues
        // Rebuild: escape HTML first
        html = area.innerHTML;
        // Remove existing marks first to avoid double-wrapping
        html = html.replace(/<mark class="text-highlight"[^>]*>(.*?)<\/mark>/g, '$1');
        cardHighlights.forEach(h => {
          const escaped = h.text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
          const re = new RegExp(escaped, 'g');
          html = html.replace(re, `<mark class="text-highlight" data-card="${cardId}" data-text="${h.text.replace(/"/g, '&quot;')}">${h.text}</mark>`);
        });
        area.innerHTML = html;
      });
    });

    // Bind click on highlights to show remove button
    document.querySelectorAll('.text-highlight').forEach(mark => {
      mark.addEventListener('click', (ev) => {
        ev.stopPropagation();
        const rect = mark.getBoundingClientRect();
        showRemoveBtn(
          rect.left + rect.width / 2 - 40 + window.scrollX,
          rect.top - 36 + window.scrollY,
          mark.dataset.card,
          mark.dataset.text
        );
      });
    });
  }

  // Floating highlight button
  let hlBtn = null;
  let removeBtn = null;

  function createHighlightBtn() {
    hlBtn = document.createElement('button');
    hlBtn.className = 'highlight-popup-btn';
    hlBtn.textContent = '\u2728 \u9ad8\u4eae';
    hlBtn.style.display = 'none';
    document.body.appendChild(hlBtn);

    hlBtn.addEventListener('mousedown', (ev) => {
      ev.preventDefault();
      ev.stopPropagation();
      applyHighlightFromSelection();
    });

    // Remove button
    removeBtn = document.createElement('button');
    removeBtn.className = 'highlight-remove-btn';
    removeBtn.textContent = '\u2716 \u53d6\u6d88\u9ad8\u4eae';
    removeBtn.style.display = 'none';
    document.body.appendChild(removeBtn);

    removeBtn.addEventListener('mousedown', (ev) => {
      ev.preventDefault();
      ev.stopPropagation();
      const cardId = removeBtn.dataset.card;
      const text = removeBtn.dataset.text;
      removeHighlight(cardId, text);
    });
  }

  function removeHighlight(cardId, text) {
    highlights = highlights.filter(h => !(h.cardId === cardId && h.text === text));
    saveHighlights();
    hideRemoveBtn();
    applyHighlights();
  }

  function showRemoveBtn(x, y, cardId, text) {
    if (!removeBtn) return;
    removeBtn.style.left = x + 'px';
    removeBtn.style.top = y + 'px';
    removeBtn.style.display = 'flex';
    removeBtn.dataset.card = cardId;
    removeBtn.dataset.text = text;
  }

  function hideRemoveBtn() {
    if (removeBtn) removeBtn.style.display = 'none';
  }

  function applyHighlightFromSelection() {
    const sel = window.getSelection();
    if (!sel || sel.isCollapsed) return;
    const text = sel.toString().trim();
    if (!text || text.length < 2) return;

    // Find parent report card
    let node = sel.anchorNode;
    let card = null;
    while (node && node !== document) {
      if (node.classList && node.classList.contains('report-card')) { card = node; break; }
      node = node.parentNode;
    }
    if (!card) return;

    const cardId = card.querySelector('.fav-btn')?.dataset?.id;
    if (!cardId) return;

    const exists = highlights.find(h => h.cardId === cardId && h.text === text);
    if (!exists) {
      highlights.push({ cardId, text });
      saveHighlights();
    }

    applyHighlights();
    sel.removeAllRanges();
    hideHighlightBtn();
  }

  function showHighlightBtn(x, y) {
    if (!hlBtn) return;
    hlBtn.style.left = x + 'px';
    hlBtn.style.top = y + 'px';
    hlBtn.style.display = 'flex';
  }

  function hideHighlightBtn() {
    if (hlBtn) hlBtn.style.display = 'none';
  }

  // Check if selection is entirely within allowed highlightable areas
  function isSelectionInHighlightableArea(sel) {
    const allowedClasses = ['card-highlights', 'card-analysis', 'card-insight'];

    function isInAllowed(node) {
      while (node && node !== document) {
        if (node.classList) {
          for (const cls of allowedClasses) {
            if (node.classList.contains(cls)) return true;
          }
          // If we hit the card boundary without finding an allowed area, stop
          if (node.classList.contains('report-card')) return false;
        }
        node = node.parentNode;
      }
      return false;
    }

    return isInAllowed(sel.anchorNode) && isInAllowed(sel.focusNode);
  }

  function initHighlightSystem() {
    createHighlightBtn();

    document.addEventListener('mouseup', (ev) => {
      setTimeout(() => {
        const sel = window.getSelection();
        if (!sel || sel.isCollapsed || sel.toString().trim().length < 2) {
          hideHighlightBtn();
          return;
        }

        // Check if selection is inside a report card
        let node = sel.anchorNode;
        let inCard = false;
        while (node && node !== document) {
          if (node.classList && node.classList.contains('report-card')) { inCard = true; break; }
          node = node.parentNode;
        }
        if (!inCard) { hideHighlightBtn(); return; }

        // Only show highlight btn if selection is within highlightable areas
        if (!isSelectionInHighlightableArea(sel)) {
          hideHighlightBtn();
          return;
        }

        const range = sel.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        showHighlightBtn(
          rect.left + rect.width / 2 - 36 + window.scrollX,
          rect.top - 40 + window.scrollY
        );
      }, 10);
    });

    // Hide remove btn on click elsewhere
    document.addEventListener('mousedown', (ev) => {
      if (removeBtn && ev.target !== removeBtn && !removeBtn.contains(ev.target)) {
        hideRemoveBtn();
      }
    });

    document.addEventListener('scroll', () => {
      hideHighlightBtn();
      hideRemoveBtn();
    }, { passive: true });
  }

  // Init
  function init() {
    loadFavorites();
    loadHighlights();
    initTabs();
    initHighlightSystem();
    loadData();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
