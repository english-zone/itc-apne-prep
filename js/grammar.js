const GRAMMAR_TOPICS = ['tenses', 'modals', 'conditionals', 'passive', 'wh-questions', 'gerunds'];

document.addEventListener('DOMContentLoaded', async () => {
  initApp();
  const container = document.getElementById('grammarTopics');
  if (!container) return;
  
  let anyLoaded = false;
  container.innerHTML = '<div class="cards-row" id="grammarCards"></div>';
  const cardsRow = document.getElementById('grammarCards');

  for (const topic of GRAMMAR_TOPICS) {
    const data = await fetchJSON(`content/grammar/${topic}.json`);
    const card = document.createElement('div');
    card.className = 'card';
    if (data) {
      anyLoaded = true;
      card.innerHTML = `
        <h3>📐 ${data.title || topic}</h3>
        <p style="color:var(--text-secondary)">${data.description || 'Examples from reading contexts'}</p>
        ${data.examples ? `<ul>${data.examples.slice(0,3).map(e => `<li>${e}</li>`).join('')}</ul>` : ''}
        <button class="btn btn-sm btn-outline" onclick="alert('Grammar details are context-based. Load more examples in JSON.')">View Examples</button>
      `;
    } else {
      card.innerHTML = `
        <h3>📐 ${topic}</h3>
        <p style="color:var(--text-secondary)">No content loaded. Add /content/grammar/${topic}.json</p>
      `;
    }
    cardsRow.appendChild(card);
  }
  
  if (!anyLoaded) {
    container.insertAdjacentHTML('afterbegin', '<div class="empty-state"><p>Add grammar JSON files to /content/grammar/ (e.g., tenses.json, modals.json)</p></div>');
  }
});
