function buildNav() {
  const currentPage = location.pathname.split('/').pop() || 'index.html';
  const links = [
    { href: 'index.html', label: '🏠 Home' },
    { href: 'reading.html', label: '📖 Reading' },
    { href: 'vocabulary.html', label: '📝 Vocab' },
    { href: 'grammar.html', label: '📐 Grammar' },
    { href: 'exams.html', label: '📋 Exams' },
    { href: 'dictionary.html', label: '📚 Dictionary' },
    { href: 'dashboard.html', label: '📊 Stats' },
    { href: 'mistakes.html', label: '🔁 Mistakes' },
  ];
  const nav = document.getElementById('navbar');
  if (!nav) return;
  nav.innerHTML = links.map(l =>
    `<a href="${l.href}" class="${currentPage === l.href ? 'active' : ''}">${l.label}</a>`
  ).join('');
}

function initTheme() {
  const saved = Storage.getTheme();
  document.documentElement.setAttribute('data-theme', saved);
  const btn = document.getElementById('themeToggle');
  if (btn) {
    btn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      Storage.setTheme(next);
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
    <div class="card"><strong>🔥 Streak</strong><br><span style="font-size:2rem">${progress.streak || 0}</span> days</div>
    <div class="card"><strong>📖 Readings</strong><br><span style="font-size:2rem">${progress.readingCount || 0}</span></div>
    <div class="card"><strong>✅ Known Words</strong><br><span style="font-size:2rem">${knownCount}</span></div>
    <div class="card"><strong>⚠️ Weak Words</strong><br><span style="font-size:2rem">${weakCount}</span></div>
    ${lastExam ? `<div class="card"><strong>📋 Last Exam</strong><br>${lastExam.score}% – ${lastExam.title || ''}</div>` : ''}
  `;
}

document.addEventListener('DOMContentLoaded', initApp);
