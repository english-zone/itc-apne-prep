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
    # bdo dir=ltr يفرض الاتجاه حتى مع وجود dir=rtl في الصفحة
    return f'<bdo dir="ltr">{txt}</bdo>'

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
        sec += f'<div class="passage-text"><bdo dir="ltr">{text}</bdo></div>\n'
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
        # جدول المعاني
        table_rows = ""
        for i, w in enumerate(words):
            eng = escape(w.get("english",""))
            ara = escape(w.get("arabic",""))
            table_rows += f'<tr><td>{i+1}</td><td class="en" dir="ltr" style="text-align: left;">{eng}</td><td class="ar">{ara}</td></tr>\n'
        table = f'<div class="word-table-wrap"><table class="word-table"><thead><tr><th>#</th><th>English</th><th>العربية</th></tr></thead><tbody>{table_rows}</tbody></table></div>'
        
        # أسئلة المفردات (أول 20 سؤال)
        all_questions = [w.get("question") for w in words if w.get("question")]
        all_questions = all_questions[:20]  # 20 سؤال كحد أقصى
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
        
        # تخطيط متوازي (جدول + أسئلة) إذا كانت الأسئلة موجودة
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
    questions = questions[:20]  # 20 سؤال فقط
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
            rows += f'<tr><td>{idx}</td><td class="en" lang="en">{escape(eng)}</td><td class="ar">{escape(w.get("arabic",""))}</td></tr>\n'
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

# ---------- المقدمة باللغة الإنجليزية ----------
intro_text = """
<h2>Welcome to the APNE-ITC Comprehensive Guide</h2>
<p>This book is the fruit of extensive effort and dedication, designed to provide you with the most effective preparation for the <strong>APNE-ITC</strong> exam. Every section has been carefully crafted to ensure you master the required skills in reading, vocabulary, grammar, and dictation.</p>
<p>Over seven intensive days, with two hours of study per day, you will progress step by step through real exam materials, practical exercises, and full mock tests. The content is drawn from authentic sources and organized in a clear, logical sequence.</p>
<p>My goal is to make your learning journey as smooth and successful as possible. May this book be a key to your success, and may your hard work bring you the results you deserve.</p>

<div style="text-align:left; margin-top:3rem;">
    <strong>Author & Instructor</strong><br>
    <span style="font-size:1.2rem;">Anas Abdulrahman</span>
</div>
"""

html = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>APNE-ITC Master Guide – Al-Reyadah Training Institute</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;600;700&display=swap');
:root {
  --primary: #0b2b4f;
  --accent: #c4450c;
  --paper: #fffef9;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Amiri', serif;
  background: #f5f2eb;
  color: #1e1e1e;
  line-height: 2.2;
  font-size: 1.2rem;
  padding: 2rem 1rem;
}
.book {
  max-width: 1000px;
  margin: 0 auto;
  background: var(--paper);
  box-shadow: 0 20px 60px rgba(0,0,0,0.12);
  border-radius: 4px;
  padding: 3rem 3.5rem;
  position: relative;
}
.print-btn {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 999;
  background: var(--primary);
  color: white;
  border: none;
  padding: 12px 28px;
  font-size: 1.1rem;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  border-radius: 50px;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
  transition: all 0.3s;
}
.print-btn:hover { background: #00264d; transform: translateY(-2px); }
.cover { text-align: center; margin-bottom: 3rem; page-break-after: always;
    background: linear-gradient(135deg, #f9f9f9 0%, #ffffff 100%);
    padding: 4rem 2rem;
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}
.cover h1 {
    font-size: 4rem;
    color: var(--primary);
    font-weight: 700;
    margin-bottom: 1rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.05);
}
.cover .subtitle {
    font-size: 1.8rem;
    color: #555;
    margin-bottom: 2rem;
}
.cover .logo {
    margin: 3rem 0;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
}
.cover .author {
    font-size: 1.3rem;
    margin-top: 3rem;
    color: #444;
}
.cover .contact {
    font-size: 1rem;
    color: #777;
    margin-top: 0.5rem;
}
.section-title { font-size: 2rem; color: var(--primary); border-bottom: 3px solid var(--primary); padding-bottom: 0.3rem; margin: 3rem 0 1.5rem; }
article.passage { margin-bottom: 2.5rem; }
.passage-text { background: #f9f9f6; padding: 1.5rem; border-right: 5px solid var(--accent); margin: 1rem 0; white-space: pre-line; }
.questions ol { list-style: none; counter-reset: q-counter; }
.questions > ol > li::before { counter-increment: q-counter; content: counter(q-counter) ". "; font-weight: bold; color: var(--primary); }
table.word-table { width: 100%; border-collapse: collapse; margin: 1.5rem 0; }
table.word-table th { background: var(--primary); color: white; padding: 10px; font-family: 'Inter', sans-serif; }
table.word-table td, table.word-table th { border: 1px solid #ccc; padding: 8px 12px; }
.en { font-family: 'Inter', sans-serif; }

.dictation ul { list-style: square; padding-right: 2rem; }
.grammar-lesson { border: 1px solid #ddd; padding: 2rem; border-radius: 8px; background: #fafafa; margin: 1rem 0; }
.grammar-lesson table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
.grammar-lesson th { background: #e9ecef; padding: 8px; }
.grammar-lesson td { border: 1px solid #ddd; padding: 8px; }
.grammar-lesson h2, .grammar-lesson h3 { color: var(--primary); }
.grammar-lesson strong { color: var(--accent); }
.glossary { margin-top: 4rem; }
.references { margin-top: 4rem; }
.references p { margin: 0.3rem 0; }
.footer-note { text-align: center; margin-top: 4rem; padding: 2rem; background: #f0ede5; border-radius: 8px; }

.vocab-flex { display: flex; gap: 2rem; flex-wrap: wrap; }
.vocab-col { flex: 1 1 45%; }
.grammar-flex { display: flex; gap: 2rem; flex-wrap: wrap; margin-top: 1rem; }
.grammar-col { flex: 1 1 45%; }
.lesson-col { border-left: 1px solid #ddd; padding-left: 1rem; }
.test-col { padding-right: 1rem; }
@media (max-width: 768px) {
  .vocab-flex, .grammar-flex { flex-direction: column; }
  .vocab-col, .grammar-col { flex: 1 1 100%; }
  .lesson-col { border-left: none; padding-left: 0; }
  .test-col { padding-right: 0; }
  body { padding: 0.5rem; font-size: 1rem; }
  .book { padding: 1.5rem; }
  .cover h1 { font-size: 2.2rem; }
  .cover .subtitle { font-size: 1.1rem; }
  .section-title { font-size: 1.5rem; }
  .print-btn { padding: 8px 20px; font-size: 0.9rem; top: 10px; right: 10px; }
  table.word-table th, table.word-table td { padding: 6px; font-size: 0.85rem; }
}
@media (max-width: 480px) {
  .book { padding: 1rem; }
  .cover h1 { font-size: 1.8rem; }
  .cover .subtitle { font-size: 1rem; }
  .section-title { font-size: 1.3rem; }
}
@media print {
  body { background: white; padding: 0; }
  .book { box-shadow: none; border-radius: 0; padding: 2cm; max-width: 100%; }
  .print-btn { display: none; }
  @page { margin: 1.5cm; @bottom-center { content: counter(page); font-family: 'Amiri'; } }
  .section-title { page-break-before: always; }
  .cover { page-break-after: always; }
}
</style>
</head>
<body>
<button class="print-btn" onclick="window.print()">🖨️ طباعة / PDF</button>
<div class="book">
'''

# ---------- صفحة الغلاف ----------
html += '<div class="cover">'
html += '<img src="assets/images/reyadah-logo.png" alt="Reyadah Logo" class="logo" width="180">'
html += '<h1>APNE-ITC Master Guide</h1>'
html += '<p class="subtitle">The Ultimate Preparation Course<br>by Al-Reyadah Training Institute</p>'
html += '<p class="author"><strong>Anas Abdulrahman</strong><br>Instructor & Author</p>'
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
