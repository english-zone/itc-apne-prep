let currentExamData = null, examSeconds = 0, examTimer = null;

const EXAM_FILES = [
  'itc-p05-10','itc-p12-18','itc-p20-29','itc-p30-36','itc-p37-41',
  'itc-p41-44','itc-p44-47','itc-p48-54','itc-p55-59','itc-p60-61',
  'itc-p61-62','itc-p62-63','itc-p64-66','itc-p68-75','itc-p75-87','itc-p79-87',
  'apne-grammar-vocab','apne-mock-test'
];

document.addEventListener('DOMContentLoaded', () => {
  initApp();
  buildExamList();
  document.getElementById('startExamBtn')?.addEventListener('click', startExam);
  document.getElementById('submitExamBtn')?.addEventListener('click', submitExam);
});

function buildExamList() {
  const sel = document.getElementById('examSelector');
  if (!sel) return;
  sel.innerHTML = '<option value="">-- اختر اختبار --</option>' +
    EXAM_FILES.map(f => `<option value="${f}">${f.replace(/-/g,' ').toUpperCase()}</option>`).join('');
  sel.addEventListener('change', onExamSelect);
}

async function onExamSelect(e) {
  const name = e.target.value;
  if (!name) return;
  const data = await fetchJSON(`content/exams/${name}.json`);
  if (!data?.questions) { document.getElementById('examPreview').innerHTML = '<p>فشل التحميل</p>'; return; }
  currentExamData = { ...data, name };
  document.getElementById('examPreview').innerHTML = `
    <div class="card">
      <h3>${data.title || name}</h3>
      <p>عدد الأسئلة: ${data.questions.length} | الوقت: ${data.timeLimit || 'غير محدد'} دقيقة</p>
    </div>`;
  document.getElementById('startExamBtn').style.display = 'inline-flex';
}

function startExam() {
  if (!currentExamData) return;
  document.getElementById('examSelector').style.display = 'none';
  document.getElementById('examPreview').style.display = 'none';
  document.getElementById('startExamBtn').style.display = 'none';
  document.getElementById('examArea').style.display = 'block';
  document.getElementById('submitExamBtn').style.display = 'inline-flex';
  document.getElementById('examQuestions').innerHTML = currentExamData.questions.map((q,i) => `
    <div class="question-card">
      <div class="q-num">${i+1}</div>
      <div class="q-text">${q.question}</div>
      <div class="options-grid">
        ${(q.options||[]).map((opt,j) => `
          <label class="option-label">
            <input type="radio" name="eq${i}" value="${j}">
            <span>${opt}</span>
          </label>
        `).join('')}
      </div>
    </div>
  `).join('');
  examSeconds = 0; clearInterval(examTimer); updateTimer();
  examTimer = setInterval(() => { examSeconds++; updateTimer(); if (currentExamData.timeLimit && examSeconds >= currentExamData.timeLimit*60) submitExam(); }, 1000);
}

function updateTimer() { const el=document.getElementById('examTimer'); if(el){ const m=Math.floor(examSeconds/60).toString().padStart(2,'0'), s=(examSeconds%60).toString().padStart(2,'0'); el.textContent=`⏱ ${m}:${s}`; } }
function submitExam() {
  clearInterval(examTimer);
  const questions = currentExamData.questions;
  const cards = document.querySelectorAll('#examQuestions .question-card');
  let correct = 0;
  cards.forEach((card,i) => {
    const q = questions[i];
    if (!q) return;
    const selected = card.querySelector('input:checked');
    if (selected && String(selected.value) === String(q.answer)) correct++;
  });
  const score = questions.length ? Math.round((correct/questions.length)*100) : 0;
  document.getElementById('examResults').innerHTML = `<div class="card result-banner">النتيجة: ${correct}/${questions.length} (${score}%)</div>`;
  document.getElementById('examResults').style.display = 'block';
  document.getElementById('submitExamBtn').style.display = 'none';
  if (typeof Storage !== 'undefined') Storage.addExamScore({ title: currentExamData.title||currentExamData.name, score, total: questions.length, correct, timeSeconds: examSeconds });
}
