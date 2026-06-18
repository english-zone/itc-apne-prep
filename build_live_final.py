import json, os, re

REPO = "/workspaces/itc-apne-prep"

def load_json(path):
    full = os.path.join(REPO, path)
    if not os.path.exists(full): return None
    with open(full, encoding="utf-8") as f: return json.load(f)

# --- تحميل البيانات ---
reading_data = load_json("content/day-07/reading.json")
yellowstone = None
if reading_data:
    for p in reading_data.get("passages", []):
        if "Yellowstone" in p.get("title", ""): yellowstone = p; break
    if not yellowstone:
        passages = reading_data.get("passages", [])
        yellowstone = passages[1] if len(passages) > 1 else passages[0]

grammar_qs = []
for day in [1, 2, 3]:
    data = load_json(f"content/day-{day:02d}/grammar-test.json")
    if data:
        items = data.get("questions", data) if isinstance(data, dict) else data
        grammar_qs.extend(items[:2])
    if len(grammar_qs) >= 5: break
grammar_qs = grammar_qs[:5]

vocab_qs = []
for day in [1, 2]:
    data = load_json(f"content/day-{day:02d}/vocabulary.json")
    if data:
        for w in data.get("words", []):
            q_obj = w.get("question")
            if q_obj and isinstance(q_obj, dict) and "q" in q_obj and "options" in q_obj:
                if "answer" not in q_obj:
                    q_obj["answer"] = 0
                vocab_qs.append(q_obj)
                if len(vocab_qs) >= 5: break
    if len(vocab_qs) >= 5: break

dict_qs = []
for day in [1, 2, 3]:
    data = load_json(f"content/day-{day:02d}/dictation.json")
    if data:
        for w in data.get("words", []):
            if isinstance(w, dict) and w.get("correct") and w.get("options"):
                dict_qs.append({"correct": w["correct"], "options": w["options"]})
            if len(dict_qs) >= 8: break
    if len(dict_qs) >= 8: break

passage_title = yellowstone["title"] if yellowstone else "Yellowstone National Park"
passage_text  = yellowstone["text"] if yellowstone else ""
reading_qs    = yellowstone.get("questions", [])[:5] if yellowstone else []

sentences = re.split(r'(?<=[.!?])\s+', passage_text.strip())
passage_sentences_html = ""
for i, sent in enumerate(sentences, 1):
    passage_sentences_html += f'<span id="s{i}" class="sentence">{sent}</span>\n'

answer_sentence = {1: 1, 2: 6, 3: 7, 4: 11, 5: 2}

grammar_explanations = {
    1: """<h4>📘 Present Simple – المضارع البسيط</h4><p><strong>القاعدة:</strong> مع الضمائر <em>he, she, it</em> يُضاف <strong>-s</strong> أو <strong>-es</strong> للفعل.</p><ul><li>✅ <strong>goes</strong>: الصيغة الصحيحة.</li><li>❌ <strong>go</strong>: للجمع.</li><li>❌ <strong>going</strong>: يحتاج is.</li><li>❌ <strong>gone</strong>: تصريف ثالث.</li></ul>""",
    2: """<h4>📘 Past Perfect – الماضي التام</h4><p><strong>القاعدة:</strong> <strong>had + V3</strong> لحدث قبل آخر في الماضي.</p><ul><li>✅ <strong>had</strong>: المغادرة قبل وصوله.</li><li>❌ <strong>has/have</strong>: مضارع.</li><li>❌ <strong>was</strong>: لا يصلح.</li></ul>""",
    3: """<h4>📘 Second Conditional – الشرطية الثانية</h4><p><strong>القاعدة:</strong> <strong>If + were/V2, would + V1</strong>.</p><ul><li>✅ <strong>were</strong>: الصيغة القياسية.</li><li>❌ <strong>am/was/be</strong>: لا تصلح.</li></ul>""",
    4: """<h4>📘 Passive Voice – المبني للمجهول</h4><p><strong>القاعدة:</strong> <strong>was/were + V3</strong> للماضي.</p><ul><li>✅ <strong>was</strong>: مفرد ماضٍ.</li><li>❌ <strong>is/were/has been</strong>: لا تتوافق.</li></ul>""",
    5: """<h4>📘 Neither...nor – توافق الفعل</h4><p><strong>القاعدة:</strong> الفعل يتبع <strong>أقرب فاعل</strong>.</p><ul><li>✅ <strong>was</strong>: أقرب فاعل مفرد.</li><li>❌ <strong>are/were/is</strong>: لا تتوافق.</li></ul>"""
}

def make_q_card(num, q_text, options, answer_idx, sentence_id=None, explanation=None):
    if not isinstance(answer_idx, int) or answer_idx < 0 or answer_idx >= len(options):
        answer_idx = 0
    correct_text = options[answer_idx]
    opts_html = ""
    for j, opt in enumerate(options):
        letter = chr(65 + j)
        is_correct = "true" if j == answer_idx else "false"
        opts_html += f'<div class="opt" data-correct="{is_correct}"><span class="opt-letter">{letter}</span><span class="opt-text">{opt}</span></div>\n'
    sent_attr = f' data-sentence="s{sentence_id}"' if sentence_id else ""
    explanation_html = f'<div class="ans-explanation">{explanation}</div>' if explanation else ""
    return f"""<div class="q-card"{sent_attr}><div class="q-text en"><span class="q-num">{num}</span> {q_text}</div><div class="options ltr-block">{opts_html}</div><div class="ans-correct">✅ الإجابة الصحيحة: <strong class="ltr-inline">{correct_text}</strong></div><div class="ans-wrong">❌ الخيارات الأخرى غير صحيحة.</div>{explanation_html}</div>"""

reading_cards = ""
for i, q in enumerate(reading_qs, 1):
    sent = answer_sentence.get(i)
    reading_cards += make_q_card(i, q["q"], q["options"], q.get("answer", 0), sentence_id=sent)

grammar_cards = ""
for i, q in enumerate(grammar_qs, 1):
    explanation = grammar_explanations.get(i, None)
    grammar_cards += make_q_card(i, q["q"], q["options"], q.get("answer", 0), explanation=explanation)

vocab_cards = ""
for i, q in enumerate(vocab_qs, 1):
    vocab_cards += make_q_card(i, q["q"], q["options"], q.get("answer", 0))

dict_cards = ""
for i, item in enumerate(dict_qs, 1):
    correct = item["correct"]
    opts = item["options"]
    ans_idx = opts.index(correct) if correct in opts else 0
    dict_cards += make_q_card(i, "Which spelling is correct?", opts, ans_idx)

html = """<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>APNE-ITC English Preparation – Live Session</title>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--primary:#0b2b4f;--accent:#0071e3;--green:#16a34a;--green-light:#dcfce7;--green-dark:#14532d;--red:#dc2626;--red-light:#fee2e2;--red-dark:#7f1d1d;--gold:#d97706;--gold-light:#fef3c7;--gray:#64748b;--border:#e2e8f0;--bg:#f8fafc;--card-shadow:0 2px 12px rgba(0,0,0,0.06);--highlight-yellow:#fff176;--explain-bg:#f0f8ff}
body{font-family:'Cairo',sans-serif;background:var(--bg);color:#1e293b;line-height:1.8}
.ar{direction:rtl;text-align:right;font-family:'Cairo',sans-serif;unicode-bidi:isolate}
.en,.ltr-block{direction:ltr;text-align:left;font-family:'Inter',sans-serif;unicode-bidi:isolate}
.ltr-inline{display:inline;direction:ltr;unicode-bidi:embed}
.hero{background:linear-gradient(135deg,#0b2b4f 0%,#1a4a8a 55%,#0071e3 100%);color:#fff;padding:3rem 2rem 2.5rem;text-align:center;direction:rtl}
.hero img{height:64px;margin-bottom:0.8rem;display:block;margin-inline:auto}
.hero h1{font-size:clamp(1.7rem,4vw,2.5rem);font-weight:900;font-family:'Inter',sans-serif;letter-spacing:-0.5px;margin-bottom:0.4rem;direction:ltr}
.hero .trainer{font-size:1.05rem;opacity:0.88;margin-bottom:0.6rem}
.hero .contact{font-size:0.95rem;opacity:0.78;margin-bottom:1.2rem}
.hero .badges{display:flex;justify-content:center;gap:0.7rem;flex-wrap:wrap;margin-top:1rem}
.hero .badge{background:rgba(255,255,255,0.13);border:1px solid rgba(255,255,255,0.22);border-radius:50px;padding:0.35rem 0.9rem;font-size:0.88rem}
.container{max-width:1000px;margin:0 auto;padding:2rem 1.5rem 5rem}
.sec-header{display:flex;align-items:center;gap:0.9rem;margin:3.5rem 0 1.6rem;padding-bottom:0.9rem;border-bottom:2px solid var(--border);direction:rtl}
.sec-icon{width:44px;height:44px;background:#e8f1fd;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.3rem;flex-shrink:0}
.sec-title-ar{font-size:1.4rem;font-weight:700;color:var(--primary)}
.sec-title-en{font-size:0.92rem;color:var(--gray);font-family:'Inter',sans-serif;direction:ltr;font-weight:500}
.passage-box{background:#fff;border-radius:16px;border:1px solid var(--border);box-shadow:var(--card-shadow);overflow:hidden;margin-bottom:2rem;direction:ltr}
.passage-header{background:var(--primary);color:#fff;padding:0.9rem 1.5rem;font-family:'Inter',sans-serif;font-size:1.05rem;font-weight:700;direction:ltr;text-align:left}
.passage-body{padding:1.5rem;font-family:'Inter',sans-serif;font-size:0.97rem;line-height:2.2;color:#334155;direction:ltr;text-align:left}
.sentence{display:inline;padding:1px 3px;border-radius:2px;transition:background 0.3s}
.sentence.highlight{background:var(--highlight-yellow);padding:1px 6px;box-shadow:0 0 4px rgba(0,0,0,0.1)}
.q-card{background:#fff;border-radius:16px;border:1px solid var(--border);padding:1.4rem 1.5rem 1.2rem;margin:1.2rem 0;box-shadow:var(--card-shadow)}
.q-num{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;background:var(--accent);color:#fff;border-radius:50%;font-size:0.88rem;font-weight:700;flex-shrink:0;margin-inline-end:0.5rem;font-family:'Inter',sans-serif}
.q-text{font-size:1.02rem;font-weight:600;color:var(--primary);margin-bottom:1rem;display:flex;align-items:flex-start;gap:0.4rem}
.options{display:grid;grid-template-columns:1fr 1fr;gap:0.55rem;margin:0.6rem 0 1rem;direction:ltr;text-align:left}
@media(max-width:560px){.options{grid-template-columns:1fr}}
.opt{display:flex;align-items:center;gap:0.5rem;padding:0.6rem 0.9rem;background:#f1f5f9;border:1.5px solid #e2e8f0;border-radius:10px;cursor:pointer;transition:background 0.18s,border-color 0.18s;direction:ltr;text-align:left;user-select:none}
.opt:hover{background:#e0e7f0;border-color:var(--accent)}
.opt-letter{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;background:#cbd5e1;color:#334155;border-radius:6px;font-size:0.8rem;font-weight:700;font-family:'Inter',sans-serif;flex-shrink:0}
.opt-text{font-family:'Inter',sans-serif;font-size:0.94rem;color:#334155;direction:ltr}
.opt[data-correct="true"].revealed-correct{background:var(--green-light);border-color:var(--green)}
.opt[data-correct="true"].revealed-correct .opt-letter{background:var(--green);color:#fff}
.opt[data-correct="true"].revealed-correct .opt-text{color:var(--green-dark);font-weight:600}
.ans-correct,.ans-wrong,.ans-explanation{display:none;border-radius:10px;padding:0.75rem 1rem;margin-top:0.6rem;font-size:0.94rem;direction:rtl;text-align:right}
.q-card.revealed .ans-correct{display:block;background:var(--green-light);border-right:4px solid var(--green);color:var(--green-dark)}
.q-card.revealed .ans-wrong{display:block;background:var(--red-light);border-right:4px solid var(--red);color:var(--red-dark)}
.q-card.revealed .ans-explanation{display:block;background:var(--explain-bg);border:1px solid var(--accent);border-right:4px solid var(--accent);margin-top:0.8rem}
.ans-explanation h4{color:var(--primary);margin-bottom:0.5rem;font-size:1.05rem}
.ans-explanation ul{padding-right:1.5rem;margin:0.5rem 0}
.ans-explanation li{margin-bottom:0.3rem}
.tips-box{background:linear-gradient(135deg,#0b2b4f,#1a4a8a);color:#fff;border-radius:20px;padding:2rem 1.5rem;margin-top:3rem;direction:rtl;text-align:right}
.tips-box h3{font-size:1.25rem;font-weight:700;margin-bottom:1.2rem;text-align:center}
.tips-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:1rem}
.tip-item{background:rgba(255,255,255,0.1);border-radius:12px;padding:1rem;font-size:0.9rem;text-align:center}
.tip-icon{font-size:1.6rem;display:block;margin-bottom:0.4rem}
.print-btn{text-align:center;margin:2rem 0}
.print-btn button{background:var(--accent);color:#fff;border:none;padding:0.75rem 2.5rem;font-size:1rem;font-family:'Cairo',sans-serif;font-weight:700;border-radius:50px;cursor:pointer;box-shadow:0 4px 14px rgba(0,113,227,0.3);transition:opacity 0.2s}
.print-btn button:hover{opacity:0.88}
.golden-tip{background:var(--gold-light);border-right:4px solid var(--gold);border-radius:10px;padding:1.2rem;margin:1.5rem 0;direction:rtl}
.golden-tip h4{font-size:1.1rem;margin-bottom:0.5rem}
.golden-tip p{margin-bottom:0.5rem}
#drawCanvas{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:9998;cursor:crosshair;display:none;pointer-events:none}
#drawCanvas.active{display:block;pointer-events:all}
#drawToolbar{position:fixed;top:12px;left:50%;transform:translateX(-50%);z-index:10000;background:rgba(15,23,42,0.92);border-radius:50px;padding:0.5rem 1.2rem;display:none;align-items:center;gap:0.8rem;backdrop-filter:blur(10px);box-shadow:0 4px 20px rgba(0,0,0,0.35)}
#drawToolbar.active{display:flex}
#drawToolbar button{background:transparent;border:1px solid rgba(255,255,255,0.3);color:#fff;border-radius:20px;padding:0.4rem 0.85rem;cursor:pointer;font-family:'Cairo',sans-serif;font-size:0.85rem;transition:background 0.15s}
#drawToolbar button:hover{background:rgba(255,255,255,0.2)}
#drawToolbar input[type="color"]{width:28px;height:28px;border-radius:50%;padding:0;border:2px solid rgba(255,255,255,0.6);cursor:pointer;background:none}
#drawToolbar input[type="range"]{width:80px;accent-color:#0071e3}
#toggleDrawBtn{position:fixed;bottom:24px;right:24px;z-index:10000;background:var(--accent);color:#fff;border:none;padding:12px 22px;border-radius:50px;font-family:'Cairo',sans-serif;font-size:1rem;font-weight:700;cursor:pointer;box-shadow:0 4px 18px rgba(0,113,227,0.45);transition:background 0.2s,transform 0.1s;display:flex;align-items:center;gap:0.4rem}
#toggleDrawBtn:hover{transform:scale(1.04)}
#toggleDrawBtn.drawing{background:#dc2626;box-shadow:0 4px 18px rgba(220,38,38,0.45)}
@media print{#toggleDrawBtn,#drawToolbar,#drawCanvas,.print-btn,.hero .badges{display:none!important}body{background:#fff}.q-card.revealed .ans-correct,.q-card.revealed .ans-wrong,.q-card.revealed .ans-explanation{display:block!important}@page{margin:1.5cm}}
</style>
</head>
<body>
<button id="toggleDrawBtn" onclick="toggleDrawing()">🖊️ وضع الرسم</button>
<div id="drawToolbar"><input type="color" id="penColor" value="#e63946" title="لون القلم"><input type="range" id="penSize" min="1" max="16" value="3" title="سُمك القلم"><button onclick="undoLast()">↩ تراجع</button><button onclick="clearCanvas()">🗑️ مسح الكل</button></div>
<canvas id="drawCanvas"></canvas>
<header class="hero">
<img src="assets/images/reyadah-logo.png" alt="شعار معهد الريادة" onerror="this.style.display='none'">
<h1>APNE&#8209;ITC&nbsp;English&nbsp;Preparation</h1>
<p class="trainer">مع المدرب: أ. أنس عبدالرحمن | معهد الريادة للتدريب</p>
<p class="contact">للتسجيل: <span class="ltr-inline">0546088130</span> – <span class="ltr-inline">0548775199</span></p>
<div class="badges"><span class="badge">📖 قراءة</span><span class="badge">📘 قواعد</span><span class="badge">🧠 مفردات</span><span class="badge">✍️ إملاء</span></div>
</header>
<div class="container">
<div class="sec-header ar"><div class="sec-icon">📖</div><div><div class="sec-title-ar">قسم القراءة</div><div class="sec-title-en">Reading Comprehension</div></div></div>
<div class="passage-box"><div class="passage-header en">""" + passage_title + """</div><div class="passage-body en">""" + passage_sentences_html + """</div></div>
<div class="golden-tip"><h4>💡 نصيحة ذهبية: Skimming vs Scanning</h4><p><strong>Skimming:</strong> 30-60 ثانية لتفهم الفكرة العامة.</p><p><strong>Scanning:</strong> 10-20 ثانية للبحث عن كلمة مفتاحية.</p><p>⏱️ <strong>الوقت النموذجي:</strong> 60-90 ثانية لكل سؤال.</p></div>
""" + reading_cards + """
<div class="sec-header ar"><div class="sec-icon">📘</div><div><div class="sec-title-ar">قسم القواعد</div><div class="sec-title-en">Grammar</div></div></div>
""" + grammar_cards + """
<div class="sec-header ar"><div class="sec-icon">🧠</div><div><div class="sec-title-ar">قسم المفردات</div><div class="sec-title-en">Vocabulary</div></div></div>
""" + vocab_cards + """
<div class="sec-header ar"><div class="sec-icon">✍️</div><div><div class="sec-title-ar">قسم الإملاء</div><div class="sec-title-en">Spelling &amp; Dictation</div></div></div>
<p class="ar" style="color:var(--gray);margin-bottom:1rem">اختر التهجئة الصحيحة لكل كلمة:</p>
""" + dict_cards + """
<div class="print-btn"><button onclick="revealAll();setTimeout(()=>window.print(),300)">🖨️ كشف الإجابات وطباعة</button></div>
<div class="tips-box"><h3>💡 نصائح للاستفادة القصوى من الاختبار</h3><div class="tips-grid"><div class="tip-item"><span class="tip-icon">📖</span>اقرأ النص كاملاً قبل الإجابة</div><div class="tip-item"><span class="tip-icon">✏️</span>حدّد الكلمات المفتاحية في كل سؤال</div><div class="tip-item"><span class="tip-icon">⏱️</span>لا تقضِ وقتاً طويلاً على سؤال واحد</div><div class="tip-item"><span class="tip-icon">🔄</span>راجع إجاباتك قبل التسليم</div></div></div>
</div>
<script>
(function () {
"use strict";
function revealCard(card) {
  if (card.classList.contains("revealed")) return;
  card.classList.add("revealed");
  var correct = card.querySelector('.opt[data-correct="true"]');
  if (correct) correct.classList.add("revealed-correct");
  var sentId = card.getAttribute("data-sentence");
  if (sentId) {
    document.querySelectorAll(".sentence.highlight").forEach(function (el) { el.classList.remove("highlight"); });
    var sent = document.getElementById(sentId);
    if (sent) { sent.classList.add("highlight"); sent.scrollIntoView({ behavior: "smooth", block: "center" }); }
  }
}
document.querySelectorAll(".q-card").forEach(function (card) {
  card.querySelectorAll(".opt").forEach(function (opt) {
    opt.addEventListener("click", function () { revealCard(card); });
  });
});
window.revealAll = function () { document.querySelectorAll(".q-card").forEach(revealCard); };

var canvas  = document.getElementById("drawCanvas");
var ctx     = canvas.getContext("2d");
var drawing = false, color = "#e63946", size = 3, strokes = [], currentStroke = [];
function resizeCanvas() {
  var img = ctx.getImageData(0, 0, canvas.width, canvas.height);
  canvas.width  = window.innerWidth;
  canvas.height = window.innerHeight;
  ctx.putImageData(img, 0, 0);
}
window.addEventListener("resize", resizeCanvas);
canvas.width  = window.innerWidth;
canvas.height = window.innerHeight;
document.getElementById("penColor").addEventListener("input", function (e) { color = e.target.value; });
document.getElementById("penSize").addEventListener("input", function (e) { size = parseInt(e.target.value); });
function startDraw(x, y) { drawing = true; currentStroke = [{ x: x, y: y }]; ctx.beginPath(); ctx.moveTo(x, y); }
function continueDraw(x, y) { if (!drawing) return; ctx.strokeStyle = color; ctx.lineWidth = size; ctx.lineCap = "round"; ctx.lineJoin = "round"; ctx.lineTo(x, y); ctx.stroke(); currentStroke.push({ x: x, y: y, c: color, s: size }); }
function stopDraw() { if (!drawing) return; drawing = false; if (currentStroke.length > 1) strokes.push(currentStroke.slice()); currentStroke = []; ctx.beginPath(); }
canvas.addEventListener("mousedown", function (e) { startDraw(e.clientX, e.clientY); });
canvas.addEventListener("mousemove", function (e) { continueDraw(e.clientX, e.clientY); });
canvas.addEventListener("mouseup", stopDraw);
window.addEventListener("mouseup", stopDraw);
canvas.addEventListener("mouseleave", function () { if (drawing) ctx.beginPath(); });
canvas.addEventListener("touchstart", function (e) { e.preventDefault(); var t = e.touches[0]; startDraw(t.clientX, t.clientY); }, { passive: false });
canvas.addEventListener("touchmove", function (e) { e.preventDefault(); var t = e.touches[0]; continueDraw(t.clientX, t.clientY); }, { passive: false });
canvas.addEventListener("touchend", function (e) { e.preventDefault(); stopDraw(); }, { passive: false });
function redrawAll() { ctx.clearRect(0, 0, canvas.width, canvas.height); strokes.forEach(function (stroke) { if (stroke.length < 2) return; ctx.beginPath(); ctx.moveTo(stroke[0].x, stroke[0].y); for (var i = 1; i < stroke.length; i++) { ctx.strokeStyle = stroke[i].c || color; ctx.lineWidth = stroke[i].s || size; ctx.lineCap = "round"; ctx.lineJoin = "round"; ctx.lineTo(stroke[i].x, stroke[i].y); ctx.stroke(); ctx.beginPath(); ctx.moveTo(stroke[i].x, stroke[i].y); } }); }
window.clearCanvas = function () { ctx.clearRect(0, 0, canvas.width, canvas.height); strokes = []; };
window.undoLast = function () { if (strokes.length === 0) return; strokes.pop(); redrawAll(); };
window.toggleDrawing = function () {
  var btn = document.getElementById("toggleDrawBtn");
  var toolbar = document.getElementById("drawToolbar");
  var isOn = canvas.classList.contains("active");
  if (isOn) { canvas.classList.remove("active"); toolbar.classList.remove("active"); btn.classList.remove("drawing"); btn.innerHTML = "🖊️ وضع الرسم"; drawing = false; }
  else { canvas.classList.add("active"); toolbar.classList.add("active"); btn.classList.add("drawing"); btn.innerHTML = "✋ إيقاف الرسم"; }
};
})();
</script>
</body>
</html>"""

out_path = os.path.join(REPO, "live_session.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)
print("✅ live_session.html built with all fixes")
