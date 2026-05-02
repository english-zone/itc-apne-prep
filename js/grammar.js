let grammarData = [];
let irregularVerbs = [];

// List of grammar JSON files (based on your content folder)
const GRAMMAR_FILES = [
  'tenses', 'passive', 'comparatives', 'gerunds', 'question-tags',
  'pronouns', 'used-to', 'prepositions', 'another-other', 'modals', 'conditionals'
];

// Built-in irregular verbs (from ITC book page 111 - common verbs)
const DEFAULT_IRREGULAR_VERBS = [
  { base: "be", past: "was/were", pp: "been" },
  { base: "become", past: "became", pp: "become" },
  { base: "begin", past: "began", pp: "begun" },
  { base: "break", past: "broke", pp: "broken" },
  { base: "bring", past: "brought", pp: "brought" },
  { base: "build", past: "built", pp: "built" },
  { base: "buy", past: "bought", pp: "bought" },
  { base: "catch", past: "caught", pp: "caught" },
  { base: "choose", past: "chose", pp: "chosen" },
  { base: "come", past: "came", pp: "come" },
  { base: "cost", past: "cost", pp: "cost" },
  { base: "cut", past: "cut", pp: "cut" },
  { base: "do", past: "did", pp: "done" },
  { base: "draw", past: "drew", pp: "drawn" },
  { base: "drink", past: "drank", pp: "drunk" },
  { base: "drive", past: "drove", pp: "driven" },
  { base: "eat", past: "ate", pp: "eaten" },
  { base: "fall", past: "fell", pp: "fallen" },
  { base: "feed", past: "fed", pp: "fed" },
  { base: "feel", past: "felt", pp: "felt" },
  { base: "fight", past: "fought", pp: "fought" },
  { base: "find", past: "found", pp: "found" },
  { base: "fly", past: "flew", pp: "flown" },
  { base: "forget", past: "forgot", pp: "forgotten" },
  { base: "get", past: "got", pp: "got/gotten" },
  { base: "give", past: "gave", pp: "given" },
  { base: "go", past: "went", pp: "gone" },
  { base: "grow", past: "grew", pp: "grown" },
  { base: "have", past: "had", pp: "had" },
  { base: "hear", past: "heard", pp: "heard" },
  { base: "hide", past: "hid", pp: "hidden" },
  { base: "hit", past: "hit", pp: "hit" },
  { base: "hold", past: "held", pp: "held" },
  { base: "keep", past: "kept", pp: "kept" },
  { base: "know", past: "knew", pp: "known" },
  { base: "learn", past: "learnt/learned", pp: "learnt/learned" },
  { base: "leave", past: "left", pp: "left" },
  { base: "lend", past: "lent", pp: "lent" },
  { base: "let", past: "let", pp: "let" },
  { base: "lose", past: "lost", pp: "lost" },
  { base: "make", past: "made", pp: "made" },
  { base: "mean", past: "meant", pp: "meant" },
  { base: "meet", past: "met", pp: "met" },
  { base: "pay", past: "paid", pp: "paid" },
  { base: "put", past: "put", pp: "put" },
  { base: "read", past: "read", pp: "read" },
  { base: "ride", past: "rode", pp: "ridden" },
  { base: "ring", past: "rang", pp: "rung" },
  { base: "rise", past: "rose", pp: "risen" },
  { base: "run", past: "ran", pp: "run" },
  { base: "say", past: "said", pp: "said" },
  { base: "see", past: "saw", pp: "seen" },
  { base: "sell", past: "sold", pp: "sold" },
  { base: "send", past: "sent", pp: "sent" },
  { base: "set", past: "set", pp: "set" },
  { base: "shake", past: "shook", pp: "shaken" },
  { base: "shine", past: "shone", pp: "shone" },
  { base: "shoot", past: "shot", pp: "shot" },
  { base: "show", past: "showed", pp: "shown" },
  { base: "shut", past: "shut", pp: "shut" },
  { base: "sing", past: "sang", pp: "sung" },
  { base: "sink", past: "sank", pp: "sunk" },
  { base: "sit", past: "sat", pp: "sat" },
  { base: "sleep", past: "slept", pp: "slept" },
  { base: "speak", past: "spoke", pp: "spoken" },
  { base: "spend", past: "spent", pp: "spent" },
  { base: "stand", past: "stood", pp: "stood" },
  { base: "steal", past: "stole", pp: "stolen" },
  { base: "swim", past: "swam", pp: "swum" },
  { base: "take", past: "took", pp: "taken" },
  { base: "teach", past: "taught", pp: "taught" },
  { base: "tell", past: "told", pp: "told" },
  { base: "think", past: "thought", pp: "thought" },
  { base: "throw", past: "threw", pp: "thrown" },
  { base: "understand", past: "understood", pp: "understood" },
  { base: "wake", past: "woke", pp: "woken" },
  { base: "wear", past: "wore", pp: "worn" },
  { base: "win", past: "won", pp: "won" },
  { base: "write", past: "wrote", pp: "written" }
];

document.addEventListener('DOMContentLoaded', async () => {
  initApp();
  await loadAllGrammar();
  loadIrregularVerbs();
  renderGrammarTopics();
});

async function loadAllGrammar() {
  grammarData = [];
  for (const file of GRAMMAR_FILES) {
    const data = await fetchJSON(`content/grammar/${file}.json`);
    if (data) {
      grammarData.push({
        id: file,
        title: data.title || file.replace(/-/g, ' ').toUpperCase(),
        rules: data.rules || [],
        examples: data.examples || [],
        notes: data.notes || ''
      });
    }
  }
  // If no JSON found, use fallback built-in content
  if (grammarData.length === 0) {
    grammarData = getFallbackGrammar();
  }
}

function getFallbackGrammar() {
  return [
    {
      id: 'present-simple',
      title: 'Present Simple Tense',
      rules: ['Used for facts, habits, schedules. Form: base verb / verb+s (he/she/it)'],
      examples: ['She works at a hospital.', 'The sun rises in the east.', 'I go to school every day.'],
      notes: 'Negative: do/does + not. Question: Do/Does + subject + verb?'
    },
    {
      id: 'past-simple',
      title: 'Past Simple Tense',
      rules: ['Completed actions in the past. Regular: verb+ed. Irregular: 2nd form.'],
      examples: ['He visited Paris last year.', 'They bought a new car.', 'I woke up late yesterday.'],
      notes: 'Negative: did + not + base form.'
    },
    {
      id: 'passive-voice',
      title: 'Passive Voice',
      rules: ['Be + past participle. The object becomes the subject.'],
      examples: ['The cake was eaten by the dog.', 'This house was built in 1990.'],
      notes: 'Used when the doer is unknown or unimportant.'
    }
  ];
}

function loadIrregularVerbs() {
  // Try to load from JSON first, otherwise use default
  fetchJSON('content/grammar/irregular-verbs.json').then(data => {
    if (data && data.verbs) irregularVerbs = data.verbs;
    else irregularVerbs = DEFAULT_IRREGULAR_VERBS;
    renderIrregularVerbs();
  }).catch(() => {
    irregularVerbs = DEFAULT_IRREGULAR_VERBS;
    renderIrregularVerbs();
  });
}

function renderIrregularVerbs() {
  const container = document.getElementById('irregularVerbsContent');
  if (!container) return;
  let html = `
    <p><strong>Over 80 common irregular verbs</strong> – memorize the base, past, and past participle forms.</p>
    <div style="overflow-x:auto;">
      <table class="irregular-table">
        <thead><tr><th>Base Form</th><th>Past Simple</th><th>Past Participle</th></tr></thead>
        <tbody>
  `;
  irregularVerbs.forEach(v => {
    html += `<tr><td>${v.base}</td><td>${v.past}</td><td>${v.pp}</td></tr>`;
  });
  html += `</tbody></table></div><p class="badge-example">💡 Tip: Practice by making sentences with each verb!</p>`;
  container.innerHTML = html;
}

function renderGrammarTopics() {
  const container = document.getElementById('grammarTopics');
  if (!container) return;
  if (grammarData.length === 0) {
    container.innerHTML = '<div class="empty-state"><p>No grammar topics found. Add JSON files to /content/grammar/</p></div>';
    return;
  }
  let html = '';
  grammarData.forEach(topic => {
    html += `
      <div class="grammar-card">
        <div class="grammar-card-header" onclick="toggleGrammarCard(this)">
          📘 ${topic.title}
          <span>▼</span>
        </div>
        <div class="grammar-card-content">
          <div class="rules">
            <strong>📌 Rules:</strong>
            <ul>${topic.rules.map(r => `<li>${r}</li>`).join('')}</ul>
          </div>
          <div class="examples">
            <strong>📝 Examples (many!):</strong>
            ${topic.examples.map(ex => `<div class="example-box"><strong>→</strong> ${ex}</div>`).join('')}
          </div>
          ${topic.notes ? `<div class="notes"><strong>⚠️ Note:</strong> ${topic.notes}</div>` : ''}
        </div>
      </div>
    `;
  });
  container.innerHTML = html;
}

// Global function for toggling (called from onclick)
window.toggleGrammarCard = function(headerElement) {
  const content = headerElement.nextElementSibling;
  const arrow = headerElement.querySelector('span');
  if (content.classList.contains('active')) {
    content.classList.remove('active');
    arrow.innerHTML = '▼';
  } else {
    content.classList.add('active');
    arrow.innerHTML = '▲';
  }
};
