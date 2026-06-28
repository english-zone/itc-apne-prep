import json, os, html as html_mod

def load_json(path):
    if not os.path.exists(path): return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def escape(txt):
    return html_mod.escape(str(txt)) if txt else ""

def q_li(q_text, opts):
    h = f'<li class="q-en"><span class="q-text">{escape(q_text)}</span>\n<ol type="a" class="opts-en">\n'
    for opt in opts:
        h += f'<li class="opt-en">{escape(opt)}</li>\n'
    h += '</ol></li>\n'
    return h

def build_reading(day_num):
    r = load_json(f"content/day-{day_num:02d}/reading.json")
    if not r: return ""
    passages = r.get("passages", [])
    if not passages and isinstance(r, list): passages = r
    sec = f'<section class="reading"><h2 class="section-title">📖 قطع القراءة ({len(passages)} قطع)</h2>\n'
    for pi, p in enumerate(passages):
        title     = escape(p.get("title", f"Passage {pi+1}"))
        text      = escape(p.get("text", "")).replace("\n", "<br>")
        questions = p.get("questions", [])
        sec += f'<article class="passage"><h3 class="en-title">{title}</h3>\n'
        sec += f'<div class="passage-text">{text}</div>\n'
        if questions:
            sec += '<div class="questions"><h4>أسئلة الفهم</h4><ol class="q-list">\n'
            for q in questions:
                sec += q_li(q.get("q", ""), q.get("options", []))
            sec += '</ol></div>\n'
        sec += '</article>\n'
    sec += '</section>\n'
    return sec

def build_vocab(day_num):
    v = load_json(f"content/day-{day_num:02d}/vocabulary.json")
    if not v: return ""
    words = v.get("words", [])
    sec = '<section class="vocabulary"><h2 class="section-title">🧠 المفردات</h2>\n'
    if words:
        all_qs = [w.get("question") for w in words if w.get("question")][:20]
        if all_qs:
            sec += '<ol class="q-list">\n'
            for q in all_qs:
                sec += q_li(q.get("q", ""), q.get("options", []))
            sec += '</ol>\n'
    sec += '</section>\n'
    return sec

def build_dictation(day_num):
    d = load_json(f"content/day-{day_num:02d}/dictation.json")
    if not d: return ""
    words = d.get("words", []) if isinstance(d, dict) else d
    if not words: return ""
    sec = '<section class="dictation"><h2 class="section-title">✍️ الإملاء</h2>\n<ul class="dict-list">\n'
    for w in words:
        if isinstance(w, dict):
            correct = escape(w.get("correct", ""))
            opts    = escape(", ".join(w.get("options", [])))
            sec += f'<li class="dict-item"><strong>{correct}</strong> — {opts}</li>\n'
        else:
            sec += f'<li class="dict-item">{escape(w)}</li>\n'
    sec += '</ul>\n</section>\n'
    return sec

def build_grammar_test(day_num):
    g = load_json(f"content/day-{day_num:02d}/grammar-test.json")
    if not g: return ""
    qs = g.get("questions", []) if isinstance(g, dict) else g
    if not qs: return ""
    sec = '<section class="grammar-test"><h2 class="section-title">📘 اختبار القواعد</h2>\n<ol class="q-list">\n'
    for q in qs:
        sec += q_li(q.get("q", ""), q.get("options", []))
    sec += '</ol>\n</section>\n'
    return sec

def build_compilation(i):
    c = load_json(f"content/exams/compilation-{i}.json")
    if not c: return ""
    qs = c if isinstance(c, list) else c.get("questions", [])
    if not qs: return ""
    sec = f'<section class="compilation"><h2 class="section-title">📋 تجميع {i}</h2>\n<ol class="q-list">\n'
    for q in qs:
        sec += q_li(q.get("q", ""), q.get("options", []))
    sec += '</ol>\n</section>\n'
    return sec

def get_daily_tips(day):
    tips = {
        1: ["1️⃣ لا تحفظ الكلمة وحدها، بل احفظها في جملة.","2️⃣ ألقِ نظرة سريعة على الأسئلة قبل القراءة.","3️⃣ ركّز على Present Simple vs Past Simple.","4️⃣ الكلمات المنتهية بـ -tion/-sion غالباً أسماء.","5️⃣ أضف 10 كلمات جديدة لرصيدك اليوم."],
        2: ["1️⃣ كرر كلمات الأمس قبل بدء درس اليوم.","2️⃣ لا تتوقف عند كل كلمة صعبة، خمّن المعنى.","3️⃣ الأزمنة المستمرة = am/is/are + V-ing.","4️⃣ انتبه للحروف الصامتة مثل k في knife.","5️⃣ خذ نفساً عميقاً بين كل قسم وآخر."],
        3: ["1️⃣ اربط الكلمة بصورة ذهنية غريبة لتتذكرها.","2️⃣ لخّص الفقرة في جملة بعد قراءتها.","3️⃣ Present Perfect = have/has + V3.","4️⃣ i قبل e إلا بعد c (مثل believe, receive).","5️⃣ اشرب ماءً كثيراً أثناء المذاكرة."],
        4: ["1️⃣ اكتب الكلمات الصعبة على بطاقات صغيرة.","2️⃣ لاحظ أدوات الربط: however, therefore, although.","3️⃣ المبني للمجهول = be + V3.","4️⃣ فرّق بين their, there, they're.","5️⃣ أنت في منتصف الطريق، استمر."],
        5: ["1️⃣ راجع قبل النوم لتثبيت المعلومات.","2️⃣ تدرب على Scanning: ابحث عن الكلمات المفتاحية.","3️⃣ المقارنة: -er than / more... than.","4️⃣ الكلمات المنتهية بـ -ful بحرف L واحد.","5️⃣ استخدم تقنية 25 دقيقة تركيز + 5 دقائق راحة."],
        6: ["1️⃣ اربط ما تتعلمه اليوم بالأيام السابقة.","2️⃣ انظر إلى جذر الكلمة (Root) لتخمين معناها.","3️⃣ بعض الأفعال تأخذ V-ing وبعضها to+V.","4️⃣ انتبه للاختلاف الإملائي بين الاسم والفعل.","5️⃣ كل خطأ تتعلم منه هو درجة نحو النجاح."],
        7: ["1️⃣ لا تذاكر شيئاً جديداً اليوم، ركّز على المراجعة.","2️⃣ اقرأ القطعة بصوت عالٍ وكأنك تشرحها.","3️⃣ أعد قراءة ملاحظاتك على أخطاء القواعد.","4️⃣ اكتب الكلمات الصعبة خمس مرات متتالية.","5️⃣ ثق بالله ثم بنفسك، وامضِ مطمئناً."]
    }
    h = '<div class="daily-tips">'
    for t in tips.get(day, []):
        h += f'<div class="tip-item">{t}</div>'
    h += '</div>'
    return h

def get_reading_title(day_num):
    r = load_json(f"content/day-{day_num:02d}/reading.json")
    if not r: return f"Day {day_num} Reading"
    ps = r.get("passages", [])
    if not ps and isinstance(r, list): ps = r
    if ps:
        fst = ps[0] if isinstance(ps[0], dict) else None
        if fst: return fst.get("title", f"Passage {day_num}")
    return f"Day {day_num} Reading"

def get_vocab_topic(day_num):
    v = load_json(f"content/day-{day_num:02d}/vocabulary.json")
    return v.get("topic", f"Vocabulary Day {day_num}") if v else f"Vocabulary Day {day_num}"

syllabus_rows = ""
for d in range(1, 8):
    rt = get_reading_title(d)
    vt = get_vocab_topic(d)
    gr = ["Present/Past Simple","Continuous Tenses","Perfect Tenses","Passive Voice",
          "Comparative/Superlative","Gerund/Infinitive","قواعد جديدة ومراجعة شاملة"][d-1]
    syllabus_rows += (
        f'<tr>'
        f'<td style="text-align:center;font-weight:600;">اليوم {d}</td>'
        f'<td class="en-cell">{escape(rt)}</td>'
        f'<td class="en-cell">{escape(vt)}</td>'
        f'<td>{gr}</td>'
        f'</tr>\n'
    )

day_titles = [get_reading_title(d) for d in range(1, 8)]

intro_text = """<p style="direction:ltr;unicode-bidi:isolate;text-align:left;font-family:'Source Serif 4',serif;">
This book is the fruit of extensive effort and dedication, designed to provide you with the most
effective preparation for the <strong>APNE-ITC</strong> exam. Every section has been carefully
crafted to ensure you master the required skills in reading, vocabulary, grammar, and dictation.</p>
<p style="direction:ltr;unicode-bidi:isolate;text-align:left;font-family:'Source Serif 4',serif;margin-top:0.8rem;">
Over seven intensive days, with two hours of study per day, you will progress step by step through
real exam materials, practical exercises, and full mock tests.</p>
<p style="direction:ltr;unicode-bidi:isolate;text-align:left;font-style:italic;margin-top:0.8rem;font-family:'Source Serif 4',serif;">
To the light of my life, my first teacher, my father.</p>
<div style="direction:ltr;unicode-bidi:isolate;text-align:left;margin-top:2rem;font-family:'Inter',sans-serif;">
  <strong>English Zone Team</strong><br>Al-Reyadah Training Institute
</div>"""

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400;1,700&family=Tajawal:wght@400;500;700&family=Inter:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap');

:root {
  --primary: #0b2b4f;
  --accent:  #c4450c;
  --paper:   #fffef9;
  --text:    #1e1e1e;
  --border:  #d8d4cc;
  --gold:    #f39c12;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Amiri', 'Tajawal', serif;
  background: #ede9e0;
  color: var(--text);
  line-height: 1.95;
  font-size: 1.1rem;
  padding: 2rem 1rem;
  direction: rtl;
}

.en-title {
  direction: ltr !important;
  unicode-bidi: isolate !important;
  text-align: left !important;
  display: block;
}

.en-cell {
  direction: ltr !important;
  unicode-bidi: isolate !important;
  text-align: left !important;
}

.passage-text {
  direction: ltr !important;
  unicode-bidi: isolate !important;
  text-align: left !important;
  background: #f8f7f3;
  padding: 0.85rem 1.1rem;
  border-left: 4px solid var(--accent);
  border-radius: 0 6px 6px 0;
  margin: 0.7rem 0 1rem;
  white-space: pre-line;
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 0.98rem;
  line-height: 1.75;
  color: #2a2a2a;
}

li.q-en {
  direction: ltr !important;
  unicode-bidi: isolate !important;
  text-align: left !important;
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 0.98rem;
  line-height: 1.6;
  margin-bottom: 0.75rem;
  list-style: none;
  padding-left: 0;
}

ol.q-list {
  counter-reset: q-counter;
  padding: 0;
  margin: 0.4rem 0;
  list-style: none;
}
ol.q-list > li.q-en::before {
  counter-increment: q-counter;
  content: counter(q-counter) ". ";
  font-weight: 700;
  color: var(--primary);
  font-family: 'Inter', sans-serif;
  font-size: 0.9rem;
}

ol.opts-en {
  list-style: lower-alpha !important;
  direction: ltr !important;
  unicode-bidi: isolate !important;
  text-align: left !important;
  padding-left: 1.6rem;
  margin-top: 0.25rem;
}
li.opt-en {
  direction: ltr !important;
  unicode-bidi: isolate !important;
  text-align: left !important;
  font-family: 'Inter', sans-serif;
  font-size: 0.93rem;
  line-height: 1.55;
  margin-bottom: 0.18rem;
  color: #333;
}

ul.dict-list {
  list-style: none;
  padding: 0;
  direction: ltr;
  unicode-bidi: isolate;
  columns: 2;
  column-gap: 2rem;
  margin-top: 0.5rem;
}
li.dict-item {
  direction: ltr !important;
  unicode-bidi: isolate !important;
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  margin-bottom: 0.4rem;
  padding-right: 0.4rem;
  border-right: 2px solid var(--border);
  break-inside: avoid;
}

.book {
  max-width: 210mm;
  margin: 0 auto;
  background: var(--paper);
  box-shadow: 0 24px 70px rgba(0,0,0,0.18);
  border-radius: 3px;
  padding: 2.4cm 1.8cm;
}

.print-btn {
  position: fixed; top: 18px; right: 18px; z-index: 999;
  background: var(--primary); color: #fff; border: none;
  padding: 9px 22px; font-size: 0.95rem;
  font-family: 'Inter', sans-serif; font-weight: 600;
  border-radius: 50px; cursor: pointer;
  box-shadow: 0 4px 14px rgba(0,0,0,0.22);
  transition: all .25s;
}
.print-btn:hover { background: #1a4070; transform: translateY(-2px); }

.cover {
  text-align: center;
  margin-bottom: 3rem;
  background: linear-gradient(160deg, #f0eee8 0%, #ffffff 60%, #e8f0f8 100%);
  padding: 4rem 2rem 3.5rem;
  border-radius: 16px;
  box-shadow: 0 16px 40px rgba(0,0,0,0.08);
  border: 1px solid #e0ddd6;
}
.cover h1 {
  font-size: 3.2rem; color: var(--primary); font-weight: 700;
  direction: ltr; letter-spacing: -0.5px; margin-bottom: 0.6rem;
}
.cover .subtitle {
  font-size: 1.35rem; color: #4a5568; direction: ltr;
  margin-bottom: 2rem; font-family: 'Inter', sans-serif;
}
.cover .logo   { margin: 1.5rem 0; }
.cover .author { font-size: 1.1rem; color: #374151; direction: ltr; font-family: 'Inter', sans-serif; margin-top: 1.5rem; }
.cover .contact{ font-size: 0.9rem; color: #6b7280; direction: ltr; margin-top: 0.4rem; font-family: 'Inter', sans-serif; }

.section-title {
  font-size: 1.5rem;
  color: var(--primary);
  border-bottom: 2.5px solid var(--primary);
  padding-bottom: 0.35rem;
  margin: 1.8rem 0 0.9rem;
  font-family: 'Tajawal', 'Amiri', sans-serif;
  font-weight: 700;
}

.day-title {
  font-size: 1.55rem;
  color: white;
  background: var(--primary);
  padding: 0.6rem 1rem;
  border-radius: 8px;
  margin: 0 0 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

article.passage { margin-bottom: 1.5rem; }
h3.en-title {
  font-size: 1.1rem;
  color: var(--primary);
  margin-bottom: 0.4rem;
  font-family: 'Source Serif 4', Georgia, serif;
  font-weight: 600;
}
.questions h4 {
  font-size: 1rem;
  margin: 0.7rem 0 0.3rem;
  color: #555;
  font-family: 'Tajawal', sans-serif;
}

table.word-table {
  width: 100%; border-collapse: collapse; margin: 0.8rem 0;
  font-size: 0.97rem;
}
table.word-table thead tr { background: var(--primary); }
table.word-table th {
  color: white; padding: 7px 10px;
  font-family: 'Tajawal', sans-serif; font-weight: 600;
  font-size: 0.95rem;
}
table.word-table td { border: 1px solid var(--border); padding: 5px 9px; }
table.word-table tbody tr:nth-child(even) { background: #f5f3ee; }

.daily-tips {
  background: #fef9e7;
  border-right: 4px solid var(--gold);
  padding: 0.7rem 0.9rem;
  margin: 0.8rem 0 1rem;
  border-radius: 0 8px 8px 0;
  font-size: 0.92rem;
  color: #6b4f00;
  line-height: 1.85;
}
.tip-item {
  padding: 0.22rem 0;
  border-bottom: 1px dashed #e8d48a;
}
.tip-item:last-child { border-bottom: none; }

.side-by-side {
  display: flex;
  gap: 1.2rem;
  margin: 1rem 0;
  align-items: flex-start;
}
.side-left  { flex: 0 0 53%; min-width: 0; }
.side-right { flex: 0 0 44%; min-width: 0; }

.side-right { border-right: 1.5px solid var(--border); padding-right: 1.1rem; }

.footer-note {
  text-align: center; margin-top: 3rem;
  padding: 1.2rem; background: #eeeae2;
  border-radius: 8px; font-size: 0.92rem;
  font-family: 'Inter', sans-serif; color: #4a4a4a;
  direction: ltr; unicode-bidi: isolate;
}

@media (max-width: 780px) {
  .side-by-side { flex-direction: column; }
  .side-right { border-right: none; padding-right: 0; border-top: 1.5px solid var(--border); padding-top: 0.8rem; }
  .book { padding: 1.2rem; }
  ul.dict-list { columns: 1; }
}

@media print {
  @page {
    size: A4 portrait;
    margin: 1.6cm 1.4cm 1.8cm 1.4cm;
  }

  @page :first {
    margin: 1cm;
  }

  body {
    background: white !important;
    padding: 0 !important;
    font-size: 9.8pt !important;
    line-height: 1.58 !important;
    color: #111 !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .book {
    box-shadow: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
    max-width: 100% !important;
    margin: 0 !important;
  }

  .print-btn { display: none !important; }

  body::after {
    content: "";
    display: block;
    position: running(footer);
  }

  .cover {
    page-break-after: always !important;
    break-after: page !important;
    height: 26cm;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    background: white !important;
    box-shadow: none !important;
    border: 1px solid #ccc !important;
    border-radius: 0 !important;
    padding: 2cm !important;
    margin: 0 !important;
  }
  .cover h1        { font-size: 26pt !important; margin-bottom: 0.5cm; }
  .cover .subtitle { font-size: 13pt !important; margin-bottom: 0.3cm; }
  .cover .author   { font-size: 11pt !important; }
  .cover .contact  { font-size: 9.5pt !important; }
  .cover .logo     { width: 110px !important; }

  .day {
    page-break-before: always !important;
    break-before: page !important;
  }

  .day-title {
    font-size: 13pt !important;
    padding: 4pt 8pt !important;
    margin: 0 0 6pt !important;
    background: var(--primary) !important;
    color: white !important;
    border-radius: 0 !important;
  }

  .section-title {
    font-size: 11.5pt !important;
    border-bottom: 1.5pt solid #0b2b4f !important;
    padding-bottom: 2pt !important;
    margin: 8pt 0 5pt !important;
    color: #0b2b4f !important;
  }
  h3.en-title {
    font-size: 10pt !important;
    margin-bottom: 3pt !important;
  }

  .passage-text {
    font-size: 9pt !important;
    line-height: 1.52 !important;
    padding: 5pt 8pt !important;
    border-left: 2.5pt solid #c4450c !important;
    background: #fafaf8 !important;
    margin: 4pt 0 6pt !important;
  }

  li.q-en {
    font-size: 9pt !important;
    line-height: 1.5 !important;
    margin-bottom: 4pt !important;
  }
  li.opt-en {
    font-size: 8.5pt !important;
    line-height: 1.45 !important;
    margin-bottom: 1.5pt !important;
  }
  ol.opts-en {
    padding-left: 12pt !important;
    margin-top: 1.5pt !important;
  }

  ul.dict-list {
    columns: 2 !important;
    column-gap: 1cm !important;
    padding: 0 !important;
  }
  li.dict-item {
    font-size: 9pt !important;
    margin-bottom: 2.5pt !important;
    padding-right: 0.3rem !important;
  }

  .side-by-side {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 0.6cm !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    align-items: flex-start !important;
    margin: 6pt 0 !important;
  }
  .side-left {
    flex: 0 0 52% !important;
    width: 52% !important;
    max-width: 52% !important;
  }
  .side-right {
    flex: 0 0 45% !important;
    width: 45% !important;
    max-width: 45% !important;
    border-right: 1pt solid #ccc !important;
    padding-right: 0.5cm !important;
  }

  table.word-table {
    font-size: 9pt !important;
    width: 100% !important;
  }
  table.word-table th { font-size: 8.5pt !important; padding: 3.5pt 6pt !important; }
  table.word-table td { padding: 2.5pt 6pt !important; }

  .daily-tips {
    font-size: 8.5pt !important;
    line-height: 1.48 !important;
    padding: 4pt 7pt !important;
    margin: 4pt 0 6pt !important;
    border-right: 2.5pt solid #f39c12 !important;
    background: #fffbe6 !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    color: #5a3c00 !important;
  }
  .tip-item { padding: 1.5pt 0 !important; }

  .compilation {
    page-break-before: always !important;
    break-before: page !important;
  }

  .footer-note {
    font-size: 8.5pt !important;
    padding: 6pt !important;
    margin-top: 0.8cm !important;
    page-break-inside: avoid !important;
  }

  article.passage  { page-break-inside: avoid !important; break-inside: avoid !important; }
  .questions       { page-break-inside: avoid !important; break-inside: avoid !important; }
  .dictation       { page-break-inside: avoid !important; break-inside: avoid !important; }

  .section-title, h3.en-title {
    page-break-after: avoid !important;
    break-after: avoid !important;
  }
  .day-title {
    page-break-after: avoid !important;
    break-after: avoid !important;
  }
}
"""

html = f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>APNE-ITC Master Guide – Al-Reyadah Training Institute</title><style>{CSS}</style></head><body><button class="print-btn" onclick="window.print()">🖨️ طباعة / PDF</button><div class="book">\n'

html += '<div class="cover"><img src="assets/images/reyadah-logo.png" alt="Reyadah Logo" class="logo" width="140"><h1>APNE-ITC Master Guide</h1><p class="subtitle">The Ultimate Preparation Course<br>by Al-Reyadah Training Institute</p><p class="author"><strong>English Zone Team</strong></p><p class="contact">📞 0546088130 | 0548775199</p></div>\n'

html += '<section class="intro"><h2 class="section-title">📝 مقدمة الكتاب</h2>' + intro_text + '</section>\n'

html += '<section class="syllabus"><h2 class="section-title">📅 المنهج الدراسي</h2>'
html += '<table class="word-table"><thead><tr><th>اليوم</th><th>القراءة</th><th>المفردات</th><th>القواعد</th></tr></thead><tbody>'
html += syllabus_rows
html += '</tbody></table></section>\n'

for d in range(1, 8):
    html += f'<div class="day" id="day-{d}">\n'
    html += f'<div class="day-title">🗓️ اليوم {d} &nbsp;–&nbsp; <span style="direction:ltr;unicode-bidi:isolate;font-family:\'Source Serif 4\',serif;font-weight:400;">{day_titles[d-1]}</span></div>\n'
    html += get_daily_tips(d)
    html += build_reading(d)
    html += '<div class="side-by-side">'
    html += '<div class="side-left">'  + build_vocab(d)        + '</div>'
    html += '<div class="side-right">' + build_grammar_test(d) + '</div>'
    html += '</div>\n'
    html += build_dictation(d)
    html += '</div>\n'

html += '<section class="compilations">\n'
for i in range(1, 7):
    html += build_compilation(i)
html += '</section>\n'

html += '<div class="footer-note"><p><strong>Al-Reyadah Training Institute</strong> &nbsp;|&nbsp; English Zone Team &nbsp;|&nbsp; 📞 0546088130 &nbsp;|&nbsp; 0548775199</p></div>\n'
html += '</div></body></html>'

with open('textbook.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ textbook.html — BiDi صحيح + استغلال كامل لـ A4 + طباعة احترافية")
