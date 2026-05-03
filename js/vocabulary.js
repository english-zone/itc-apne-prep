let currentVocabQuestions = [];
let currentVocabIndex = 0;
let vocabScore = 0;
let currentSet = "apne_words";

async function loadVocabQuestions(setName) {
  currentSet = setName;
  try {
    const response = await fetch(`content/vocabulary/extracted/${setName}.json`);
    if (!response.ok) throw new Error("File not found");
    const words = await response.json();
    currentVocabQuestions = words.map(item => ({
      word: item.word,
      correct: item.correctMeaning,
      options: shuffleArray([item.correctMeaning, ...item.distractors]),
      example: item.example
    }));
    currentVocabIndex = 0;
    vocabScore = 0;
    displayVocabQuestion();
  } catch (err) {
    document.getElementById("vocab-quiz-area").innerHTML = `<p style="color:red;">Error loading vocabulary from ${setName}. Make sure the file exists.</p>`;
  }
}

function displayVocabQuestion() {
  if (currentVocabIndex >= currentVocabQuestions.length) {
    showVocabResult();
    return;
  }
  const q = currentVocabQuestions[currentVocabIndex];
  document.getElementById("vocab-question-text").innerHTML = `
    <strong>What is the meaning of: <span style="color:#0077cc;">${q.word}</span>?</strong>
    <div class="vocab-example">📖 Example: ${q.example}</div>
  `;
  const optionsDiv = document.getElementById("vocab-options");
  optionsDiv.innerHTML = "";
  q.options.forEach(opt => {
    const btn = document.createElement("button");
    btn.className = "vocab-option-btn";
    btn.innerText = opt;
    btn.onclick = () => checkVocabAnswer(opt);
    optionsDiv.appendChild(btn);
  });
  document.getElementById("vocab-feedback").innerHTML = "";
  document.getElementById("next-vocab-btn").style.display = "none";
}

function checkVocabAnswer(selected) {
  const q = currentVocabQuestions[currentVocabIndex];
  const isCorrect = (selected === q.correct);
  if (isCorrect) {
    vocabScore++;
    document.getElementById("vocab-feedback").innerHTML = `<span class="correct-feedback">✅ Correct! Well done.</span>`;
  } else {
    document.getElementById("vocab-feedback").innerHTML = `<span class="wrong-feedback">❌ Wrong. The correct meaning is: "${q.correct}".<br>📘 Example: ${q.example}</span>`;
  }
  document.getElementById("next-vocab-btn").style.display = "inline-block";
}

function nextVocabQuestion() {
  currentVocabIndex++;
  displayVocabQuestion();
}

function showVocabResult() {
  const total = currentVocabQuestions.length;
  document.getElementById("vocab-quiz-area").innerHTML = `
    <h2>Vocabulary Quiz Result</h2>
    <p>You scored ${vocabScore} out of ${total}.</p>
    <button onclick="resetVocab()">Try Again</button>
  `;
}

function resetVocab() {
  loadVocabQuestions(currentSet);
}

function changeSet() {
  const select = document.getElementById("set-select");
  loadVocabQuestions(select.value);
}

function shuffleArray(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

if (document.getElementById("vocab-question-text")) {
  loadVocabQuestions("apne_words");
}
