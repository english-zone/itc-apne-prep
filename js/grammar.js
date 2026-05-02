// ========================
// GRAMMAR DATA (HARDCODED – لا تحميل خارجي)
// ========================

const GRAMMAR_TOPICS = [
  {
    id: "present-simple",
    title: "🟢 Present Simple Tense (المضارع البسيط)",
    rules: [
      "يستخدم للحقائق العامة والعادات والروتين اليومي.",
      "التكوين: الفعل في المصدر + (s/es) للضمائر he/she/it.",
      "النفي: do not (don't) / does not (doesn't) + الفعل المصدر.",
      "السؤال: Do/Does + الفاعل + المصدر؟"
    ],
    examples: [
      "I wake up at 6:00 every morning.",
      "She works at a hospital in Riyadh.",
      "The sun rises in the east.",
      "They don't eat meat on Fridays.",
      "Does he speak Arabic? Yes, he does.",
      "Water boils at 100 degrees Celsius."
    ],
    notes: "الكلمات المفتاحية: always, usually, often, sometimes, never, every day/week."
  },
  {
    id: "past-simple",
    title: "🔵 Past Simple Tense (الماضي البسيط)",
    rules: [
      "يستخدم لأحداث انتهت في الماضي.",
      "الأفعال المنتظمة: نضيف ed- (played, visited).",
      "الأفعال الشاذة: الصيغة الثانية (went, saw, bought).",
      "النفي: did not (didn't) + الفعل المصدر.",
      "السؤال: Did + الفاعل + المصدر؟"
    ],
    examples: [
      "I visited my grandmother yesterday.",
      "They bought a new car last week.",
      "She didn't watch the movie.",
      "Did you see Ali at the party?",
      "He went to London in 2019.",
      "We finished the project on time."
    ],
    notes: "الكلمات المفتاحية: yesterday, last night, in 2010, ago, previous."
  },
  {
    id: "present-continuous",
    title: "🟡 Present Continuous (المضارع المستمر)",
    rules: [
      "يستخدم لحدث يحدث الآن أو في الوقت الحالي.",
      "التكوين: am/is/are + الفعل + ing.",
      "النفي: am not/is not/are not + ing.",
      "السؤال: Am/Is/Are + الفاعل + ing؟"
    ],
    examples: [
      "I am studying English right now.",
      "She is cooking dinner at the moment.",
      "They are playing football in the garden.",
      "He isn't sleeping; he's reading.",
      "Are you listening to me?",
      "Look! It's raining outside."
    ],
    notes: "الكلمات المفتاحية: now, at the moment, today, this week, Look!, Listen!"
  },
  {
    id: "past-continuous",
    title: "🟠 Past Continuous (الماضي المستمر)",
    rules: [
      "يستخدم لحدث كان مستمراً في الماضي عندما حدث آخر.",
      "التكوين: was/were + الفعل + ing.",
      "النفي: was not/were not + ing.",
      "غالباً مع while أو when."
    ],
    examples: [
      "I was watching TV when the phone rang.",
      "While she was cooking, he was cleaning.",
      "They were sleeping at 11 PM last night.",
      "He wasn't working when I saw him.",
      "What were you doing at 8 o'clock?",
      "The children were playing outside."
    ],
    notes: "الكلمات المفتاحية: while, when, at [time] yesterday."
  },
  {
    id: "present-perfect",
    title: "🟣 Present Perfect (المضارع التام)",
    rules: [
      "يستخدم لحدث مرتبط بالحاضر (خبرة، تغيير، حدث بدأ بالماضي وما زال).",
      "التكوين: have/has + past participle (التصريف الثالث).",
      "النفي: haven't/hasn't + past participle."
    ],
    examples: [
      "I have visited Makkah three times.",
      "She has never eaten sushi.",
      "They have already finished their homework.",
      "Have you ever been to Dubai?",
      "He has lived in Jeddah since 2015.",
      "We haven't seen him today."
    ],
    notes: "الكلمات المفتاحية: ever, never, already, yet, since, for, just."
  },
  {
    id: "past-perfect",
    title: "🔴 Past Perfect (الماضي التام)",
    rules: [
      "يستخدم لحدث انتهى قبل حدث آخر في الماضي.",
      "التكوين: had + past participle.",
      "النفي: hadn't + past participle."
    ],
    examples: [
      "When I arrived, the train had already left.",
      "She had finished work before she went out.",
      "They had never seen such a beautiful place.",
      "He was tired because he had worked all day.",
      "Had you studied before the exam?",
      "By 10 PM, I had completed the report."
    ],
    notes: "الكلمات المفتاحية: already, just, never, by the time, before, after."
  },
  {
    id: "future-simple",
    title: "🟤 Future Simple (المستقبل البسيط)",
    rules: [
      "يستخدم للتوقع أو القرار اللحظي أو التكهن.",
      "التكوين: will + الفعل المصدر.",
      "النفي: will not (won't) + المصدر.",
      "أيضاً: be going to + مصدر (للخطط المستقبلية)."
    ],
    examples: [
      "I think it will rain tomorrow.",
      "She will call you later.",
      "They are going to buy a new house.",
      "He won't be late, I promise.",
      "Will you help me with this?",
      "Look at those clouds! It's going to snow."
    ],
    notes: "الكلمات المفتاحية: tomorrow, next week, soon, in the future, probably."
  },
  {
    id: "passive-voice",
    title: "📦 Passive Voice (المبني للمجهول)",
    rules: [
      "نستخدمه عندما نركز على المفعول به وليس الفاعل.",
      "التكوين: be (بصيغة مناسبة) + past participle.",
      "يُذكر الفاعل مع by إذا كان مهماً."
    ],
    examples: [
      "The cake was eaten by the children.",
      "This house was built in 1990.",
      "English is spoken all over the world.",
      "The letter will be sent tomorrow.",
      "The homework has been finished.",
      "A new bridge is being constructed."
    ],
    notes: "إذا كان الفاعل غير مهم أو مجهول نحذفه (مثال: My car was stolen)."
  },
  {
    id: "comparatives",
    title: "⚖️ Comparatives & Superlatives (المقارنة والتفضيل)",
    rules: [
      "Comparative: للمقارنة بين شيئين (adj+er / more + adj).",
      "Superlative: للأعلى درجة (the + adj+est / the most + adj).",
      "الكلمات القصيرة (مقطع واحد): taller, faster, biggest.",
      "الكلمات الطويلة (3 مقاطع فأكثر): more beautiful, the most expensive."
    ],
    examples: [
      "Ahmed is taller than Khalid.",
      "This test is more difficult than the last one.",
      "She is the smartest student in class.",
      "Mount Everest is the highest mountain.",
      "My phone is newer than yours.",
      "This is the most delicious food I've ever eaten."
    ],
    notes: "قاعدة: good → better → best, bad → worse → worst, far → farther/further."
  },
  {
    id: "gerunds-infinitives",
    title: "🔁 Gerunds & Infinitives (المصادر)",
    rules: [
      "Gerund (فعل + ing) يأتي بعد أفعال معينة (enjoy, mind, avoid).",
      "Infinitive (to + مصدر) بعد أفعال أخرى (want, decide, promise).",
      "بعض الأفعال يتغير المعنى (stop, remember, forget)."
    ],
    examples: [
      "I enjoy reading books.",
      "She decided to study medicine.",
      "Stop smoking (توقف عن التدخين).",
      "He stopped to smoke (توقف ليدخن).",
      "I remember locking the door (أتذكر أنني أقفلت الباب).",
      "Please remember to lock the door (تذكر أن تقفل الباب)."
    ],
    notes: "بعد حروف الجر نستخدم Gerund: interested in learning, good at swimming."
  },
  {
    id: "question-tags",
    title: "❓ Question Tags (ذيل السؤال)",
    rules: [
      "تستخدم للتأكيد أو طلب الموافقة.",
      "إذا كانت الجملة مثبتة، السؤال منفي (isn't it? aren't they?).",
      "إذا كانت الجملة منفية، السؤال مثبت (is it? does he?).",
      "الضمير والفعل المساعد يتطابقان مع الجملة الأصلية."
    ],
    examples: [
      "You are coming, aren't you?",
      "She doesn't like coffee, does she?",
      "They have finished, haven't they?",
      "He can swim, can't he?",
      "Let's go, shall we?",
      "I'm right, aren't I?"
    ],
    notes: "مع I'm نستخدم aren't I (نادراً am I not)."
  },
  {
    id: "pronouns",
    title: "👤 Pronouns (الضمائر)",
    rules: [
      "Subject pronouns: I, you, he, she, it, we, they (فاعل).",
      "Object pronouns: me, you, him, her, it, us, them (مفعول به).",
      "Possessive adjectives: my, your, his, her, its, our, their (ملكية قبل الاسم).",
      "Possessive pronouns: mine, yours, his, hers, ours, theirs (بدون اسم)."
    ],
    examples: [
      "She gave me her book. (She فاعل، me مفعول، her ملكية)",
      "This phone is mine, not yours.",
      "They invited us to their party.",
      "I love my mother.",
      "Is this bag yours or his?",
      "We saw them at the mall."
    ],
    notes: "الفرق: It's my car (الصفة) / The car is mine (الضمير)."
  },
  {
    id: "used-to",
    title: "⏮️ Used to (عادة في الماضي)",
    rules: [
      "يستخدم لعادات أو حالات كانت موجودة في الماضي ولكنها انتهت.",
      "التكوين: used to + المصدر.",
      "النفي: didn't use to + المصدر.",
      "السؤال: Did + فاعل + use to + مصدر؟"
    ],
    examples: [
      "I used to play football every day when I was young.",
      "She used to live in a small village.",
      "He didn't use to like vegetables, but now he does.",
      "Did you use to smoke?",
      "There used to be a cinema here.",
      "We used to go fishing every summer."
    ],
    notes: "لا تخلط بين used to (عادة ماضية) و be used to (اعتياد على شيء)."
  },
  {
    id: "prepositions",
    title: "📍 Prepositions (حروف الجر)",
    rules: [
      "حروف الجر للزمان: at (ساعة), on (يوم), in (شهر/سنة).",
      "حروف الجر للمكان: at (نقطة), on (سطح), in (داخل), next to, between.",
      "بعض الأفعال تأتي بحرف جر ثابت (depend on, listen to, laugh at)."
    ],
    examples: [
      "The meeting is at 3 PM on Monday in May.",
      "She is sitting on the chair in the room.",
      "I'm interested in learning English.",
      "He apologized for being late.",
      "They are waiting for the bus.",
      "It depends on the weather."
    ],
    notes: "احفظ الأفعال مع حروف الجر: look at, look for, look after, belong to, etc."
  },
  {
    id: "another-other",
    title: "🔁 Another / Other / Others",
    rules: [
      "Another = واحد آخر (مع مفرد).",
      "Other = آخر/آخرون (مع جمع أو غير معدود).",
      "Others = آخرون (ضمير جمع).",
      "The other = الآخر (معين)."
    ],
    examples: [
      "I'd like another cup of tea.",
      "Do you have any other questions?",
      "Some people like coffee; others prefer tea.",
      "One shoe is here, but where is the other?",
      "Let's meet another day.",
      "Other people think differently."
    ],
    notes: "Another + singular countable; Other + plural/uncountable."
  },
  {
    id: "modals",
    title: "🎯 Modal Verbs (الأفعال الناقصة)",
    rules: [
      "can = يستطيع / قدرة.",
      "could = استطاع في الماضي / طلب مهذب.",
      "must = يجب / إلزام.",
      "should = ينبغي / نصيحة.",
      "may/might = ربما / احتمال.",
      "have to = مضطر (إلزام خارجي)."
    ],
    examples: [
      "I can speak three languages.",
      "You must stop at the red light.",
      "She should see a doctor.",
      "It may rain tomorrow.",
      "They have to wake up early.",
      "Could you help me, please?"
    ],
    notes: "mustn't = ممنوع، don't have to = ليس مضطراً."
  },
  {
    id: "conditionals",
    title: "⚡ Conditionals (الجمل الشرطية)",
    rules: [
      "Type 0: حقائق عامة (If + present, present).",
      "Type 1: احتمال حقيقي (If + present, will + مصدر).",
      "Type 2: تخيل غير حقيقي (If + past, would + مصدر).",
      "Type 3: ندم على الماضي (If + past perfect, would have + pp)."
    ],
    examples: [
      "If you heat water, it boils. (Type 0)",
      "If it rains, we will stay home. (Type 1)",
      "If I were rich, I would travel the world. (Type 2)",
      "If she had studied, she would have passed. (Type 3)",
      "Unless you hurry, you'll be late. (unless = if not)",
      "I would have called you if I had known."
    ],
    notes: "في Type 2 نستخدم were لجميع الضمائر (If I were you)."
  }
];

// Irregular verbs list (110 verbs from ITC book)
const IRREGULAR_VERBS = [
  { base: "be", past: "was/were", pp: "been" },
  { base: "beat", past: "beat", pp: "beaten" },
  { base: "become", past: "became", pp: "become" },
  { base: "begin", past: "began", pp: "begun" },
  { base: "bend", past: "bent", pp: "bent" },
  { base: "bet", past: "bet", pp: "bet" },
  { base: "bite", past: "bit", pp: "bitten" },
  { base: "bleed", past: "bled", pp: "bled" },
  { base: "blow", past: "blew", pp: "blown" },
  { base: "break", past: "broke", pp: "broken" },
  { base: "bring", past: "brought", pp: "brought" },
  { base: "build", past: "built", pp: "built" },
  { base: "burn", past: "burnt/burned", pp: "burnt/burned" },
  { base: "buy", past: "bought", pp: "bought" },
  { base: "catch", past: "caught", pp: "caught" },
  { base: "choose", past: "chose", pp: "chosen" },
  { base: "come", past: "came", pp: "come" },
  { base: "cost", past: "cost", pp: "cost" },
  { base: "cut", past: "cut", pp: "cut" },
  { base: "dig", past: "dug", pp: "dug" },
  { base: "do", past: "did", pp: "done" },
  { base: "draw", past: "drew", pp: "drawn" },
  { base: "dream", past: "dreamt/dreamed", pp: "dreamt/dreamed" },
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
  { base: "forgive", past: "forgave", pp: "forgiven" },
  { base: "freeze", past: "froze", pp: "frozen" },
  { base: "get", past: "got", pp: "got/gotten" },
  { base: "give", past: "gave", pp: "given" },
  { base: "go", past: "went", pp: "gone" },
  { base: "grow", past: "grew", pp: "grown" },
  { base: "hang", past: "hung", pp: "hung" },
  { base: "have", past: "had", pp: "had" },
  { base: "hear", past: "heard", pp: "heard" },
  { base: "hide", past: "hid", pp: "hidden" },
  { base: "hit", past: "hit", pp: "hit" },
  { base: "hold", past: "held", pp: "held" },
  { base: "hurt", past: "hurt", pp: "hurt" },
  { base: "keep", past: "kept", pp: "kept" },
  { base: "kneel", past: "knelt", pp: "knelt" },
  { base: "know", past: "knew", pp: "known" },
  { base: "lay", past: "laid", pp: "laid" },
  { base: "lead", past: "led", pp: "led" },
  { base: "learn", past: "learnt/learned", pp: "learnt/learned" },
  { base: "leave", past: "left", pp: "left" },
  { base: "lend", past: "lent", pp: "lent" },
  { base: "let", past: "let", pp: "let" },
  { base: "lie", past: "lay", pp: "lain" },
  { base: "light", past: "lit", pp: "lit" },
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
  { base: "stick", past: "stuck", pp: "stuck" },
  { base: "strike", past: "struck", pp: "struck" },
  { base: "swim", past: "swam", pp: "swum" },
  { base: "take", past: "took", pp: "taken" },
  { base: "teach", past: "taught", pp: "taught" },
  { base: "tear", past: "tore", pp: "torn" },
  { base: "tell", past: "told", pp: "told" },
  { base: "think", past: "thought", pp: "thought" },
  { base: "throw", past: "threw", pp: "thrown" },
  { base: "understand", past: "understood", pp: "understood" },
  { base: "wake", past: "woke", pp: "woken" },
  { base: "wear", past: "wore", pp: "worn" },
  { base: "win", past: "won", pp: "won" },
  { base: "write", past: "wrote", pp: "written" }
];

// ========================
// RENDER EVERYTHING
// ========================

document.addEventListener('DOMContentLoaded', () => {
  initApp();  // from app.js
  renderIrregularVerbs();
  renderGrammarTopics();
});

function renderIrregularVerbs() {
  const container = document.getElementById('irregularVerbsContent');
  if (!container) return;
  let html = `
    <p style="margin-bottom: 1rem;"><strong>📖 قائمة الأفعال الشاذة (Irregular Verbs) – أكثر من 100 فعل</strong><br>
    احفظ التصريف الثاني (Past) والثالث (Past Participle) جيداً.</p>
    <div style="overflow-x: auto;">
      <table class="irregular-table">
        <thead><tr><th>Base Form (المصدر)</th><th>Past Simple (الماضي)</th><th>Past Participle (التصريف الثالث)</th></tr></thead>
        <tbody>
  `;
  IRREGULAR_VERBS.forEach(v => {
    html += `<tr><td>${v.base}</td><td>${v.past}</td><td>${v.pp}</td></tr>`;
  });
  html += `
        </tbody>
      </table>
    </div>
    <p class="badge-example">💡 نصيحة: كوّن جملة بكل فعل لتحفظه بسرعة.</p>
  `;
  container.innerHTML = html;
}

function renderGrammarTopics() {
  const container = document.getElementById('grammarTopics');
  if (!container) return;
  let html = '';
  GRAMMAR_TOPICS.forEach(topic => {
    html += `
      <div class="grammar-card">
        <div class="grammar-card-header" onclick="toggleGrammarCard(this)">
          ${topic.title}
          <span>▼</span>
        </div>
        <div class="grammar-card-content">
          <div class="rules">
            <strong>📌 القواعد:</strong>
            <ul>${topic.rules.map(r => `<li>${r}</li>`).join('')}</ul>
          </div>
          <div class="examples">
            <strong>📝 أمثلة كثيرة:</strong>
            ${topic.examples.map(ex => `<div class="example-box"><strong>→</strong> ${ex}</div>`).join('')}
          </div>
          ${topic.notes ? `<div class="notes"><strong>⚠️ ملاحظة:</strong> ${topic.notes}</div>` : ''}
        </div>
      </div>
    `;
  });
  container.innerHTML = html;
}

window.toggleGrammarCard = function(header) {
  const content = header.nextElementSibling;
  const arrow = header.querySelector('span');
  if (content.classList.contains('active')) {
    content.classList.remove('active');
    arrow.innerHTML = '▼';
  } else {
    content.classList.add('active');
    arrow.innerHTML = '▲';
  }
};
