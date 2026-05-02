document.addEventListener('DOMContentLoaded', () => {
  initApp();
  renderMistakes();
});

function renderMistakes() {
  const container = document.getElementById('mistakesList');
  if (!container) return;
  const mistakes = Storage.getMistakes();
  
  if (mistakes.length === 0) {
    container.innerHTML = '<div class="empty-state"><p>🎉 No mistakes logged yet! Keep studying.</p></div>';
    // Weak areas
    const weakAreas = document.getElementById('weakAreas');
    if (weakAreas) weakAreas.innerHTML = '<p style="color:var(--text-secondary)">No weak areas detected.</p>';
    return;
  }
  
  const active = mistakes.filter(m => !m.mastered);
  const mastered = mistakes.filter(m => m.mastered);
  
  // Weak areas analysis
  const weakByType = {};
  active.forEach(m => {
    const key = m.type || 'unknown';
    weakByType[key] = (weakByType[key] || 0) + 1;
  });
  const weakAreas = document.getElementById('weakAreas');
  if (weakAreas) {
    weakAreas.innerHTML = Object.entries(weakByType).map(([type, count]) => 
      `<span class="card" style="display:inline-block;margin:0.25rem;padding:0.5rem 1rem;">${type}: <strong>${count}</strong></span>`
    ).join('') || '<p>No patterns detected.</p>';
  }
  
  container.innerHTML = `
    <h3>Active Mistakes (${active.length})</h3>
    ${active.map(m => `
      <div class="mistake-item" id="mistake-${m.id}">
        <div>
          <strong>${m.type || 'question'}</strong>: ${m.question || m.word || ''}<br>
          <small>Your answer: "${m.userAnswer}" → Correct: "${m.correctAnswer}"</small><br>
          <small style="color:var(--text-secondary)">${new Date(m.date).toLocaleString()}</small>
        </div>
        <div style="display:flex;gap:0.5rem">
          <button class="btn btn-sm btn-outline" onclick="retryMistake(${m.id})">🔄 Retry</button>
          <button class="btn btn-sm btn-success" onclick="markMastered(${m.id})">✅ Mastered</button>
        </div>
      </div>
    `).join('')}
    
    ${mastered.length > 0 ? `
      <h3 style="margin-top:2rem;">Mastered (${mastered.length})</h3>
      ${mastered.map(m => `
        <div class="mistake-item mastered">
          <div><strong>${m.type}</strong>: ${m.question || m.word || ''}</div>
        </div>
      `).join('')}
    ` : ''}
  `;
}

function retryMistake(id) {
  alert('Retry mode: Review this concept and test yourself again. (Full retry flow requires the original content JSON.)');
}

function markMastered(id) {
  Storage.markMastered(id);
  renderMistakes();
}

window.retryMistake = retryMistake;
window.markMastered = markMastered;
