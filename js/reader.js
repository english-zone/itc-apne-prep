let currentPassageData = null, readingSeconds = 0, timerInterval = null;

const PASSAGES = [
  { name: 'japan', title: 'Japan' },
  { name: 'us-government', title: 'US Government' },
  { name: 'desalination', title: 'Water Desalination' },
  { name: 'california', title: 'California' },
  { name: 'egypt', title: 'Egypt' },
  { name: 'letter-editor', title: 'Letter to the Editor' },
  { name: 'risks-farming', title: 'The Risks of Farming' },
  { name: 'vso', title: 'Voluntary Service Overseas' },
  { name: 'bicycles', title: 'Bicycles' },
  { name: 'red-sea', title: 'The Red Sea' },
  { name: 'diabetes', title: 'Diabetes' },
  { name: 'amelia-earhart', title: 'Amelia Earhart' },
  { name: 'super-bus', title: 'The Super Bus' },
  { name: 'email-etiquette', title: 'Email Etiquette' },
  { name: 'tintin-tibet', title: 'Tintin in Tibet' },
  { name: 'yellowstone', title: 'Yellowstone' }
];

document.addEventListener('DOMContentLoaded', () => {
  initApp();
  buildPassageList();
  document.getElementById('passageSelector')?.addEventListener('change', onPassageSelect);
  document.getElementById('submitAnswers')?.addEventListener('click', submitComprehension);
});

function buildPassageList() {
  const sel = document.getElementById('passageSelector');
  if (!sel) return;
  sel.innerHTML = '<option value="">-- اختر قطعة --</option>' +
    PASSAGES.map(p => `<option value="${p.name}">${p.title}</option>`).join('');
}

async function onPassageSelect(e) {
  const name = e.target.value;
  if (!name) return;
  const data = await fetchJSON(`content/reading/${name}.json`);
  if (!data) { document.getElementById('readingContent').innerHTML = '<p class="error">فشل التحميل</p>'; return; }
  currentPassageData = data;
  renderPassage(data);
  document.getElementById('comprehensionSection').style.display = data.questions ? 'block' : 'none';
  if (data.questions) renderQuestions(data.questions);
  startTimer();
}

function renderPassage(data) {
  const container = document.getElementById('readingContent');
  const content = data.content || (data.paragraphs || []).join('\n') || data.text || 'No content.';
  container.innerHTML = content.split('\n').filter(p => p.trim()).map(p => `<p>${p}</p>`).join('');
}

function renderQuestions(questions) {
  const container = document.getElementById('questionsContainer');
  container.innerHTML = questions.map((q, i) => `
    <div class="question-card">
      <div class="q-num">${i+1}</div>
      <div class="q-text">${q.question}</div>
      <div class="options-grid">
        ${q.options.map((opt, j) => `
          <label class="option-label">
            <input type="radio" name="q${i}" value="${j}">
            <span>${opt}</span>
          </label>
        `).join('')}
      </div>
      <div class="feedback" style="display:none;"></div>
    </div>
  `).join('');
}

function submitComprehension() {
  const questions = currentPassageData?.questions || [];
  const cards = document.querySelectorAll('.question-card');
  let correct = 0;
  cards.forEach((card, i) => {
    const q = questions[i];
    if (!q) return;
    const selected = card.querySelector('input:checked');
    const fb = card.querySelector('.feedback');
    fb.style.display = 'block';
    if (selected && String(selected.value) === String(q.answer)) {
      correct++;
      fb.innerHTML = '✅ صحيح';
      fb.className = 'feedback correct';
    } else {
      fb.innerHTML = `❌ خطأ (الإجابة: ${q.options[q.answer]})`;
      fb.className = 'feedback wrong';
      if (typeof Storage !== 'undefined') Storage.addMistake({ type:'reading', passage: currentPassageData.title, question: q.question, userAnswer: selected?.value, correctAnswer: q.answer });
    }
  });
  const score = questions.length ? Math.round((correct/questions.length)*100) : 0;
  document.getElementById('resultsContainer').innerHTML = `<div class="card result-banner">النتيجة: ${correct}/${questions.length} (${score}%)</div>`;
  if (typeof Storage !== 'undefined') Storage.addExamScore({ title: currentPassageData.title, score, total: questions.length, correct });
}

function startTimer() { readingSeconds=0; clearInterval(timerInterval); updateTimerDisplay(); timerInterval=setInterval(()=>{readingSeconds++;updateTimerDisplay();},1000); }
function updateTimerDisplay(){ const el=document.getElementById('readingTimer'); if(el){ const m=Math.floor(readingSeconds/60).toString().padStart(2,'0'), s=(readingSeconds%60).toString().padStart(2,'0'); el.textContent=`⏱ ${m}:${s}`; } }
