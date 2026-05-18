import json, os, html as html_mod

def load_json(path):
    if not os.path.exists(path): return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def escape(txt):
    return html_mod.escape(str(txt)) if txt else ""

def wrap_en(txt):
    if not txt:
        return ""
    # نستخدم span بسيط بدون bdo وسيتولى CSS مهمة الاتجاه
    return f'<span class="ltr-text">{txt}</span>'

def build_reading(day_num):
    r = load_json(f"content/day-{day_num:02d}/reading.json")
    if not r: return ""
    passages = r.get("passages", [])
    if not passages and isinstance(r, list):
        passages = r
    sec = f'<section class="reading"><h2 class="section-title">قطع القراءة ({len(passages)} قطع)</h2>\n'
    for pi, p in enumerate(passages):
        title = escape(p.get("title", f"Passage {pi+1}"))
        text = escape(p.get("text", "")).replace("\n", "<br>")
        questions = p.get("questions", [])
        sec += f'<article class="passage"><h3>{title}</h3>\n'
        sec += f'<div class="passage-text">{text}</div>\n'
        if questions:
            sec += '<div class="questions"><h4>أسئلة الفهم</h4><ol>\n'
            for q in questions:
                q_text = escape(q.get("q", ""))
                opts = q.get("options", [])
                sec += f'<li>{wrap_en(q_text)}<ol type="a">\n'
                for opt in opts:
                    sec += f'<li>{wrap_en(escape(opt))}</li>\n'
                sec += '</ol></li>\n'
            sec += '</ol></div>\n'
        sec += '</article>\n'
    sec += '</section>\n'
    return sec

def build_vocab(day_num):
    v = load_json(f"content/day-{day_num:02d}/vocabulary.json")
    if not v: return ""
    words = v.get("words", [])
    sec = '<section class="vocabulary">\n<h2 class="section-title">المفردات</h2>\n'
    if words:
        table_rows = ""
        for i, w in enumerate(words):
            eng = escape(w.get("english",""))
            ara = escape(w.get("arabic",""))
            table_rows += f'<tr><td>{i+1}</td><td class="en">{eng}</td><td class="ar">{ara}</td></tr>\n'
        table = f'<div class="word-table-wrap"><table class="word-table"><thead><tr><th>#</th><th>English</th><th>العربية</th></tr></thead><tbody>{table_rows}</tbody></table></div>'
        
        all_questions = [w.get("question") for w in words if w.get("question")]
        all_questions = all_questions[:20]
        questions_html = ""
        if all_questions:
            questions_html = '<div class="vocab-questions"><h4>أسئلة المفردات</h4><ol>\n'
            for q in all_questions:
                q_text = escape(q.get("q", ""))
                opts = q.get("options", [])
                questions_html += f'<li>{wrap_en(q_text)}<ol type="a">\n'
                for opt in opts:
                    questions_html += f'<li>{wrap_en(escape(opt))}</li>\n'
                questions_html += '</ol></li>\n'
            questions_html += '</ol></div>\n'
        
        if questions_html:
            sec += '<div class="vocab-flex">\n'
            sec += f'<div class="vocab-col">{table}</div>\n'
            sec += f'<div class="vocab-col">{questions_html}</div>\n'
            sec += '</div>\n'
        else:
            sec += table
    sec += '</section>\n'
    return sec

def build_dictation(day_num):
    d = load_json(f"content/day-{day_num:02d}/dictation.json")
    if not d: return ""
    words = d.get("words", []) if isinstance(d, dict) else d
    if not words: return ""
    sec = '<section class="dictation">\n<h2 class="section-title">الإملاء</h2>\n<ul>\n'
    for w in words:
        if isinstance(w, dict):
            correct = escape(w.get("correct", ""))
            opts = w.get("options", [])
            sec += f'<li><strong>{wrap_en(correct)}</strong> — {wrap_en(", ".join(opts))}</li>\n'
        else:
            sec += f'<li>{wrap_en(escape(w))}</li>\n'
    sec += '</ul>\n</section>\n'
    return sec

def build_grammar_lesson(day_num):
    path = f"content/day-{day_num:02d}/grammar.html"
    if not os.path.exists(path): return ""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return f'<section class="grammar-lesson">\n<h2 class="section-title">درس القواعد</h2>\n{content}\n</section>\n'

def build_grammar_test(day_num):
    g = load_json(f"content/day-{day_num:02d}/grammar-test.json")
    if not g: return ""
    questions = g.get("questions", []) if isinstance(g, dict) else g
    if not questions: return ""
    questions = questions[:20]
    sec = '<section class="grammar-test">\n<h2 class="section-title">اختبار القواعد</h2>\n<ol>\n'
    for q in questions:
        q_text = escape(q.get("q", ""))
        opts = q.get("options", [])
        sec += f'<li>{wrap_en(q_text)}<ol type="a">\n'
        for opt in opts:
            sec += f'<li>{wrap_en(escape(opt))}</li>\n'
        sec += '</ol></li>\n'
    sec += '</ol>\n</section>\n'
    return sec

def build_compilation(i):
    c = load_json(f"content/exams/compilation-{i}.json")
    if not c: return ""
    questions = c if isinstance(c, list) else c.get("questions", [])
    if not questions: return ""
    sec = f'<section class="compilation"><h2 class="section-title">تجميع {i}</h2>\n<ol>\n'
    for q in questions:
        q_text = escape(q.get("q", ""))
        opts = q.get("options", [])
        sec += f'<li>{wrap_en(q_text)}<ol type="a">\n'
        for opt in opts:
            sec += f'<li>{wrap_en(escape(opt))}</li>\n'
        sec += '</ol></li>\n'
    sec += '</ol>\n</section>\n'
    return sec

def build_glossary():
    all_words = []
    for d in range(1, 8):
        v = load_json(f"content/day-{d:02d}/vocabulary.json")
        if v:
            all_words.extend(v.get("words", []))
    seen = set()
    rows = ""
    idx = 0
    for w in all_words:
        eng = w.get("english","")
        if eng not in seen:
            seen.add(eng)
            idx += 1
            rows += f'<tr><td>{idx}</td><td class="en">{escape(eng)}</td><td class="ar">{escape(w.get("arabic",""))}</td></tr>\n'
    return f'<section class="glossary"><h2 class="section-title">مسرد الكلمات</h2><table class="word-table"><thead><tr><th>#</th><th>English</th><th>العربية</th></tr></thead><tbody>{rows}</tbody></table></section>'

def get_reading_title(day_num):
    r = load_json(f"content/day-{day_num:02d}/reading.json")
    if not r: return f"Day {day_num} Reading"
    passages = r.get("passages", [])
    if not passages and isinstance(r, list):
        passages = r
    if passages:
        first = passages[0] if isinstance(passages[0], dict) else None
        if first:
            return first.get("title", f"Passage {day_num}")
    return f"Day {day_num} Reading"

def get_vocab_topic(day_num):
    v = load_json(f"content/day-{day_num:02d}/vocabulary.json")
    if v:
        return v.get("topic", f"Vocabulary Day {day_num}")
    return f"Vocabulary Day {day_num}"

syllabus_rows = ""
for d in range(1, 8):
    reading_title = get_reading_title(d)
    vocab_topic = get_vocab_topic(d)
    grammar = ["Present/Past Simple", "Continuous Tenses", "Perfect Tenses",
               "Passive Voice", "Comparative/Superlative", "Gerund/Infinitive", "قواعد جديدة ومراجعة شاملة"][d-1]
    syllabus_rows += f'<tr><td>اليوم {d}</td><td>{escape(reading_title)}</td><td>{escape(vocab_topic)}</td><td>{grammar}</td></tr>\n'

day_titles = [get_reading_title(d) for d in range(1, 8)]

# ---------- المقدمة بالإنجليزية مع الإهداء ----------
intro_text = """
<h2>Welcome to the APNE-ITC Comprehensive Guide</h2>
<p>This book is the fruit of extensive effort and dedication, designed to provide you with the most effective preparation for the <strong>APNE-ITC</strong> exam. Every section has been carefully crafted to ensure you master the required skills in reading, vocabulary, grammar, and dictation.</p>
<p>Over seven intensive days, with two hours of study per day, you will progress step by step through real exam materials, practical exercises, and full mock tests. The content is drawn from authentic sources and organized in a clear, logical sequence.</p>
<p>My goal is to make your learning journey as smooth and successful as possible. May this book be a key to your success, and may your hard work bring you the results you deserve.</p>
<p><em>To the light of my life, my first teacher, my father.</em></p>

<div style="text-align:left; margin-top:3rem;">
    <strong>Author & Instructor</strong><br>
    <span style="font-size:1.2rem;">Anas Abdulrahman</span>
</div>
"""

# ---------- CSS المتكامل من Claude ----------
style = '''
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=Inter:wght@400;500;600;700&family=Amiri:ital,wght@0,400;0,700;1,400&display=swap');

:root {
  --primary: #0b2b4f;
  --accent: #c4450c;
  --paper: #fffef9;
  --col-gap: 2.5rem;
  --border-subtle: #dde5f0;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Cairo', 'Amiri', serif;
  background: #f5f2eb;
  color: #1e1e1e;
  line-height: 2.1;
  font-size: 1.12rem;
  padding: 2rem 1rem;
}

.print-btn {
  position: fixed; top: 20px; right: 20px; z-index: 999;
  background: var(--primary); color: white; border: none;
  padding: 12px 28px; font-size: 1.1rem;
  font-family: 'Inter', sans-serif; font-weight: 600;
  border-radius: 50px; cursor: pointer;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: all .3s;
}
.print-btn:hover { background: #00264d; transform: translateY(-2px); }

.book {
  max-width: 1100px; margin: 0 auto;
  background: var(--paper);
  box-shadow: 0 20px 60px rgba(0,0,0,0.12);
  border-radius: 4px; padding: 3rem 3.5rem; position: relative;
}

.cover {
  text-align: center; margin-bottom: 3rem; page-break-after: always;
  background: linear-gradient(135deg,#f9f9f9,#fff);
  padding: 4rem 2rem; border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}
.cover h1 {
  font-size: 4rem; color: var(--primary); font-weight: 700;
  margin-bottom: 1rem; font-family: 'Inter', sans-serif; direction: ltr;
}
.cover .subtitle {
  font-size: 1.8rem; color: #555; margin-bottom: 2rem;
  direction: ltr; font-family: 'Inter', sans-serif;
}
.cover .logo { margin: 3rem 0; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1)); }
.cover .author { font-size: 1.3rem; margin-top: 3rem; color: #444; direction: ltr; }
.cover .contact { font-size: 1rem; color: #777; margin-top: .5rem; }

.section-title {
  font-size: 2rem; color: var(--primary);
  border-bottom: 3px solid var(--primary);
  padding-bottom: .3rem; margin: 3rem 0 1.5rem;
  direction: rtl; text-align: right;
  font-family: 'Cairo', sans-serif;
}

article.passage { margin-bottom: 2.5rem; }
article.passage h3 {
  direction: ltr; text-align: left;
  font-family: 'Inter', sans-serif;
  font-size: 1.4rem; font-weight: 700; color: var(--primary);
  margin: .5rem 0 1rem;
}
.passage-text {
  background: #f9f9f6; padding: 1.4rem 1.5rem;
  border-left: 5px solid var(--accent);
  border-right: none;
  margin: 1rem 0; white-space: pre-line;
  direction: ltr; text-align: left;
  font-family: 'Inter', sans-serif;
  font-size: .97rem; line-height: 1.9;
}

.questions { margin-top: 1.5rem; }
.questions h4 {
  direction: rtl; text-align: right;
  font-family: 'Cairo', sans-serif;
  color: var(--primary); margin-bottom: 1rem; font-size: 1.1rem;
}
.questions ol {
  list-style: none; counter-reset: q-counter;
  direction: ltr; text-align: left;
  font-family: 'Inter', sans-serif; font-size: .93rem;
}
.questions > ol > li {
  position: relative; padding-left: 2rem; margin-bottom: 1.2rem;
}
.questions > ol > li::before {
  counter-increment: q-counter;
  content: counter(q-counter) ". ";
  font-weight: bold; color: var(--primary);
  position: absolute; left: 0;
}
.questions ol[type="a"] {
  list-style: lower-alpha; padding-left: 1.5rem; margin-top: .4rem;
}
.questions ol[type="a"] li { padding-left: 0; margin-bottom: .3rem; }

.vocab-flex {
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
  gap: var(--col-gap);
  align-items: start;
  margin-top: 1.5rem;
}
.vocab-col { min-width: 0; }

.word-table-wrap {
  max-height: 640px; overflow-y: auto;
  border: 1px solid #ccc; border-radius: 4px;
}
.word-table-wrap::-webkit-scrollbar { width: 6px; }
.word-table-wrap::-webkit-scrollbar-thumb {
  background: var(--primary); border-radius: 3px;
}

table.word-table {
  width: 100%; border-collapse: collapse;
  margin: 0; font-size: .88rem;
}
table.word-table thead th {
  background: var(--primary); color: white;
  padding: 8px 10px;
  font-family: 'Cairo', sans-serif;
  position: sticky; top: 0; z-index: 2;
}
table.word-table td, table.word-table th {
  border: 1px solid #ccc; padding: 6px 10px;
}
table.word-table td.en {
  direction: ltr; text-align: left;
  font-family: 'Inter', sans-serif;
}
table.word-table td.ar {
  direction: rtl; text-align: right;
  font-family: 'Cairo', sans-serif;
}

.vocab-questions h4 {
  direction: rtl; text-align: right;
  font-family: 'Cairo', sans-serif;
  color: var(--primary); margin-bottom: 1rem;
}
.vocab-questions ol {
  direction: ltr; text-align: left;
  list-style: decimal; padding-left: 1.5rem;
  font-family: 'Inter', sans-serif; font-size: .90rem;
}
.vocab-questions ol li { margin-bottom: .9rem; }
.vocab-questions ol[type="a"] {
  list-style: lower-alpha; padding-left: 1.2rem; margin-top: .25rem;
}

.grammar-flex {
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
  gap: var(--col-gap);
  align-items: start;
  margin-top: 1.5rem;
}
.grammar-col { min-width: 0; }

.lesson-col {
  border-right: 2px solid var(--border-subtle);
  border-left: none !important;
  padding-right: 1.2rem; padding-left: 0 !important;
}
.test-col { padding-right: 0 !important; padding-left: .5rem; }

.grammar-lesson {
  font-family: 'Inter', sans-serif; font-size: .88rem;
  border: none !important; background: transparent !important;
  padding: 0 !important;
}
.grammar-lesson h2, .grammar-lesson h3, .grammar-lesson h4 {
  direction: rtl; text-align: right;
  font-family: 'Cairo', sans-serif;
  color: var(--primary);
  margin: 1rem 0 .5rem;
}
.grammar-lesson h2 { font-size: 1.3rem; border-bottom: 2px solid var(--primary); padding-bottom: .3rem; }
.grammar-lesson h3 { font-size: 1.1rem; }

.grammar-lesson p,
.grammar-lesson ul,
.grammar-lesson li {
  direction: ltr; text-align: left;
  font-family: 'Inter', sans-serif;
}
.grammar-lesson table { font-size: .85rem; margin: .8rem 0; width: 100%; border-collapse: collapse; }
.grammar-lesson th {
  background: #0059b3 !important; color: white !important;
  padding: 8px; text-align: center;
}
.grammar-lesson td {
  padding: 7px 8px; text-align: left;
  border-bottom: 1px solid #e0e8f5;
  background: #fafcff;
}
.grammar-lesson .container,
.grammar-lesson .page {
  padding: 0 !important; box-shadow: none !important;
  border: none !important; border-radius: 0 !important;
  background: transparent !important; max-width: 100% !important;
}
.grammar-lesson .footer-note,
.grammar-lesson .print-footer {
  display: none;
}

.grammar-test h2.section-title {
  direction: rtl; text-align: right; font-family: 'Cairo', sans-serif;
}
.grammar-test ol {
  direction: ltr; text-align: left;
  list-style: decimal; padding-left: 1.5rem;
  font-family: 'Inter', sans-serif; font-size: .90rem;
}
.grammar-test ol li { margin-bottom: .9rem; }
.grammar-test ol[type="a"] {
  list-style: lower-alpha; padding-left: 1.2rem; margin-top: .25rem;
}

.dictation ul {
  list-style: none; padding: 0;
  direction: ltr; text-align: left;
  font-family: 'Inter', sans-serif; font-size: .93rem;
}
.dictation ul li {
  padding: .5rem 0; border-bottom: 1px dashed #e0e0e0;
}
.dictation ul li strong { color: var(--primary); font-weight: 700; }

.syllabus table.word-table th,
.syllabus table.word-table td {
  text-align: center; font-family: 'Cairo', sans-serif;
}

.glossary table.word-table td:nth-child(2) {
  direction: ltr; text-align: left; font-family: 'Inter', sans-serif;
}
.glossary table.word-table td:nth-child(3) {
  direction: rtl; text-align: right; font-family: 'Cairo', sans-serif;
}

.references p, .footer-note p {
  direction: rtl; text-align: right; font-family: 'Cairo', sans-serif;
}
.intro p {
  direction: rtl; text-align: right; font-family: 'Cairo', sans-serif;
}
.intro h2 {
  direction: ltr; text-align: left; font-family: 'Inter', sans-serif;
}

.ltr-text {
  direction: ltr;
  unicode-bidi: isolate;
}

@media (max-width: 900px) {
  .vocab-flex, .grammar-flex {
    grid-template-columns: 1fr !important;
  }
  .lesson-col {
    border-right: none;
    border-bottom: 2px solid var(--border-subtle);
    padding-right: 0; padding-bottom: 1.5rem; margin-bottom: 1.5rem;
  }
  body { font-size: 1rem; padding: .5rem; }
  .book { padding: 1.5rem 1rem; }
  .cover h1 { font-size: 2.2rem; }
  .cover .subtitle { font-size: 1.1rem; }
  .section-title { font-size: 1.5rem; }
  .print-btn { padding: 8px 20px; font-size: .9rem; top: 10px; right: 10px; }
}

@media (max-width: 480px) {
  .book { padding: 1rem; }
  .cover h1 { font-size: 1.8rem; }
}

@media print {
  body { background: white; padding: 0; }
  .book { box-shadow: none; border-radius: 0; padding: 2cm; max-width: 100%; }
  .print-btn { display: none; }
  .word-table-wrap { max-height: none; overflow: visible; }
  @page { margin: 1.5cm; @bottom-center { content: counter(page); font-family: 'Cairo'; font-size: 11px; } }
  .section-title { page-break-before: always; }
  .cover { page-break-after: always; }
  .vocab-flex, .grammar-flex { grid-template-columns: 1fr 1fr !important; }
  .lesson-col { border-right: 1px solid #ccc; }
}
'''

html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>APNE-ITC Master Guide – Al-Reyadah Training Institute</title>
<style>{style}</style>
</head>
<body>
<button class="print-btn" onclick="window.print()">🖨️ طباعة / PDF</button>
<div class="book">
'''

# غلاف باسم English Zone Team فقط
html += '<div class="cover">'
html += '<img src="assets/images/reyadah-logo.png" alt="Reyadah Logo" class="logo" width="180">'
html += '<h1>APNE-ITC Master Guide</h1>'
html += '<p class="subtitle">The Ultimate Preparation Course<br>by Al-Reyadah Training Institute</p>'
html += '<p class="author"><strong>English Zone Team</strong></p>'
html += '<p class="contact">📞 0546088130 | 0548775199</p>'
html += '</div>'

html += '<section class="intro">'
html += '<h2 class="section-title">مقدمة الكتاب</h2>'
html += intro_text
html += '</section>'

html += '<section class="syllabus">'
html += '<h2 class="section-title">المنهج الدراسي</h2>'
html += '<table class="word-table"><thead><tr><th>اليوم</th><th>القراءة</th><th>المفردات</th><th>القواعد</th></tr></thead><tbody>'
html += syllabus_rows
html += '</tbody></table></section>'

for d in range(1, 8):
    html += f'<div class="day" id="day-{d}"><h1 class="section-title">اليوم {d} – {day_titles[d-1]}</h1>'
    html += build_reading(d)
    html += build_vocab(d)
    html += build_dictation(d)
    html += '<div class="grammar-flex">'
    html += '<div class="grammar-col lesson-col">'
    html += build_grammar_lesson(d)
    html += '</div>'
    html += '<div class="grammar-col test-col">'
    html += build_grammar_test(d)
    html += '</div>'
    html += '</div>'
    html += '</div>'

html += '<section class="compilations">'
for i in range(1, 7):
    html += build_compilation(i)
html += '</section>'

html += build_glossary()

html += '<section class="references"><h2 class="section-title">المصادر والمراجع</h2>'
refs = [
    "English Grammar in Use – Raymond Murphy (Cambridge)",
    "Practical English Usage – Michael Swan (Oxford)",
    "Oxford English Grammar Course – Swan & Walter (Oxford)",
    "Longman English Grammar – L.G. Alexander (Pearson)",
    "Understanding and Using English Grammar – Betty S. Azar (Pearson)",
    "Advanced Grammar in Use – Martin Hewings (Cambridge)",
    "The Official Cambridge Guide to IELTS – Cullen et al. (Cambridge)",
    "Vocabulary in Use – Stuart Redman (Cambridge)",
]
for r in refs:
    html += f'<p>• {r}</p>'
html += '</section>'

html += '<div class="footer-note">'
html += '<p><strong>Al-Reyadah Training Institute</strong><br>Instructor: Anas Abdulrahman<br>0546088130 | 0548775199</p>'
html += '</div>'

html += '</div></body></html>'

with open('textbook.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ textbook.html جاهز بحجم:", round(os.path.getsize('textbook.html')/1024), "KB")
