let currentVocabSet = [];
let currentVocabIndex = 0;
let currentFilter = 'all';
let dictionaryData = null;

const VOCAB_SETS = [
  { name: 'family-body', title: 'العائلة والجسم' },
  { name: 'clothing-weather', title: 'الملابس والطقس' },
  { name: 'health-medicine', title: 'الصحة والطب' },
  { name: 'food-drink', title: 'الطعام والشراب' },
  { name: 'jobs-work', title: 'الوظائف والأعمال' },
  { name: 'shopping-materials', title: 'التسوق والمواد' },
  { name: 'verbs-actions', title: 'أفعال وأحداث' }
];

document.addEventListener('DOMContentLoaded', () => {
  initApp();
  buildVocabList();
  document.getElementById('vocabSetSelector')?.addEventListener('change', onVocabSetSelect);
  
  // ✅ Handle URL parameter ?set=...
  const urlParams = new URLSearchParams(window.location.search);
  const setId = urlParams.get('set');
  if (setId) {
    setTimeout(() => {
      const selector = document.getElementById('vocabSetSelector');
      if (selector && selector.querySelector(`option[value="${setId}"]`)) {
        selector.value = setId;
        onVocabSetSelect({ target: selector });
      } else {
        console.warn(`Vocabulary set "${setId}" not found`);
      }
    }, 100);
  }
});

function buildVocabList() {
  const selector = document.getElementById('vocabSetSelector');
  if (!selector) return;
  selector.innerHTML = '<option value="">-- Load a vocab set --</option>' +
    VOCAB_SETS.map(s => `<option value="${s.name}">${s.title}</option>`).join('');
}

async function onVocabSetSelect(e) {
  const name = e.target.value;
  if (!name) return;
  const data = await fetchJSON(`content/vocabulary/${name}.json`);
  if (!data?.words) return;
  currentVocabSet = data.words.map(w => ({ english: w.english || w.word, arabic: w.arabic || '' }));
  currentVocabIndex = 0;
  dictionaryData = dictionaryData || await fetchJSON('content/dictionary/dictionary-light.json') || {};
  renderFlashcard();
}

function getFilteredWords() {
  if (currentFilter === 'all') return currentVocabSet;
  return currentVocabSet.filter(w => (Storage.getVocabulary()[w.english] || 'learning') === currentFilter);
}

function renderFlashcard() {
  const container = document.getElementById('flashcardContainer');
  const filtered = getFilteredWords();
  if (filtered.length === 0) { container.innerHTML = '<p>لا توجد كلمات.</p>'; return; }
  if (currentVocabIndex >= filtered.length) currentVocabIndex = 0;
  const word = filtered[currentVocabIndex];
  const state = Storage.getVocabulary()[word.english] || 'learning';
  const dictEntry = dictionaryData?.[word.english] || {};
  const definition = dictEntry.meaning_en || 'No definition';
  const emojis = { known: '✅', learning: '📘', weak: '⚠️' };
  const bgEmoji = emojis[state] || '📖';
  container.innerHTML = `
    <div class="flashcard" onclick="this.classList.toggle('flipped')" style="position:relative;">
      <div style="position:absolute;top:10px;right:15px;font-size:3rem;opacity:0.15;">${bgEmoji}</div>
      <div class="word">${word.english}</div>
      <div class="detail">${definition}</div>
    </div>
    <div style="margin-top:1rem; display:flex; gap:0.5rem; flex-wrap:wrap; justify-content:center;">
      <button class="btn btn-sm" onclick="markWord('known','${word.english}')">✅ Known</button>
      <button class="btn btn-sm" onclick="markWord('learning','${word.english}')">📘 Learning</button>
      <button class="btn btn-sm" onclick="markWord('weak','${word.english}')">⚠️ Weak</button>
      <button class="btn btn-sm" onclick="nextWord(${filtered.length})">➡️ Next</button>
    </div>
    <p style="text-align:center; color: var(--text-secondary);">${currentVocabIndex+1}/${filtered.length} – <strong>${state}</strong></p>
  `;
}

function markWord(state, word) { Storage.updateWord(word, state); renderFlashcard(); }
function nextWord(total) { currentVocabIndex = (currentVocabIndex + 1) % total; renderFlashcard(); }
window.markWord = markWord;
window.nextWord = nextWord;
