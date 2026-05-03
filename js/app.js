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
  
  // Brand with Reyadah logo image
  const brandHTML = `
    <div style="display:flex; align-items:center; gap:0.75rem;">
      <a href="index.html" class="brand" style="font-weight:bold; font-size:1.2rem;">🚀 ITC Prep</a>
      <span style="border-left:2px solid var(--border); height:24px;"></span>
      <img src="assets/images/reyadah-logo.png" alt="مركز الريادة للتدريب" style="height:32px; width:auto;">
    </div>
  `;
  
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

function addPrintButton() {
  const themeBtn = document.getElementById('themeToggle');
  if (themeBtn && !document.getElementById('printButton')) {
    const printBtn = document.createElement('button');
    printBtn.id = 'printButton';
    printBtn.textContent = '🖨️';
    printBtn.title = 'Print page (content only)';
    printBtn.style.marginLeft = '0.5rem';
    printBtn.style.background = 'var(--surface)';
    printBtn.style.border = '1px solid var(--border)';
    printBtn.style.borderRadius = '2rem';
    printBtn.style.width = '2.5rem';
    printBtn.style.height = '2.5rem';
    printBtn.style.cursor = 'pointer';
    printBtn.addEventListener('click', () => {
      window.print();
    });
    themeBtn.parentNode.appendChild(printBtn);
  }
}

function initApp() {
  buildNav();
  initTheme();
  addPrintButton();
}

async function fetchJSON(path) {
  try {
    const res = await fetch(path);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (e) {
    console.warn(e);
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
