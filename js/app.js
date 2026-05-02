function buildNav() {
  const currentPage = location.pathname.split('/').pop() || 'index.html';
  const links = [
    { href: 'index.html', label: '🏠', title: 'Home' },
    { href: 'reading.html', label: '📖', title: 'Reading' },
    { href: 'vocabulary.html', label: '📝', title: 'Vocab' },
    { href: 'grammar.html', label: '📐', title: 'Grammar' },
    { href: 'exams.html', label: '📋', title: 'Exams' },
    { href: 'dictionary.html', label: '📚', title: 'Dictionary' },
    { href: 'dashboard.html', label: '📊', title: 'Stats' },
    { href: 'mistakes.html', label: '🔁', title: 'Mistakes' },
  ];
  const nav = document.getElementById('navbar');
  if (!nav) return;
  
  // Add brand
  const brandHTML = `<a href="index.html" class="brand"><span class="brand-icon">🚀</span> ITC Prep</a>`;
  const linksHTML = links.map(l =>
    `<a href="${l.href}" class="${currentPage === l.href ? 'active' : ''}" title="${l.title}">${l.label}</a>`
  ).join('');
  
  nav.innerHTML = brandHTML + '<span class="nav-links" style="display:flex;gap:0.25rem;flex-wrap:wrap">' + linksHTML + '</span>';
}

function initTheme() {
  const saved = Storage.getTheme();
  document.documentElement.setAttribute('data-theme', saved);
  const btn = document.getElementById('themeToggle');
  if (btn) {
    btn.textContent = saved === 'dark' ? '☀️' : '🌙';
    btn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      Storage.setTheme(next);
      btn.textContent = next === 'dark' ? '☀️' : '🌙';
    });
  }
}

function initApp() {
  buildNav();
  initTheme();
}

async function fetchJSON(path) {
  try {
    const res = await fetch(path);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch {
    return null;
  }
}

async function renderDashboardSummary() {
  const container = document.getElementById('dashboardSummary');
  if (!container) return;
  const progress = Storage.getProgress();
  const examScores = Storage.getExamScores();
  const vocab = Storage.getVocabulary();
  const vocabWords = Object.entries(vocab);
  const weakCount = vocabWords.filter(([,s]) => s === 'weak').length;
  const knownCount = vocabWords.filter(([,s]) => s === 'known').length;
  const lastExam = examScores.length ? examScores[examScores.length - 1] : null;
  
  container.innerHTML = `
    <div class="hero-stat">
      <div class="value">🔥 ${progress.streak || 0}</div>
      <div class="label">Day Streak</div>
    </div>
    <div class="hero-stat">
      <div class="value">📖 ${progress.readingCount || 0}</div>
      <div class="label">Readings</div>
    </div>
    <div class="hero-stat">
      <div class="value">✅ ${knownCount}</div>
      <div class="label">Known Words</div>
    </div>
    <div class="hero-stat">
      <div class="value">⚠️ ${weakCount}</div>
      <div class="label">Weak Words</div>
    </div>
    ${lastExam ? `
    <div class="hero-stat">
      <div class="value">📋 ${lastExam.score}%</div>
      <div class="label">Last Exam</div>
    </div>` : ''}
  `;
}

document.addEventListener('DOMContentLoaded', initApp);
