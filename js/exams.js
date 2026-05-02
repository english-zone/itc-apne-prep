let examTimerInterval = null;
let examSeconds = 0;
let currentExamData = null;

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
  const names = ['exam1', 'midterm', 'final', 'practice1', 'sample'];
  const available = [];
  for (const name of names) {
    const data = await fetchJSON(`content/exams/${name}.json`);
    if (data) available.push({ name, title: data.title || name, questions: data.questions, timeLimit: data.timeLimit });
  }
  if (available.length === 0) {
    selector.innerHTML = '<option value="">-- No exams found --</option>';
    return;
  }
  selector.innerHTML = '<option value="">-- Select an exam --</option>' +
    available.map(a => `<option value="${a.name}">${a.title} (${a.questions?.length || 0} Q, ${a.timeLimit || '∞'} min)</option>`).join('');
  window._exams = available;
}

function onExamSelect(e) {
  const name = e.target.value;
  const exam = (window._exams || []).find(ex => ex.name === name);
  const preview = document.getElementById('examPreview');
  if (!preview) return;
  if (exam) {
    preview.innerHTML = `
      <div class="card">
        <h3>${exam.title}</h3>
        <p>Questions: ${exam.questions?.length || 0}</p>
        <p>Time Limit: ${exam.timeLimit || 'No limit'} minutes</p>
      </div>
    `;
    document.getElementById('startExamBtn').style.display = 'inline-flex';
  }
}

function startExam() {
  const name = document.getElementById('examSelector').value;
  const exam = (window._exams || []).find(ex => ex.name === name);
  if (!exam) return;
  currentExamData = exam;
  document.getElementById('examPreview').style.display = 'none';
  document.getElementById('examSelector').style.display = 'none';
  document.getElementById('startExamBtn').style.display = 'none';
  document.getElementById('examArea').style.display = 'block';
  document.getElementById('submitExamBtn').style.display = 'inline-flex';
  
  const container = document.getElementById('examQuestions');
  container.innerHTML = (exam.questions || []).map((q, i) => `
    <div class="question-block" data-index="${i}">
      <p class="q-text">${i + 1}. ${q.question}</p>
      <div class="options">
        ${(q.options || []).map((opt, j) => `
          <label><input type="radio" name="examQ${i}" value="${j}"> ${opt}</label>
        `).join('')}
      </div>
    </div>
  `).join('');
  
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
  const m = Math.floor(examSeconds / 60).toString().padStart(2, '0');
  const s = (examSeconds % 60).toString().padStart(2, '0');
  el.textContent = `⏱ ${m}:${s}`;
  if (currentExamData?.timeLimit) {
    const remaining = currentExamData.timeLimit * 60 - examSeconds;
    if (remaining < 60) el.style.color = 'var(--danger)';
  }
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
    else if (!selected || String(selected.value) !== String(q.answer)) {
      Storage.addMistake({
        type: 'exam',
        exam: currentExamData.title,
        question: q.question,
        userAnswer: selected?.value || 'not answered',
        correctAnswer: q.answer
      });
    }
  });
  const score = questions.length ? Math.round((correct / questions.length) * 100) : 0;
  document.getElementById('examResults').innerHTML = `
    <div class="card"><strong>Result:</strong> ${correct}/${questions.length} (${score}%)</div>
    <div class="card"><strong>Time:</strong> ${Math.floor(examSeconds/60)}m ${examSeconds%60}s</div>
  `;
  document.getElementById('examResults').style.display = 'block';
  document.getElementById('submitExamBtn').style.display = 'none';
  Storage.addExamScore({ title: currentExamData.title, score, total: questions.length, correct, timeSeconds: examSeconds });
}

// Expose to global scope for inline onclick in HTML
window.startExam = startExam;
window.submitExam = submitExam;
