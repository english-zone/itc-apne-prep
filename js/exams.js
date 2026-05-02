let examTimerInterval = null;
let examSeconds = 0;
let currentExamData = null;

const EXAM_FILES = [
  'grammar-exam1','grammar-exam2','vocab-exam1','vocab-exam2','comprehensive-exam',
  'itc-p05-10','itc-p12-18','itc-p20-29','itc-p30-36','itc-p37-41',
  'itc-p41-44','itc-p44-47','itc-p48-54','itc-p55-59','itc-p60-61',
  'itc-p61-62','itc-p62-63','itc-p64-66','itc-p68-75','itc-p75-87','itc-p79-87',
  'apne-grammar-vocab','apne-mock-test'
];

document.addEventListener('DOMContentLoaded', async () => {
  initApp();
  await loadExamList();
  document.getElementById('examSelector')?.addEventListener('change', onExamSelect);
  document.getElementById('startExamBtn')?.addEventListener('click', startExam);
  document.getElementById('submitExamBtn')?.addEventListener('click', submitExam);
});

async function loadExamList() {
  const selector = document.getElementById('examSelector');
  if (!selector) return;
  selector.innerHTML = '<option value="">-- Loading exams... --</option>';
  const available = [];
  for (const name of EXAM_FILES) {
    try {
      const data = await fetchJSON(`content/exams/${name}.json`);
      if (data) available.push({ name, title: data.title || name, questions: data.questions, timeLimit: data.timeLimit });
    } catch(e) {}
  }
  if (available.length === 0) {
    selector.innerHTML = '<option value="">-- No exams found --</option>';
    return;
  }
  selector.innerHTML = '<option value="">-- Select an exam --</option>' +
    available.map(a => `<option value="${a.name}">${a.title} (${a.questions?.length||0} Q)</option>`).join('');
  window._exams = available;
}

function onExamSelect(e) {
  const exam = (window._exams || []).find(ex => ex.name === e.target.value);
  const preview = document.getElementById('examPreview');
  if (!preview || !exam) return;
  preview.innerHTML = `
    <div class="card">
      <h3>${exam.title}</h3>
      <p>Questions: ${exam.questions?.length||0} | Time: ${exam.timeLimit||'No limit'} min</p>
    </div>`;
  document.getElementById('startExamBtn').style.display = 'inline-flex';
}

function startExam() {
  const exam = (window._exams || []).find(ex => ex.name === document.getElementById('examSelector').value);
  if (!exam) return;
  currentExamData = exam;
  document.getElementById('examPreview').style.display = 'none';
  document.getElementById('examSelector').style.display = 'none';
  document.getElementById('startExamBtn').style.display = 'none';
  document.getElementById('examArea').style.display = 'block';
  document.getElementById('submitExamBtn').style.display = 'inline-flex';
  
  document.getElementById('examQuestions').innerHTML = (exam.questions||[]).map((q,i) => `
    <div class="question-block">
      <p class="q-text">${i+1}. ${q.question}</p>
      <div class="options">
        ${(q.options||[]).map((opt,j) => `<label><input type="radio" name="examQ${i}" value="${j}"> ${opt}</label>`).join('')}
      </div>
    </div>`).join('');
  
  examSeconds = 0;
  clearInterval(examTimerInterval);
  updateExamTimer();
  examTimerInterval = setInterval(() => {
    examSeconds++;
    updateExamTimer();
    if (exam.timeLimit && examSeconds >= exam.timeLimit * 60) submitExam();
  }, 1000);
}

function updateExamTimer() {
  const el = document.getElementById('examTimer');
  if (!el) return;
  const m = Math.floor(examSeconds/60).toString().padStart(2,'0');
  const s = (examSeconds%60).toString().padStart(2,'0');
  el.textContent = `⏱ ${m}:${s}`;
  if (currentExamData?.timeLimit && examSeconds >= currentExamData.timeLimit*60 - 60) el.style.color = 'var(--danger)';
}

function submitExam() {
  clearInterval(examTimerInterval);
  const questions = currentExamData?.questions || [];
  const blocks = document.querySelectorAll('#examQuestions .question-block');
  let correct = 0;
  blocks.forEach((block, i) => {
    const q = questions[i];
    if (!q) return;
    const selected = block.querySelector('input:checked');
    if (selected && String(selected.value) === String(q.answer)) correct++;
    else Storage.addMistake({ type:'exam', exam:currentExamData.title, question:q.question, userAnswer:selected?.value||'none', correctAnswer:q.answer });
  });
  const score = questions.length ? Math.round((correct/questions.length)*100) : 0;
  document.getElementById('examResults').innerHTML = `<div class="card"><strong>Result:</strong> ${correct}/${questions.length} (${score}%)</div>`;
  document.getElementById('examResults').style.display = 'block';
  document.getElementById('submitExamBtn').style.display = 'none';
  Storage.addExamScore({ title: currentExamData.title, score, total: questions.length, correct, timeSeconds: examSeconds });
}
window.startExam = startExam; window.submitExam = submitExam;
