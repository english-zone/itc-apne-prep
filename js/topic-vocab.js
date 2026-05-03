let currentQuestions = [];
let currentIndex = 0;
let score = 0;
let currentTopic = "family-body";

async function loadTopic(topic) {
    currentTopic = topic;
    try {
        const response = await fetch(`content/vocabulary/topics/${topic}.json`);
        if (!response.ok) throw new Error("File not found");
        const words = await response.json();
        currentQuestions = words.map(item => ({
            word: item.word,
            correct: item.correctMeaning,
            options: shuffleArray([item.correctMeaning, ...item.distractors]),
            example: item.example
        }));
        currentIndex = 0;
        score = 0;
        displayQuestion();
    } catch (err) {
        document.getElementById("quiz-area").innerHTML = `<p style="color:red;">خطأ في تحميل المفردات للموضوع ${topic}</p>`;
    }
}

function displayQuestion() {
    if (currentIndex >= currentQuestions.length) {
        document.getElementById("quiz-area").innerHTML = `<h3>نتيجة الاختبار: ${score} من ${currentQuestions.length}</h3><button onclick="resetQuiz()">إعادة المحاولة</button>`;
        return;
    }
    const q = currentQuestions[currentIndex];
    document.getElementById("question-text").innerHTML = `<strong>ما معنى كلمة: <span style="color:#0077cc;">${q.word}</span>؟</strong><br><div class="vocab-example">📖 مثال: ${q.example}</div>`;
    const optionsDiv = document.getElementById("options-area");
    optionsDiv.innerHTML = "";
    q.options.forEach(opt => {
        const btn = document.createElement("button");
        btn.innerText = opt;
        btn.className = "vocab-option-btn";
        btn.onclick = () => checkAnswer(opt);
        optionsDiv.appendChild(btn);
    });
    document.getElementById("feedback").innerHTML = "";
    document.getElementById("next-vocab-btn").style.display = "none";
}

function checkAnswer(selected) {
    const q = currentQuestions[currentIndex];
    const isCorrect = (selected === q.correct);
    if (isCorrect) {
        score++;
        document.getElementById("feedback").innerHTML = `<span class="correct-feedback">✅ صحيح! "${q.correct}"</span>`;
    } else {
        document.getElementById("feedback").innerHTML = `<span class="wrong-feedback">❌ خطأ. المعنى الصحيح: "${q.correct}"</span>`;
    }
    document.getElementById("next-vocab-btn").style.display = "inline-block";
}

function nextQuestion() {
    currentIndex++;
    displayQuestion();
}

function changeTopic() {
    const select = document.getElementById("topic-select");
    loadTopic(select.value);
}

function resetQuiz() {
    loadTopic(currentTopic);
}

function shuffleArray(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}

// بدء التحميل
loadTopic("family-body");
