import json, os, html as html_mod

def load_json(path):
    if not os.path.exists(path): return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def escape(txt):
    return html_mod.escape(str(txt)) if txt else ""

def wrap_en(txt):
    if not txt: return ""
    # إجبار النص الإنجليزي على LTR مع عزل كامل
    return f'<span dir="ltr" style="unicode-bidi:isolate; direction:ltr;">{txt}</span>'

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
        sec += f'<div class="passage-text" dir="ltr">{text}</div>\n'
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
        all_questions = [w.get("question") for w in words if w.get("question")]
        all_questions = all_questions[:20]
        if all_questions:
            sec += '<div class="vocab-questions"><ol>\n'
            for q in all_questions:
                q_text = escape(q.get("q", ""))
                opts = q.get("options", [])
                sec += f'<li>{wrap_en(q_text)}<ol type="a">\n'
                for opt in opts:
                    sec += f'<li>{wrap_en(escape(opt))}</li>\n'
                sec += '</ol></li>\n'
            sec += '</ol></div>\n'
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

def build_grammar_test(day_num):
    g = load_json(f"content/day-{day_num:02d}/grammar-test.json")
    if not g: return ""
    questions = g.get("questions", []) if isinstance(g, dict) else g
    if not questions: return ""
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

# ====== نصائح يومية ======
def get_daily_tips(day):
    tips = {
        1: [
            "1️⃣ <b>قاعدة ذهبية:</b> لا تحفظ الكلمة وحدها، بل احفظها في جملة. اكتب ثلاث جمل من عندك لكل كلمة جديدة.",
            "2️⃣ <b>للقراءة:</b> قبل أن تقرأ القطعة، ألقِ نظرة سريعة على الأسئلة لتعرف ما الذي تبحث عنه.",
            "3️⃣ <b>للقواعد:</b> ركّز اليوم على الفرق بين <em>Present Simple</em> و <em>Past Simple</em>، واستخدم كلمات الزمن الدالة (yesterday, always).",
            "4️⃣ <b>للإملاء:</b> الكلمات التي تنتهي بـ <em>-tion</em> و <em>-sion</em> غالباً ما تكون أسماء. تدرب على كتابتها.",
            "5️⃣ <b>للتحفيز:</b> أنت تبدأ رحلة الألف ميل بخطوة. أنهِ هذا اليوم وأنت تشعر أنك أضفت 10 كلمات جديدة لرصيدك."
        ],
        2: [
            "1️⃣ <b>قاعدة ذهبية:</b> كرر كلمات الأمس قبل أن تبدأ درس اليوم. التكرار المتباعد يثبّت المعلومات.",
            "2️⃣ <b>للقراءة:</b> لا تتوقف عند كل كلمة صعبة. حاول تخمين المعنى من السياق أولاً.",
            "3️⃣ <b>للقواعد:</b> لاحظ أن الأزمنة المستمرة (<em>Continuous</em>) تحتاج دائماً إلى <em>am/is/are + V-ing</em>.",
            "4️⃣ <b>للإملاء:</b> انتبه للكلمات التي تحتوي على حروف صامتة مثل <em>k</em> في <em>knife</em> أو <em>w</em> في <em>write</em>.",
            "5️⃣ <b>للاسترخاء:</b> خذ نفساً عميقاً بين كل قسم وآخر. العقل المتعب لا يحفظ."
        ],
        3: [
            "1️⃣ <b>قاعدة ذهبية:</b> اربط الكلمة بصورة ذهنية. كلما كانت الصورة أغرب، كان التذكر أقوى.",
            "2️⃣ <b>للقراءة:</b> بعد قراءة الفقرة، اسأل نفسك: 'ما الفكرة الرئيسية هنا؟' ولخّصها في جملة.",
            "3️⃣ <b>للقواعد:</b> <em>Present Perfect</em> يربط الماضي بالحاضر. فكر فيه كجسر زمني (have/has + V3).",
            "4️⃣ <b>للإملاء:</b> الكلمات التي تحتوي على <em>ie</em> أو <em>ei</em> (مثل <em>believe</em>, <em>receive</em>) لها قاعدة: <em>i</em> قبل <em>e</em> إلا بعد <em>c</em>.",
            "5️⃣ <b>للصحة:</b> اشرب ماءً كثيراً أثناء المذاكرة. الجفاف يضعف التركيز."
        ],
        4: [
            "1️⃣ <b>قاعدة ذهبية:</b> اكتب الكلمات الصعبة على بطاقات صغيرة وراجعها في أوقات الانتظار.",
            "2️⃣ <b>للقراءة:</b> لاحظ أدوات الربط (<em>however, therefore, although</em>) فهي تكشف علاقة الأفكار.",
            "3️⃣ <b>للقواعد:</b> تذكّر أن المبني للمجهول (<em>Passive</em>) يتكون من <em>be + V3</em>، وهو شائع في النصوص العلمية.",
            "4️⃣ <b>للإملاء:</b> انتبه للفرق بين <em>their</em> (ملكهم)، <em>there</em> (هناك)، و <em>they're</em> (هم يكونون).",
            "5️⃣ <b>للتحفيز:</b> أنت في منتصف الطريق. الإنجاز يغذي الهمة، فاستمر."
        ],
        5: [
            "1️⃣ <b>قاعدة ذهبية:</b> استخدم أسلوب 'المراجعة قبل النوم'. ما تراجعه قبل النوم يثبته الدماغ أثناء النوم.",
            "2️⃣ <b>للقراءة:</b> تدرب على قراءة الأسئلة أولاً، ثم البحث عن الإجابات في النص (Scanning).",
            "3️⃣ <b>للقواعد:</b> للمقارنة بين شيئين استخدم <em>-er than</em> أو <em>more ... than</em>. للتفضيل استخدم <em>the ... -est</em> أو <em>the most ...</em>.",
            "4️⃣ <b>للإملاء:</b> الكلمات التي تنتهي بـ <em>-ful</em> (مثل <em>beautiful</em>) تُكتب بحرف <em>l</em> واحد في النهاية.",
            "5️⃣ <b>لإدارة الوقت:</b> خصص 25 دقيقة تركيز كامل، ثم 5 دقائق راحة. هذه التقنية تزيد الإنتاجية."
        ],
        6: [
            "1️⃣ <b>قاعدة ذهبية:</b> اربط ما تتعلمه اليوم بما تعلمته في الأيام السابقة. المعرفة شبكة متصلة.",
            "2️⃣ <b>للقراءة:</b> عند مواجهة كلمة لا تعرفها، انظر إلى جذرها (Root) فقد يذكرك بكلمة تعرفها.",
            "3️⃣ <b>للقواعد:</b> لاحظ أن بعض الأفعال يأتي بعدها <em>V-ing</em> (مثل <em>enjoy, mind, suggest</em>) وبعضها <em>to + V</em> (مثل <em>want, decide, hope</em>).",
            "4️⃣ <b>للإملاء:</b> انتبه للكلمات التي يتغير هجاؤها بين الاسم والفعل، مثل <em>advise</em> (فعل) و <em>advice</em> (اسم).",
            "5️⃣ <b>للثقة:</b> ثق بقدراتك. كل خطأ تتعلم منه هو درجة تصعد بها نحو النجاح."
        ],
        7: [
            "1️⃣ <b>قاعدة ذهبية:</b> لا تذاكر شيئاً جديداً اليوم. ركّز على مراجعة الأخطاء السابقة فقط.",
            "2️⃣ <b>للقراءة:</b> جرّب أن تقرأ القطعة بصوت عالٍ وكأنك تشرحها لغيرك. هذا يثبّت الفهم.",
            "3️⃣ <b>للقواعد:</b> أعد قراءة ملاحظاتك على القواعد التي أخطأت فيها خلال الأسبوع. التكرار يصنع الإتقان.",
            "4️⃣ <b>للإملاء:</b> اكتب الكلمات التي لطالما أخطأت في تهجئتها خمس مرات متتالية.",
            "5️⃣ <b>للحصاد:</b> أنت اليوم تجني ثمرة أسبوع كامل من الجد والاجتهاد. ثق بالله، وتوكل عليه، وامضِ مطمئناً."
        ]
    }
    tip_html = '<div class="daily-tips">'
    for tip in tips.get(day, []):
        tip_html += f'<div class="tip-item">{tip}</div>'
    tip_html += '</div>'
    return tip_html

# ====== توليد المنهج ======
syllabus_rows = ""
for d in range(1, 8):
    reading_title = get_reading_title(d)
    vocab_topic = get_vocab_topic(d)
    grammar = ["Present/Past Simple", "Continuous Tenses", "Perfect Tenses",
               "Passive Voice", "Comparative/Superlative", "Gerund/Infinitive",
               "قواعد جديدة ومراجعة شاملة"][d-1]
    syllabus_rows += f'<tr><td>اليوم {d}</td><td>{escape(reading_title)}</td><td>{escape(vocab_topic)}</td><td>{grammar}</td></tr>\n'

day_titles = [get_reading_title(d) for d in range(1, 8)]

intro_text = """
<h2>Welcome to the APNE-ITC Comprehensive Guide</h2>
<p>This book is the fruit of extensive effort and dedication...</p>
<p><em>To the light of my life, my first teacher, my father.</em></p>
<div style="text-align:left; margin-top:3rem;">
    <strong>Author & Instructor</strong><br>
    <span style="font-size:1.2rem;">English Zone Team</span>
</div>
"""

# ====== HTML ======
html = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>APNE-ITC Master Guide – Al-Reyadah Training Institute</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;600;700&display=swap');
:root { --primary: #0b2b4f; --accent: #c4450c; --paper: #fffef9; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Amiri', serif; background: #f5f2eb; color: #1e1e1e; line-height: 2.2; font-size: 1.2rem; padding: 2rem 1rem; }
.book { max-width: 1100px; margin: 0 auto; background: var(--paper); box-shadow: 0 20px 60px rgba(0,0,0,0.12); border-radius: 4px; padding: 3rem 3.5rem; position: relative; }
.print-btn { position: fixed; top: 20px; right: 20px; z-index: 999; background: var(--primary); color: white; border: none; padding: 12px 28px; font-size: 1.1rem; font-family: 'Inter', sans-serif; font-weight: 600; border-radius: 50px; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: all .3s; }
.print-btn:hover { background: #00264d; transform: translateY(-2px); }
.cover { text-align: center; margin-bottom: 3rem; page-break-after: always; background: linear-gradient(135deg,#f9f9f9,#fff); padding: 4rem 2rem; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
.cover h1 { font-size: 4rem; color: var(--primary); font-weight: 700; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.05); }
.cover .subtitle { font-size: 1.8rem; color: #555; margin-bottom: 2rem; }
.cover .logo { margin: 3rem 0; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1)); }
.cover .author { font-size: 1.3rem; margin-top: 3rem; color: #444; }
.cover .contact { font-size: 1rem; color: #777; margin-top: .5rem; }
.section-title { font-size: 1.8rem; color: var(--primary); border-bottom: 3px solid var(--primary); padding-bottom: .3rem; margin: 2rem 0 1rem; }
article.passage { margin-bottom: 2rem; }
.passage-text { background: #f9f9f6; padding: 1.2rem; border-right: 5px solid var(--accent); margin: 1rem 0; white-space: pre-line; font-size: 1rem; }
.questions ol { list-style: none; counter-reset: q-counter; }
.questions > ol > li::before { counter-increment: q-counter; content: counter(q-counter) ". "; font-weight: bold; color: var(--primary); }
table.word-table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
table.word-table th { background: var(--primary); color: white; padding: 8px; font-family: 'Inter', sans-serif; }
table.word-table td, table.word-table th { border: 1px solid #ccc; padding: 6px 10px; }
.en { font-family: 'Inter', sans-serif; }
.dictation ul { list-style: square; padding-right: 2rem; }
.grammar-test h2.section-title { font-size: 1.5rem; }
.daily-tips { background: #fef9e7; border-right: 5px solid #f39c12; padding: 1rem; margin: 1rem 0; border-radius: 10px; font-size: 0.95rem; color: #7d6608; line-height: 1.9; }
.tip-item { margin-bottom: 0.6rem; padding-bottom: 0.4rem; border-bottom: 1px dashed #e0c36a; }
.tip-item:last-child { border-bottom: none; margin-bottom: 0; }
.footer-note { text-align: center; margin-top: 4rem; padding: 2rem; background: #f0ede5; border-radius: 8px; }

/* تخطيط متوازي: القراءة (يمين) + القواعد (يسار) */
.day-flex { display: flex; gap: 2rem; margin: 1.5rem 0; }
.reading-col { flex: 0 0 60%; }
.grammar-col { flex: 0 0 38%; }
@media (max-width: 800px) { .day-flex { flex-direction: column; } .reading-col, .grammar-col { flex: 0 0 100%; } }

/* إصلاح نهائي لاتجاه النص الإنجليزي */
[dir="ltr"] { direction: ltr !important; text-align: left !important; unicode-bidi: isolate !important; }

@media print { body { background: white; padding: 0; } .book { box-shadow: none; border-radius: 0; padding: 1.5cm; max-width: 100%; } .print-btn { display: none; } @page { margin: 1.5cm; @bottom-center { content: counter(page); font-family: 'Amiri'; } } .section-title { page-break-before: always; } .cover { page-break-after: always; } }
</style>
</head>
<body>
<button class="print-btn" onclick="window.print()">🖨️ طباعة / PDF</button>
<div class="book">
'''

# ====== الغلاف ======
html += '<div class="cover">'
html += '<img src="assets/images/reyadah-logo.png" alt="Reyadah Logo" class="logo" width="180">'
html += '<h1>APNE-ITC Master Guide</h1>'
html += '<p class="subtitle">The Ultimate Preparation Course<br>by Al-Reyadah Training Institute</p>'
html += '<p class="author"><strong>English Zone Team</strong></p>'
html += '<p class="contact">📞 0546088130 | 0548775199</p>'
html += '</div>'

# ====== المقدمة ======
html += '<section class="intro">'
html += '<h2 class="section-title">مقدمة الكتاب</h2>'
html += intro_text
html += '</section>'

# ====== المنهج ======
html += '<section class="syllabus">'
html += '<h2 class="section-title">المنهج الدراسي</h2>'
html += '<table class="word-table"><thead><tr><th>اليوم</th><th>القراءة</th><th>المفردات</th><th>القواعد</th></tr></thead><tbody>'
html += syllabus_rows
html += '</tbody></table></section>'

# ====== الأيام ======
for d in range(1, 8):
    html += f'<div class="day" id="day-{d}">'
    html += f'<h1 class="section-title">اليوم {d} – {day_titles[d-1]}</h1>'
    html += get_daily_tips(d)
    html += '<div class="day-flex">'
    html += '<div class="reading-col">'
    html += build_reading(d)
    html += '</div>'
    html += '<div class="grammar-col">'
    html += build_grammar_test(d)
    html += '</div>'
    html += '</div>'
    html += build_vocab(d)
    html += build_dictation(d)
    html += '</div>'

# ====== التجميعات ======
html += '<section class="compilations">'
for i in range(1, 7):
    html += build_compilation(i)
html += '</section>'

# ====== التذييل ======
html += '<div class="footer-note">'
html += '<p><strong>Al-Reyadah Training Institute</strong><br>English Zone Team<br>0546088130 | 0548775199</p>'
html += '</div>'

html += '</div></body></html>'

with open('textbook.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ تم بناء الكتاب مع إصلاح الاتجاه الإنجليزي وتقليل الهوامش")
