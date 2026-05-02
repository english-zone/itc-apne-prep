document.addEventListener('DOMContentLoaded', () => {
  initApp();
  renderFullDashboard();
});

function renderFullDashboard() {
  const container = document.getElementById('fullDashboard');
  if (!container) return;
  
  const progress = Storage.getProgress();
  const examScores = Storage.getExamScores();
  const vocab = Storage.getVocabulary();
  const mistakes = Storage.getMistakes();
  const history = Storage.getReadingHistory();
  
  const vocabEntries = Object.entries(vocab);
  const known = vocabEntries.filter(([,s]) => s === 'known').length;
  const learning = vocabEntries.filter(([,s]) => s === 'learning').length;
  const weak = vocabEntries.filter(([,s]) => s === 'weak').length;
  const activeMistakes = mistakes.filter(m => !m.mastered).length;
  
  const avgScore = examScores.length 
    ? Math.round(examScores.reduce((sum, e) => sum + e.score, 0) / examScores.length) 
    : 0;
  
  container.innerHTML = `
    <div class="dashboard-grid">
      <div class="card"><strong>🔥 Study Streak</strong><br><span style="font-size:2.5rem">${progress.streak || 0}</span> days</div>
      <div class="card"><strong>📖 Total Readings</strong><br><span style="font-size:2.5rem">${progress.readingCount || 0}</span></div>
      <div class="card"><strong>📋 Exams Taken</strong><br><span style="font-size:2.5rem">${examScores.length}</span></div>
      <div class="card"><strong>📊 Avg Exam Score</strong><br><span style="font-size:2.5rem">${avgScore}%</span></div>
    </div>
    
    <h2 style="margin-top:2rem;">📝 Vocabulary Mastery</h2>
    <div class="dashboard-grid">
      <div class="card" style="border-left:4px solid var(--known)"><strong>✅ Known</strong><br>${known} words</div>
      <div class="card" style="border-left:4px solid var(--learning)"><strong>📘 Learning</strong><br>${learning} words</div>
      <div class="card" style="border-left:4px solid var(--weak)"><strong>⚠️ Weak</strong><br>${weak} words</div>
    </div>
    
    <h2 style="margin-top:2rem;">🔁 Mistakes</h2>
    <div class="card">
      <p><strong>Active mistakes:</strong> ${activeMistakes}</p>
      <p><strong>Total logged:</strong> ${mistakes.length}</p>
      <a href="mistakes.html" class="btn btn-outline" style="margin-top:0.5rem">Review Mistakes</a>
    </div>
    
    <h2 style="margin-top:2rem;">📋 Recent Exams</h2>
    ${examScores.length === 0 ? '<div class="empty-state"><p>No exams taken yet.</p></div>' : 
      examScores.slice(-5).reverse().map(e => `
        <div class="card" style="margin-bottom:0.5rem">
          <strong>${e.title || 'Exam'}</strong> – ${e.score}% (${e.correct || 0}/${e.total || 0}) 
          <span style="color:var(--text-secondary);font-size:0.8rem">${new Date(e.date).toLocaleDateString()}</span>
        </div>
      `).join('')
    }
  `;
}
