let fullDictionary = {};   // { word: { ar: '', en: '' } }
let currentLetter = null;
let vocabularySets = [
  'family-body', 'clothing-weather', 'health-medicine', 'food-drink',
  'jobs-work', 'shopping-materials', 'verbs-actions'
];

document.addEventListener('DOMContentLoaded', async () => {
  initApp();
  await loadAllVocabulary();
  buildAlphabetFilter();
  document.getElementById('dictSearch')?.addEventListener('input', onSearch);
  renderDictionaryList();
});

async function loadAllVocabulary() {
  fullDictionary = {};
  for (const setName of vocabularySets) {
    const data = await fetchJSON(`content/vocabulary/${setName}.json`);
    if (data && data.words) {
      data.words.forEach(item => {
        const word = item.word;
        if (!fullDictionary[word]) {
          fullDictionary[word] = {
            ar: item.meaning_ar || item.arabic || '',
            en: item.meaning_en || item.definition || item.english || ''
          };
        }
      });
    }
  }
  // Optional: also load from dictionary.json as fallback, but only keep simple fields
  const legacy = await fetchJSON('content/dictionary/dictionary.json');
  if (legacy) {
    for (const [word, entry] of Object.entries(legacy)) {
      if (!fullDictionary[word]) {
        fullDictionary[word] = {
          ar: entry.meaning_ar || '',
          en: entry.meaning_en || entry.definition || ''
        };
      }
    }
  }
}

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
  document.querySelectorAll('#alphabetFilter button').forEach(b => b.classList.remove('active'));
  const btn = document.querySelector(`#alphabetFilter button[data-letter="${letter}"]`);
  if (btn) btn.classList.add('active');
  renderDictionaryList();
}

function onSearch(e) {
  currentLetter = null;
  document.querySelectorAll('#alphabetFilter button').forEach(b => b.classList.remove('active'));
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
  
  // Sort alphabetically
  entries.sort((a, b) => a[0].localeCompare(b[0]));
  
  if (entries.length === 0) {
    container.innerHTML = '<div class="empty-state"><p>❌ No words found. Make sure vocabulary files exist in /content/vocabulary/</p></div>';
    return;
  }
  
  container.innerHTML = entries.map(([word, data]) => `
    <div class="card dict-card" onclick="showSimpleMeaning('${word.replace(/'/g, "\\'")}')">
      <div><strong>${word}</strong> <span style="color:var(--accent);">${data.ar ? '🇸🇦 ' + data.ar : ''}</span></div>
      <div style="font-size:0.85rem; color:var(--text-secondary);">${data.en || ''}</div>
    </div>
  `).join('');
}

function showSimpleMeaning(word) {
  const data = fullDictionary[word];
  if (!data) return;
  alert(`${word}\n\nArabic: ${data.ar}\nEnglish: ${data.en || '—'}`);
}

window.filterByLetter = filterByLetter;
window.showSimpleMeaning = showSimpleMeaning;
