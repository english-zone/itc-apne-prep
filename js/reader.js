let readingTimerInterval = null;
let readingSeconds = 0;
let currentPassageData = null;
let currentDictionary = null;

const READING_PASSAGES = [
  'japan', 'us-government', 'desalination', 'california', 'egypt',
  'letter-editor', 'risks-farming', 'vso', 'bicycles', 'red-sea',
  'diabetes', 'amelia-earhart', 'super-bus', 'email-etiquette',
  'tintin-tibet', 'yellowstone'
];

document.addEventListener('DOMContentLoaded', async () => {
  initApp();
  await loadPassageList();
  document.getElementById('passageSelector')?.addEventListener('change', onPassageSelect);
  document.getElementById('focusModeBtn')?.addEventListener('click', toggleFocusMode);
  document.getElementById('submitAnswers')?.addEventListener('click', submitComprehension);
  document.querySelector('#wordPopup .popup-close')?.addEventListener('click', () => {
    document.getElementById('wordPopup').style.display = 'none';
  });
});

async function loadPassageList() {
  const selector = document.getElementById('passageSelector');
  if (!selector) return;
  selector.innerHTML = '<option value="">-- Loading passages... --</option>';
  
  const available = [];
  for (const name of READING_PASSAGES) {
    try {
      const data = await fetchJSON(`content/reading/${name}.json`);
      if (data) available.push({ name, title: data.title || name });
    } catch(e) {}
  }
  
  if (available.length === 0) {
    selector.innerHTML = '<option value="">-- No passages found --</option>';
    document.getElementById('readingContent').innerHTML = '<div class="empty-state"><p>Add JSON files to /content/reading/</p></div>';
    return;
  }
  
  selector.innerHTML = '<option value="">-- Load a passage --</option>' +
    available.map(a => `<option value="${a.name}">${a.title}</option>`).join('');
}

async function onPassageSelect(e) {
  const name = e.target.value;
  if (!name) return;
  const data = await fetchJSON(`content/reading/${name}.json`);
  if (!data) {
    document.getElementById('readingContent').innerHTML = '<div class="empty-state"><p>Failed to load passage.</p></div>';
    return;
  }
  currentPassageData = data;
  renderPassage(data);
  document.getElementById('comprehensionSection').style.display = data.questions ? 'block' : 'none';
  if (data.questions) renderQuestions(data.questions);
  startTimer();
  Storage.addReadingHistory({ passage: data.title || name });
  Storage.updateProgress({ readingCount: (Storage.getProgress().readingCount || 0) + 1 });
}

function renderPassage(data) {
  const container = document.getElementById('readingContent');
  const paragraphs = data.paragraphs || [data.text] || ['No content available.'];
  container.innerHTML = paragraphs.map(p => `<p>${makeWordsClickable(p)}</p>`).join('');
  container.querySelectorAll('.clickable-word').forEach(el => {
    el.addEventListener('click', () => showWordPopup(el.dataset.word));
  });
}

function makeWordsClickable(text) {
  return text.split(/(\s+)/).map(token => {
    const word = token.replace(/[^a-zA-Z'-]/g, '');
    if (word.length > 2 && /^[a-zA-Z]/.test(word)) {
      return `<span class="clickable-word" data-word="${word.toLowerCase()}">${token}</span>`;
    }
    return token;
  }).join('');
}

async function showWordPopup(word) {
  if (!currentDictionary) {
    currentDictionary = await fetchJSON('content/dictionary/dictionary.json') || await fetchJSON('content/dictionary/dictionary-full.json') || {};
  }
  const entry = currentDictionary[word] || currentDictionary[word.toLowerCase()];
  const popup = document.getElementById('wordPopup');
  const content = document.getElementById('popupContent');
  if (entry) {
    content.innerHTML = `
      <h2>${word}</h2>
      <p><strong>EN:</strong> ${entry.meaning_en || entry.definition || '—'}</p>
      <p><strong>AR:</strong> ${entry.meaning_ar || '—'}</p>
      ${entry.synonyms ? `<p><strong>Synonyms:</strong> ${entry.synonyms.join(', ')}</p>` : ''}
      ${entry.antonyms ? `<p><strong>Antonyms:</strong> ${entry.antonyms.join(', ')}</p>` : ''}
      ${entry.collocations ? `<p><strong>Collocations:</strong> ${entry.collocations.join(', ')}</p>` : ''}
      ${entry.example ? `<p><em>${entry.example}</em></p>` : ''}
    `;
  } else {
    content.innerHTML = `<h2>${word}</h2><p>No dictionary entry found.</p>`;
  }
  popup.style.display = 'flex';
}

function renderQuestions(questions) {
  const container = document.getElementById('questionsContainer');
  container.innerHTML = questions.map((q, i) => `
    <div class="question-block" data-index="${i}" data-type="${q.type || 'mcq'}">
      <p class="q-text">${i + 1}. ${q.question}</p>
      <div class="options">
        ${(q.options || []).map((opt, j) => `
          <label><input type="radio" name="q${i}" value="${j}"> ${opt}</label>
        `).join('')}
        ${q.type === 'truefalse' ? `
          <label><input type="radio" name="q${i}" value="true"> True</label>
          <label><input type="radio" name="q${i}" value="false"> False</label>
        ` : ''}
      </div>
      <div class="feedback" style="display:none;"></div>
    </div>
  `).join('');
}

function submitComprehension() {
  const questions = currentPassageData?.questions || [];
  const blocks = document.querySelectorAll('.question-block');
  let correct = 0;
  blocks.forEach((block, i) => {
    const q = questions[i];
    if (!q) return;
    const selected = block.querySelector('input:checked');
    const feedback = block.querySelector('.feedback');
    feedback.style.display = 'block';
    if (selected) {
      const userAnswer = selected.value;
      const isCorrect = String(userAnswer) === String(q.answer);
      if (isCorrect) {
        correct++;
        feedback.textContent = '✅ Correct!';
        feedback.className = 'feedback correct';
      } else {
        feedback.textContent = `❌ Wrong. Correct: ${q.options ? q.options[q.answer] : q.answer}`;
        feedback.className = 'feedback wrong';
        Storage.addMistake({ type:'reading', passage: currentPassageData.title, question: q.question, userAnswer, correctAnswer: q.answer });
      }
    } else {
      feedback.textContent = '⚠️ Not answered';
      feedback.className = 'feedback wrong';
    }
  });
  const score = questions.length ? Math.round((correct / questions.length) * 100) : 0;
  document.getElementById('resultsContainer').innerHTML = `<div class="card"><strong>Score:</strong> ${correct}/${questions.length} (${score}%)</div>`;
  Storage.addExamScore({ title: currentPassageData.title, score, total: questions.length, correct });
}

function startTimer() {
  readingSeconds = 0;
  clearInterval(readingTimerInterval);
  updateTimerDisplay();
  readingTimerInterval = setInterval(() => { readingSeconds++; updateTimerDisplay(); }, 1000);
}

function updateTimerDisplay() {
  const el = document.getElementById('readingTimer');
  if (el) {
    const m = Math.floor(readingSeconds / 60).toString().padStart(2, '0');
    const s = (readingSeconds % 60).toString().padStart(2, '0');
    el.textContent = `${m}:${s}`;
  }
}

function toggleFocusMode() {
  document.body.classList.toggle('focus-mode');
  const btn = document.getElementById('focusModeBtn');
  if (btn) btn.textContent = document.body.classList.contains('focus-mode') ? '📖 Exit Focus' : '🧘 Focus Mode';
}
