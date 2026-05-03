const dictationData = [
  { sentence: "The teacher asked us to _____ our homework on time.", options: ["submit", "submitt", "submet", "submitte"], correct: "submit" },
  { sentence: "She has a strong _____ in her abilities.", options: ["confidence", "confidance", "confidense", "confidince"], correct: "confidence" },
  { sentence: "The _____ of the new policy was felt immediately.", options: ["effect", "affect", "efect", "affectt"], correct: "effect" },
  { sentence: "He received an _____ to the graduation ceremony.", options: ["invitation", "invintation", "invitationn", "invateition"], correct: "invitation" },
  { sentence: "The company's _____ is to provide excellent service.", options: ["mission", "mision", "misson", "mition"], correct: "mission" }
];
let currentDictationIndex = 0, dictationScore = 0;
function loadDictationQuestion() {
  const q = dictationData[currentDictationIndex];
  document.getElementById("dictation-sentence").innerText = q.sentence;
  const container = document.getElementById("dictation-options");
  container.innerHTML = "";
  q.options.forEach(opt => { const btn = document.createElement("button"); btn.className = "dictation-option"; btn.innerText = opt; btn.onclick = () => checkDictationAnswer(opt); container.appendChild(btn); });
  document.getElementById("dictation-feedback").innerHTML = "";
}
function checkDictationAnswer(selected) {
  const correct = dictationData[currentDictationIndex].correct;
  if (selected === correct) { dictationScore++; document.getElementById("dictation-feedback").innerHTML = '<span style="color:green;">✔️ صحيح!</span>'; }
  else { document.getElementById("dictation-feedback").innerHTML = `<span style="color:red;">❌ خطأ. الإجابة الصحيحة: ${correct}</span>`; }
  document.getElementById("next-dictation").style.display = "inline-block";
}
function nextDictation() { currentDictationIndex++; if (currentDictationIndex < dictationData.length) { loadDictationQuestion(); document.getElementById("next-dictation").style.display = "none"; } else { showDictationResult(); } }
function showDictationResult() { document.getElementById("dictation-result").innerHTML = `<h3>نتيجة اختبار الإملاء: ${dictationScore} من ${dictationData.length}</h3><button onclick="resetDictation()">إعادة الاختبار</button>`; document.getElementById("dictation-result").style.display = "block"; document.getElementById("dictation-options").style.display = "none"; document.getElementById("next-dictation").style.display = "none"; }
function resetDictation() { currentDictationIndex = 0; dictationScore = 0; document.getElementById("dictation-result").style.display = "none"; document.getElementById("dictation-options").style.display = "flex"; loadDictationQuestion(); }
if (document.getElementById("dictation-sentence")) loadDictationQuestion();
