let currentVocabSet = [];
let currentVocabIndex = 0;
let currentFilter = 'all';
let dictionaryData = null;

document.addEventListener('DOMContentLoaded', async () => {
  initApp();
  await loadVocabSets();
  document.getElementById('vocabSetSelector')?.addEventListener('change', onVocabSetSelect);
  document.querySelectorAll('.filter-btns .btn').forEach(btn => {
    btn.addEventListener('click', () => {
      currentFilter = btn.dataset.filter;
      document.querySelectorAll('.filter-btns .btn').forEach(b => b.classList.remove('btn-primary'));
      btn.classList.add('btn-primary');
      renderFlashcard();
    });
  });
  document.querySelector('#wordDetailPopup .popup-close')?.addEventListener('click', () => {
    document.getElementById('wordDetailPopup').style.display = 'none';
  });
});

async function loadVocabSets() {
  const selector = document.getElementById('vocabSetSelector');
  if (!selector) return;
  const names = ['set1', 'set2', 'vocab1', 'sample', 'essential'];
  const available = [];
  for (const name of names) {
    const data = await fetchJSON(`content/vocabulary/${name}.json`);
    if (data && data.words) available.push({ name, title: data.title || name, words: data.words });
  }
  if (available.length === 0) {
    selector.innerHTML = '<option value="">-- No vocab sets --</option>';
    document.getElementById('flashcardContainer').innerHTML = '<div class="empty-state"><p>Add JSON files to /content/vocabulary/</p></div>';
    return;
  }
  selector.innerHTML = '<option value="">-- Load a vocab set --</option>' +
    available.map(a => `<option value="${a.name}">${a.title} (${a.words.length} words)</option>`).join('');
  window._vocabSets = available;
}

async function onVocabSetSelect(e) {
  const name = e.target.value;
  const set = (window._vocabSets || []).find(s => s.name === name);
  if (!set) return;
  currentVocabSet = set.words;
  currentVocabIndex = 0;
  dictionaryData = dictionaryData || await fetchJSON('content/dictionary/dictionary.json') || {};
  renderFlashcard();
}

function getFilteredWords() {
  if (currentFilter === 'all') return currentVocabSet;
  return currentVocabSet.filter(w => {
    const state = Storage.getVocabulary()[w.word] || 'learning';
    return state === currentFilter;
  });
}

function renderFlashcard() {
  const container = document.getElementById('flashcardContainer');
  const filtered = getFilteredWords();
  if (filtered.length === 0) {
    container.innerHTML = '<div class="empty-state"><p>No words match this filter.</p></div>';
    return;
  }
  if (currentVocabIndex >= filtered.length) currentVocabIndex = 0;
  const word = filtered[currentVocabIndex];
  const state = Storage.getVocabulary()[word.word] || 'learning';
  container.innerHTML = `
    <div class="flashcard" id="flashcardEl" onclick="this.classList.toggle('flipped')">
      <div class="word">${word.word}</div>
      <div class="detail" id="flashcardDetail">Tap to reveal</div>
    </div>
    <div class="flashcard-controls">
      <button class="btn btn-sm" onclick="markWord('known')">✅ Known</button>
      <button class="btn btn-sm" onclick="markWord('learning')">📘 Learning</button>
      <button class="btn btn-sm" onclick="markWord('weak')">⚠️ Weak</button>
      <button class="btn btn-sm" onclick="showWordDetail('${word.word}')">📚 Detail</button>
      <button class="btn btn-sm" onclick="nextWord(${filtered.length})">➡️ Next</button>
    </div>
    <p style="color:var(--text-secondary)">${currentVocabIndex + 1} / ${filtered.length} – State: <strong>${state}</strong></p>
  `;
  // Preload detail for flip
  const detail = dictionaryData[word.word] || {};
  const detailEl = document.getElementById('flashcardDetail');
  if (detailEl) {
    detailEl.textContent = detail.meaning_en || detail.definition || 'No definition';
  }
}

function markWord(state) {
  const filtered = getFilteredWords();
  const word = filtered[currentVocabIndex];
  if (!word) return;
  Storage.updateWord(word.word, state);
  renderFlashcard();
}

function nextWord(total) {
  currentVocabIndex = (currentVocabIndex + 1) % total;
  renderFlashcard();
}

function showWordDetail(word) {
  const entry = dictionaryData[word] || {};
  const popup = document.getElementById('wordDetailPopup');
  const content = document.getElementById('detailContent');
  content.innerHTML = `
    <h2>${word}</h2>
    <p><strong>EN:</strong> ${entry.meaning_en || entry.definition || '—'}</p>
    <p><strong>AR:</strong> ${entry.meaning_ar || '—'}</p>
    ${entry.synonyms ? `<p><strong>Synonyms:</strong> ${entry.synonyms.join(', ')}</p>` : ''}
    ${entry.antonyms ? `<p><strong>Antonyms:</strong> ${entry.antonyms.join(', ')}</p>` : ''}
    ${entry.collocations ? `<p><strong>Collocations:</strong> ${entry.collocations.join(', ')}</p>` : ''}
    ${entry.example ? `<p><em>${entry.example}</em></p>` : ''}
  `;
  popup.style.display = 'flex';
}
