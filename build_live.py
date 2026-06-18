import json, os

REPO = "/workspaces/itc-apne-prep"

def load_json(path):
    full = os.path.join(REPO, path)
    if not os.path.exists(full):
        return None
    with open(full, encoding="utf-8") as f:
        return json.load(f)

# --- تحميل البيانات ---
reading_data = load_json("content/day-07/reading.json")
yellowstone = None
if reading_data:
    for p in reading_data.get("passages", []):
        if "Yellowstone" in p.get("title", ""):
            yellowstone = p
            break
    if not yellowstone:
        passages = reading_data.get("passages", [])
        yellowstone = passages[1] if len(passages) > 1 else passages[0]

grammar_qs = []
for day in [1, 2, 3]:
    data = load_json(f"content/day-{day:02d}/grammar-test.json")
    if data:
        items = data.get("questions", data) if isinstance(data, dict) else data
        grammar_qs.extend(items[:2])
    if len(grammar_qs) >= 5:
        break
grammar_qs = grammar_qs[:5]

vocab_qs = []
for day in [1, 2]:
    data = load_json(f"content/day-{day:02d}/vocabulary.json")
    if data:
        for w in data.get("words", []):
            if "question" in w:
                vocab_qs.append(w["question"])
                if len(vocab_qs) >= 5:
                    break
    if len(vocab_qs) >= 5:
        break

dict_qs = []
for day in [1, 2, 3]:
    data = load_json(f"content/day-{day:02d}/dictation.json")
    if data:
        for w in data.get("words", []):
            if isinstance(w, dict) and w.get("correct") and w.get("options"):
                dict_qs.append({"correct": w["correct"], "options": w["options"]})
            if len(dict_qs) >= 8:
                break
    if len(dict_qs) >= 8:
        break

passage_title = yellowstone["title"] if yellowstone else "Yellowstone National Park"
passage_text  = yellowstone["text"] if yellowstone else ""
reading_qs    = yellowstone.get("questions", [])[:5] if yellowstone else []

# --- تقسيم النص إلى أسطر منفصلة مع معرفات ---
lines = passage_text.split('\n')
line_ids = []
passage_lines_html = ""
for idx, line in enumerate(lines):
    line_id = f"line-{idx+1}"
    line_ids.append(line_id)
    passage_lines_html += f'<span id="{line_id}" class="passage-line">{line}</span>\n'

# --- إسناد رقم السطر لكل سؤال (محدد يدوياً) ---
# سأقوم بتحديد الأسطر بناءً على محتوى النص المتوقع
answer_lines = {
    1: "line-5",   # "Yellowstone National Park, established in 1872..."
    2: "line-9",   # "The park sits atop a volcanic hotspot..."
    3: "line-10",  # "Old Faithful... erupts approximately every 90 minutes..."
    4: "line-14",  # "The reintroduction of wolves in 1995..."
    5: "line-3"    # "...home to a vast array of wildlife, including grizzly bears, wolves, bison, and elk."
}

# --- دالة بناء بطاقة السؤال ---
def make_q_card(num, q_text, options, answer_idx, line_id=None):
    correct_text = options[answer_idx] if 0 <= answer_idx < len(options) else "—"
    opts_html = ""
    for j, opt in enumerate(options):
        letter = chr(65 + j)
        is_correct = "true" if j == answer_idx else "false"
        opts_html += f'<div class="opt" data-correct="{is_correct}"><span class="opt-letter">{letter}</span><span class="opt-text">{opt}</span></div>\n'
    
    line_attr = f' data-line="{line_id}"' if line_id else ""
    return f"""
<div class="q-card"{line_attr}>
  <div class="q-text en"><span class="q-num">{num}</span> {q_text}</div>
  <div class="options ltr-block">{opts_html}</div>
  <div class="ans-correct">✅ الإجابة الصحيحة: <strong class="ltr-inline">{correct_text}</strong></div>
  <div class="ans-wrong">❌ الخيارات الأخرى غير صحيحة.</div>
</div>"""

# --- بناء البطاقات ---
reading_cards = ""
for i, q in enumerate(reading_qs, 1):
    line = answer_lines.get(i, None)
    reading_cards += make_q_card(i, q["q"], q["options"], q.get("answer", -1), line_id=line)

grammar_cards = ""
for i, q in enumerate(grammar_qs, 1):
    grammar_cards += make_q_card(i, q["q"], q["options"], q.get("answer", -1))

vocab_cards = ""
for i, q in enumerate(vocab_qs, 1):
    vocab_cards += make_q_card(i, q["q"], q["options"], q.get("answer", -1))

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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--primary:#0b2b4f;--accent:#0071e3;--green:#16a34a;--green-light:#dcfce7;--green-dark:#14532d;--red:#dc2626;--red-light:#fee2e2;--red-dark:#7f1d1d;--gold:#d97706;--gold-light:#fef3c7;--gray:#64748b;--border:#e2e8f0;--bg:#f8fafc;--card-shadow:0 2px 12px rgba(0,0,0,0.06);--highlight-yellow:#fff176}
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
.passage-body{padding:1.5rem;font-family:'Inter',sans-serif;font-size:0.97rem;line-height:2;color:#334155;direction:ltr;text-align:left}
.passage-line{display:block;padding:2px 5px;border-radius:3px;transition:background 0.3s}
.passage-line.highlight{background:var(--highlight-yellow);padding:2px 8px;border-radius:4px;box-shadow:0 0 5px rgba(0,0,0,0.1)}
.q-card{background:#fff;border-radius:16px;border:1px solid var(--border);padding:1.4rem 1.5rem 1.2rem;margin:1.2rem 0;box-shadow:var(--card-shadow)}
.q-num{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;background:var(--accent);color:#fff;border-radius:50%;font-size:0.88rem;font-weight:700;flex-shrink:0;margin-inline-end:0.5rem;font-family:'Inter',sans-serif}
.q-text{font-size:1.02rem;font-weight:600;color:var(--primary);margin-bottom:1rem;display:flex;align-items:flex-start;gap:0.4rem}
.options{display:grid;grid-template-columns:1fr 1fr;gap:0.55rem;margin:0.6rem 0 1rem;direction:ltr;text-align:left}
@media(max-width:560px){.options{grid-template-columns:1fr}}
.opt{display:flex;align-items:center;gap:0.5rem;padding:0.6rem 0.9rem;background:#f1f5f9;border:1.5px solid #e2e8f0;border-radius:10px;cursor:pointer;transition:background 0.18s,border-color 0.18s;direction:ltr;text-align:left;user-select:none}
.opt:hover{background:#e0e7f0;border-color:var(--accent)}
.opt-letter{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;background:#cbd5e1;color:#334155;border-radius:6px;font-size:0.8rem;font-weight:700;font-family:'Inter',sans-serif;flex-shrink:0}
.opt-text{font-family:'Inter',sans-serif;font-size:0.94rem;color:#334155;direction:ltr}
.opt[data-correct="true"]{display:flex}
.opt[data-correct="true"].revealed-correct{background:var(--green-light);border-color:var(--green)}
.opt[data-correct="true"].revealed-correct .opt-letter{background:var(--green);color:#fff}
.opt[data-correct="true"].revealed-correct .opt-text{color:var(--green-dark);font-weight:600}
.ans-correct,.ans-wrong{display:none;border-radius:10px;padding:0.75rem 1rem;margin-top:0.6rem;font-size:0.94rem;direction:rtl;text-align:right}
.q-card.revealed .ans-correct{display:block;background:var(--green-light);border-right:4px solid var(--green);color:var(--green-dark)}
.q-card.revealed .ans-wrong{display:block;background:var(--red-light);border-right:4px solid var(--red);color:var(--red-dark)}
.tips-box{background:linear-gradient(135deg,#0b2b4f,#1a4a8a);color:#fff;border-radius:20px;padding:2rem 1.5rem;margin-top:3rem;direction:rtl;text-align:right}
.tips-box h3{font-size:1.25rem;font-weight:700;margin-bottom:1.2rem;text-align:center}
.tips-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:1rem}
.tip-item{background:rgba(255,255,255,0.1);border-radius:12px;padding:1rem;font-size:0.9rem;text-align:center}
.tip-icon{font-size:1.6rem;display:block;margin-bottom:0.4rem}
.print-btn{text-align:center;margin:2rem 0}
.print-btn button{background:var(--accent);color:#fff;border:none;padding:0.75rem 2.5rem;font-size:1rem;font-family:'Cairo',sans-serif;font-weight:700;border-radius:50px;cursor:pointer;box-shadow:0 4px 14px rgba(0,113,227,0.3);transition:opacity 0.2s}
.print-btn button:hover{opacity:0.88}
.golden-tip{background:var(--gold-light);border-right:4px solid var(--gold);border-radius:10px;padding:1.2rem;margin:1.5rem 0;direction:rtl;color:var(--gold-dark)}
.golden-tip h4{font-size:1.1rem;margin-bottom:0.5rem}
.golden-tip p{margin-bottom:0.5rem}
@media print{.print-btn,.hero .badges{display:none}body{background:#fff}.q-card.revealed .ans-correct,.q-card.revealed .ans-wrong{display:block!important}@page{margin:1.5cm}}
</style>
</head>
<body>
<header class="hero">
<img src="assets/images/reyadah-logo.png" alt="شعار معهد الريادة" onerror="this.style.display='none'">
<h1>APNE&#8209;ITC&nbsp;English&nbsp;Preparation</h1>
<p class="trainer">مع المدرب: أ. أنس عبدالرحمن | معهد الريادة للتدريب</p>
<p class="contact">للتسجيل: <span class="ltr-inline">0546088130</span> – <span class="ltr-inline">0548775199</span></p>
<div class="badges">
<span class="badge">📖 قراءة</span><span class="badge">📘 قواعد</span><span class="badge">🧠 مفردات</span><span class="badge">✍️ إملاء</span>
</div>
</header>
<div class="container">
<div class="sec-header ar"><div class="sec-icon">📖</div><div><div class="sec-title-ar">قسم القراءة</div><div class="sec-title-en">Reading Comprehension</div></div></div>
<div class="passage-box"><div class="passage-header en">""" + passage_title + """</div><div class="passage-body en">""" + passage_lines_html + """</div></div>

<div class="golden-tip">
<h4>💡 نصيحة ذهبية: Skimming vs Scanning</h4>
<p><strong>Skimming (التصفح السريع):</strong> استخدمه في البداية لتفهم الفكرة العامة للقطعة خلال 30-60 ثانية. اقرأ الجملة الأولى والأخيرة من كل فقرة فقط.</p>
<p><strong>Scanning (البحث السريع):</strong> استخدمه للبحث عن كلمة مفتاحية من السؤال (مثل تاريخ، اسم، رقم). يستغرق 10-20 ثانية للسؤال الواحد.</p>
<p>⏱️ <strong>الوقت النموذجي:</strong> خصص 60-90 ثانية لكل سؤال قراءة (يشمل العودة للنص والتحقق).</p>
</div>

""" + reading_cards + """

<div class="sec-header ar"><div class="sec-icon">📘</div><div><div class="sec-title-ar">قسم القواعد</div><div class="sec-title-en">Grammar</div></div></div>
""" + grammar_cards + """

<div class="sec-header ar"><div class="sec-icon">🧠</div><div><div class="sec-title-ar">قسم المفردات</div><div class="sec-title-en">Vocabulary</div></div></div>
""" + vocab_cards + """

<div class="sec-header ar"><div class="sec-icon">✍️</div><div><div class="sec-title-ar">قسم الإملاء</div><div class="sec-title-en">Spelling &amp; Dictation</div></div></div>
<p class="ar" style="color:var(--gray);margin-bottom:1rem">اختر التهجئة الصحيحة لكل كلمة:</p>
""" + dict_cards + """

<div class="print-btn"><button onclick="revealAll();window.print()">🖨️ كشف الإجابات وطباعة</button></div>
<div class="tips-box"><h3>💡 نصائح للاستفادة القصوى من الاختبار</h3><div class="tips-grid"><div class="tip-item"><span class="tip-icon">📖</span>اقرأ النص كاملاً قبل الإجابة</div><div class="tip-item"><span class="tip-icon">✏️</span>حدّد الكلمات المفتاحية في كل سؤال</div><div class="tip-item"><span class="tip-icon">⏱️</span>لا تقضِ وقتاً طويلاً على سؤال واحد</div><div class="tip-item"><span class="tip-icon">🔄</span>راجع إجاباتك قبل التسليم</div></div></div>
</div>
<script>
(function(){
"use strict";
function revealCard(card){
if(card.classList.contains("revealed"))return;
card.classList.add("revealed");
var correct=card.querySelector('.opt[data-correct="true"]');
if(correct)correct.classList.add("revealed-correct");

var lineId = card.getAttribute('data-line');
if (lineId) {
    // إزالة التمييز السابق
    document.querySelectorAll('.passage-line.highlight').forEach(function(el){ el.classList.remove('highlight'); });
    // تمييز السطر الجديد
    var line = document.getElementById(lineId);
    if (line) {
        line.classList.add('highlight');
        line.scrollIntoView({behavior:'smooth',block:'center'});
    }
}
}
document.querySelectorAll(".q-card").forEach(function(card){
card.querySelectorAll(".opt").forEach(function(opt){
opt.addEventListener("click",function(){revealCard(card);});
});
});
window.revealAll=function(){
document.querySelectorAll(".q-card").forEach(revealCard);
};
})();
</script>
</body>
</html>"""

with open(os.path.join(REPO, "live_session.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("✅ live_session.html created with line-level highlighting")
