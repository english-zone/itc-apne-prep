let fullDictionary = {};
let currentLetter = null;

document.addEventListener('DOMContentLoaded', async () => {
  initApp();
  fullDictionary = await fetchJSON('content/dictionary/dictionary.json') || {};
  buildAlphabetFilter();
  document.getElementById('dictSearch')?.addEventListener('input', onSearch);
  renderDictionaryList();
});

function buildAlphabetFilter() {
  const container = document.getElementById('alphabetFilter');
  if (!container) return;
  const letters = '#ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
  container.innerHTML = letters.map(l => 
    `<button data-letter="${l}" onclick="filterByLetter('${l}')">${l}</button>`
  ).join('');
}

function filterByLetter(letter) {
  currentLetter = letter === '#' ? null : letter;
  document.querySelectorAll('.alphabet-filter button').forEach(b => b.classList.remove('active'));
  const btn = document.querySelector(`.alphabet-filter button[data-letter="${letter}"]`);
  if (btn) btn.classList.add('active');
  renderDictionaryList();
}

function onSearch(e) {
  currentLetter = null;
  document.querySelectorAll('.alphabet-filter button').forEach(b => b.classList.remove('active'));
  renderDictionaryList(e.target.value);
}

function renderDictionaryList(searchTerm = '') {
  const container = document.getElementById('dictionaryList');
  if (!container) return;
  let entries = Object.entries(fullDictionary);
  
  if (searchTerm) {
    const term = searchTerm.toLowerCase();
    entries = entries.filter(([word]) => word.toLowerCase().includes(term));
  } else if (currentLetter) {
    entries = entries.filter(([word]) => word.toUpperCase().startsWith(currentLetter));
  }
  
  if (entries.length === 0) {
    container.innerHTML = '<div class="empty-state"><p>No words found. Add entries to /content/dictionary/dictionary.json</p></div>';
    return;
  }
  
  container.innerHTML = entries.map(([word, entry]) => `
    <div class="card" style="cursor:pointer" onclick="showDictDetail('${word}')">
      <strong>${word}</strong>
      <span style="color:var(--text-secondary)"> – ${entry.meaning_en || entry.definition || ''}</span>
      ${entry.meaning_ar ? `<span style="color:var(--accent)"> [${entry.meaning_ar}]</span>` : ''}
    </div>
  `).join('');
}

function showDictDetail(word) {
  const entry = fullDictionary[word];
  if (!entry) return;
  const popup = document.getElementById('dictDetailPopup');
  const content = document.getElementById('dictDetailContent');
  content.innerHTML = `
    <h2>${word}</h2>
    <p><strong>EN Meaning:</strong> ${entry.meaning_en || entry.definition || '—'}</p>
    <p><strong>AR Meaning:</strong> ${entry.meaning_ar || '—'}</p>
    ${entry.pronunciation ? `<p><strong>Pronunciation:</strong> ${entry.pronunciation}</p>` : ''}
    ${entry.synonyms ? `<p><strong>Synonyms:</strong> ${entry.synonyms.join(', ')}</p>` : ''}
    ${entry.antonyms ? `<p><strong>Antonyms:</strong> ${entry.antonyms.join(', ')}</p>` : ''}
    ${entry.collocations ? `<p><strong>Collocations:</strong> ${entry.collocations.join(', ')}</p>` : ''}
    ${entry.example ? `<p><em>Example: ${entry.example}</em></p>` : ''}
  `;
  popup.style.display = 'flex';
}

window.filterByLetter = filterByLetter;
window.showDictDetail = showDictDetail;
