import json, os, html as html_mod

def load_json(path):
    if not os.path.exists(path): return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def escape(txt):
    return html_mod.escape(str(txt)) if txt else ""

def q_li(q_text, opts):
    html_code = f'<li class="q-en"><span class="q-text">{escape(q_text)}</span>\n<ol type="a" class="opts-en">\n'
    for opt in opts:
        html_code += f'<li class="opt-en">{escape(opt)}</li>\n'
    html_code += '</ol></li>\n'
    return html_code

def build_reading(day_num):
    r = load_json(f"content/day-{day_num:02d}/reading.json")
    if not r: return ""
    passages = r.get("passages", [])
    if not passages and isinstance(r, list):
        passages = r
    sec = f'<section class="reading"><h2 class="section-title">📖 قطع القراءة ({len(passages)} قطع)</h2>\n'
    for pi, p in enumerate(passages):
        title = escape(p.get("title", f"Passage {pi+1}"))
        text  = escape(p.get("text", "")).replace("\n", "<br>")
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
        all_questions = [w.get("question") for w in words if w.get("question")]
        all_questions = all_questions[:20]
        if all_questions:
            sec += '<ol class="q-list">\n'
            for q in all_questions:
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
    questions = g.get("questions", []) if isinstance(g, dict) else g
    if not questions: return ""
    sec = '<section class="grammar-test"><h2 class="section-title">📘 اختبار القواعد</h2>\n<ol class="q-list">\n'
    for q in questions:
        sec += q_li(q.get("q", ""), q.get("options", []))
    sec += '</ol>\n</section>\n'
    return sec

def build_compilation(i):
    c = load_json(f"content/exams/compilation-{i}.json")
    if not c: return ""
    questions = c if isinstance(c, list) else c.get("questions", [])
    if not questions: return ""
    sec = f'<section class="compilation"><h2 class="section-title">📋 تجميع {i}</h2>\n<ol class="q-list">\n'
    for q in questions:
        sec += q_li(q.get("q", ""), q.get("options", []))
    sec += '</ol>\n</section>\n'
    return sec

def get_daily_tips(day):
    tips = {
        1: [
            "1️⃣ <b>قاعدة ذهبية:</b> لا تحفظ الكلمة وحدها، بل احفظها في جملة. اكتب ثلاث جمل من عندك لكل كلمة جديدة.",
            "2️⃣ <b>للقراءة:</b> قبل أن تقرأ القطعة، ألقِ نظرة سريعة على الأسئلة لتعرف ما الذي تبحث عنه.",
            "3️⃣ <b>للقواعد:</b> ركّز اليوم على الفرق بين <em>Present Simple</em> و <em>Past Simple</em>.",
            "4️⃣ <b>للإملاء:</b> الكلمات التي تنتهي بـ <em>-tion</em> و <em>-sion</em> غالباً ما تكون أسماء.",
            "5️⃣ <b>للتحفيز:</b> أنهِ هذا اليوم وأنت تشعر أنك أضفت 10 كلمات جديدة لرصيدك."
        ],
        2: [
            "1️⃣ <b>قاعدة ذهبية:</b> كرر كلمات الأمس قبل أن تبدأ درس اليوم. التكرار المتباعد يثبّت المعلومات.",
            "2️⃣ <b>للقراءة:</b> لا تتوقف عند كل كلمة صعبة. حاول تخمين المعنى من السياق أولاً.",
            "3️⃣ <b>للقواعد:</b> الأزمنة المستمرة تحتاج دائماً إلى <em>am/is/are + V-ing</em>.",
            "4️⃣ <b>للإملاء:</b> انتبه للكلمات التي تحتوي على حروف صامتة مثل <em>k</em> في <em>knife</em>.",
            "5️⃣ <b>للاسترخاء:</b> خذ نفساً عميقاً بين كل قسم وآخر. العقل المتعب لا يحفظ."
        ],
        3: [
            "1️⃣ <b>قاعدة ذهبية:</b> اربط الكلمة بصورة ذهنية. كلما كانت الصورة أغرب، كان التذكر أقوى.",
            "2️⃣ <b>للقراءة:</b> بعد قراءة الفقرة، اسأل نفسك: 'ما الفكرة الرئيسية هنا؟' ولخّصها في جملة.",
            "3️⃣ <b>للقواعد:</b> <em>Present Perfect</em> يربط الماضي بالحاضر (have/has + V3).",
            "4️⃣ <b>للإملاء:</b> تذكر قاعدة <em>i</em> قبل <em>e</em> إلا بعد <em>c</em> (مثل <em>believe</em>, <em>receive</em>).",
            "5️⃣ <b>للصحة:</b> اشرب ماءً كثيراً أثناء المذاكرة. الجفاف يضعف التركيز."
        ],
        4: [
            "1️⃣ <b>قاعدة ذهبية:</b> اكتب الكلمات الصعبة على بطاقات صغيرة وراجعها في أوقات الانتظار.",
            "2️⃣ <b>للقراءة:</b> لاحظ أدوات الربط (<em>however, therefore, although</em>) فهي تكشف علاقة الأفكار.",
            "3️⃣ <b>للقواعد:</b> المبني للمجهول (<em>Passive</em>) = <em>be + V3</em>، شائع في النصوص العلمية.",
            "4️⃣ <b>للإملاء:</b> انتبه للفرق بين <em>their</em> (ملكهم)، <em>there</em> (هناك)، و <em>they're</em> (هم يكونون).",
            "5️⃣ <b>للتحفيز:</b> أنت في منتصف الطريق. الإنجاز يغذي الهمة، فاستمر."
        ],
        5: [
            "1️⃣ <b>قاعدة ذهبية:</b> استخدم أسلوب 'المراجعة قبل النوم'. ما تراجعه قبل النوم يثبته الدماغ أثناء النوم.",
            "2️⃣ <b>للقراءة:</b> تدرب على قراءة الأسئلة أولاً، ثم البحث عن الإجابات في النص (Scanning).",
            "3️⃣ <b>للقواعد:</b> للمقارنة: <em>-er than</em> أو <em>more ... than</em>. للتفضيل: <em>the ... -est</em> أو <em>the most ...</em>.",
            "4️⃣ <b>للإملاء:</b> الكلمات التي تنتهي بـ <em>-ful</em> تُكتب بحرف <em>l</em> واحد (مثل <em>beautiful</em>).",
            "5️⃣ <b>لإدارة الوقت:</b> خصص 25 دقيقة تركيز كامل، ثم 5 دقائق راحة."
        ],
        6: [
            "1️⃣ <b>قاعدة ذهبية:</b> اربط ما تتعلمه اليوم بما تعلمته في الأيام السابقة. المعرفة شبكة متصلة.",
            "2️⃣ <b>للقراءة:</b> عند مواجهة كلمة لا تعرفها، انظر إلى جذرها (Root) فقد يذكرك بكلمة تعرفها.",
            "3️⃣ <b>للقواعد:</b> بعض الأفعال يأتي بعدها <em>V-ing</em> (مثل <em>enjoy, mind</em>) وبعضها <em>to + V</em> (مثل <em>want, decide</em>).",
            "4️⃣ <b>للإملاء:</b> انتبه للكلمات التي يتغير هجاؤها بين الاسم والفعل، مثل <em>advise</em> (فعل) و <em>advice</em> (اسم).",
            "5️⃣ <b>للثقة:</b> ثق بقدراتك. كل خطأ تتعلم منه هو درجة تصعد بها نحو النجاح."
        ],
        7: [
            "1️⃣ <b>قاعدة ذهبية:</b> لا تذاكر شيئاً جديداً اليوم. ركّز على مراجعة الأخطاء السابقة فقط.",
            "2️⃣ <b>للقراءة:</b> جرّب أن تقرأ القطعة بصوت عالٍ وكأنك تشرحها لغيرك. هذا يثبّت الفهم.",
            "3️⃣ <b>للقواعد:</b> أعد قراءة ملاحظاتك على القواعد التي أخطأت فيها خلال الأسبوع.",
            "4️⃣ <b>للإملاء:</b> اكتب الكلمات التي لطالما أخطأت في تهجئتها خمس مرات متتالية.",
            "5️⃣ <b>للحصاد:</b> أنت اليوم تجني ثمرة أسبوع كامل من الجد والاجتهاد. ثق بالله، وتوكل عليه، وامضِ مطمئناً."
        ]
    }
    tip_html = '<div class="daily-tips">'
    for tip in tips.get(day, []):
        tip_html += f'<div class="tip-item">{tip}</div>'
    tip_html += '</div>'
    return tip_html

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
    vocab_topic   = get_vocab_topic(d)
    grammar = ["Present/Past Simple", "Continuous Tenses", "Perfect Tenses",
               "Passive Voice", "Comparative/Superlative", "Gerund/Infinitive",
               "قواعد جديدة ومراجعة شاملة"][d-1]
    syllabus_rows += (
        f'<tr>'
        f'<td>اليوم {d}</td>'
        f'<td class="en-cell">{escape(reading_title)}</td>'
        f'<td class="en-cell">{escape(vocab_topic)}</td>'
        f'<td>{grammar}</td>'
        f'</tr>\n'
    )

day_titles = [get_reading_title(d) for d in range(1, 8)]

intro_text = """
<h2 class="en-title">Welcome to the APNE-ITC Comprehensive Guide</h2>
<p>This book is the fruit of extensive effort and dedication, designed to provide you with the most effective preparation for the <strong>APNE-ITC</strong> exam. Every section has been carefully crafted to ensure you master the required skills in reading, vocabulary, grammar, and dictation.</p>
<p>Over seven intensive days, with two hours of study per day, you will progress step by step through real exam materials, practical exercises, and full mock tests.</p>
<p><em>To the light of my life, my first teacher, my father.</em></p>
<div class="intro-sign">
    <strong>English Zone Team</strong><br>
    <span>Al-Reyadah Training Institute</span>
</div>
"""

html = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>APNE-ITC Master Guide – Al-Reyadah Training Institute</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400;1,700&family=Tajawal:wght@400;500;700&family=Inter:wght@400;500;600;700&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap');

:root {
  --primary: #0b2b4f;
  --accent:  #c4450c;
  --paper:   #fffef9;
  --text:    #1e1e1e;
  --border:  #e0e0e0;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Amiri', 'Tajawal', serif;
  background: #f5f2eb;
  color: var(--text);
  line-height: 2;
  font-size: 1.15rem;
  padding: 2rem 1rem;
  direction: rtl;
}

.en-title {
  direction: ltr;
  unicode-bidi: isolate;
  text-align: left;
}

.en-cell {
  direction: ltr;
  unicode-bidi: isolate;
  text-align: left;
}

.passage-text {
  direction: ltr;
  unicode-bidi: isolate;
  text-align: left;
  background: #f9f9f6;
  padding: 1rem 1.2rem;
  border-left: 5px solid var(--accent);
  margin: 0.8rem 0;
  white-space: pre-line;
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 1rem;
  border-radius: 4px;
}

li.q-en {
  direction: ltr;
  unicode-bidi: isolate;
  text-align: left;
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 1rem;
  margin-bottom: 0.8rem;
  list-style: none;
}

ol.q-list {
  counter-reset: q-counter;
  padding: 0;
  margin: 0.5rem 0;
}
ol.q-list > li.q-en::before {
  counter-increment: q-counter;
  content: counter(q-counter) ". ";
  font-weight: 700;
  color: var(--primary);
  margin-left: 0;
}

ol.opts-en {
  list-style: lower-alpha;
  direction: ltr;
  unicode-bidi: isolate;
  text-align: left;
  padding-left: 1.8rem;
  margin-top: 0.3rem;
}
li.opt-en {
  direction: ltr;
  unicode-bidi: isolate;
  font-family: 'Inter', sans-serif;
  font-size: 0.97rem;
  margin-bottom: 0.2rem;
}

ul.dict-list {
  list-style: square;
  padding-left: 2rem;
  direction: ltr;
  unicode-bidi: isolate;
}
li.dict-item {
  direction: ltr;
  unicode-bidi: isolate;
  font-family: 'Inter', sans-serif;
  margin-bottom: 0.5rem;
}

.intro-sign {
  direction: ltr;
  unicode-bidi: isolate;
  text-align: left;
  margin-top: 3rem;
}

.book {
  max-width: 210mm;
  margin: 0 auto;
  background: var(--paper);
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
  border-radius: 4px;
  padding: 2.5cm 2cm;
}

.print-btn {
  position: fixed;
  top: 20px; right: 20px;
  z-index: 999;
  background: var(--primary);
  color: white;
  border: none;
  padding: 10px 24px;
  font-size: 1rem;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  border-radius: 50px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  transition: all .3s;
}
.print-btn:hover { background: #00264d; transform: translateY(-2px); }

.cover {
  text-align: center;
  margin-bottom: 3rem;
  page-break-after: always;
  background: linear-gradient(135deg, #f9f9f9 0%, #ffffff 100%);
  padding: 4rem 2rem;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}
.cover h1        { font-size: 3.5rem; color: var(--primary); font-weight: 700; margin-bottom: 1rem; direction: ltr; }
.cover .subtitle { font-size: 1.5rem; color: #555; margin-bottom: 2rem; direction: ltr; }
.cover .logo     { margin: 2rem 0; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1)); }
.cover .author   { font-size: 1.2rem; margin-top: 2rem; color: #444; direction: ltr; }
.cover .contact  { font-size: 0.95rem; color: #777; margin-top: 0.5rem; direction: ltr; }

.section-title {
  font-size: 1.6rem;
  color: var(--primary);
  border-bottom: 3px solid var(--primary);
  padding-bottom: 0.4rem;
  margin: 2rem 0 1rem;
}

article.passage        { margin-bottom: 2rem; }
.passage h3.en-title   { font-size: 1.2rem; color: var(--primary); margin-bottom: 0.5rem; }
.questions h4          { margin: 0.8rem 0 0.4rem; }

table.word-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}
table.word-table th {
  background: var(--primary);
  color: white;
  padding: 8px;
  font-family: 'Inter', sans-serif;
}
table.word-table td,
table.word-table th {
  border: 1px solid var(--border);
  padding: 6px 10px;
}

.daily-tips {
  background: #fef9e7;
  border-right: 5px solid #f39c12;
  padding: 0.8rem 1rem;
  margin: 1rem 0;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #7d6608;
  line-height: 1.9;
}
.tip-item {
  margin-bottom: 0.5rem;
  padding-bottom: 0.3rem;
  border-bottom: 1px dashed #e0c36a;
}
.tip-item:last-child { border-bottom: none; margin-bottom: 0; }

.side-by-side {
  display: flex;
  gap: 2rem;
  margin: 1.5rem 0;
  align-items: flex-start;
}
.side-left  { flex: 1 1 55%; }
.side-right { flex: 1 1 45%; }

.footer-note {
  text-align: center;
  margin-top: 4rem;
  padding: 1.5rem;
  background: #f0ede5;
  border-radius: 8px;
}

@media (max-width: 800px) {
  .side-by-side { flex-direction: column; }
  .book { padding: 1.5rem; }
}

@media print {
  @page {
    size: A4 portrait;
    margin: 1.8cm 1.5cm 2cm 1.5cm;
    @top-left {
      content: "APNE-ITC Master Guide";
      font-family: 'Inter', sans-serif;
      font-size: 8pt;
      color: #888;
      border-bottom: 0.5pt solid #ccc;
      padding-bottom: 4pt;
    }
    @top-right {
      content: "Al-Reyadah Training Institute";
      font-family: 'Inter', sans-serif;
      font-size: 8pt;
      color: #888;
      border-bottom: 0.5pt solid #ccc;
      padding-bottom: 4pt;
    }
    @bottom-center {
      content: "— " counter(page) " —";
      font-family: 'Amiri', serif;
      font-size: 10pt;
      color: #555;
    }
  }

  @page :first {
    @top-left   { content: none; }
    @top-right  { content: none; }
    @bottom-center { content: none; }
  }

  body {
    background: white !important;
    padding: 0 !important;
    font-size: 10pt !important;
    line-height: 1.65 !important;
    color: #111 !important;
  }

  .book {
    box-shadow: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
    max-width: 100% !important;
    margin: 0 !important;
  }

  .print-btn { display: none !important; }

  .cover {
    page-break-after: always !important;
    break-after: page !important;
    min-height: 24cm;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    background: white !important;
    padding: 3cm 2cm !important;
  }
  .cover h1        { font-size: 28pt !important; margin-bottom: 0.6cm; }
  .cover .subtitle { font-size: 14pt !important; }
  .cover .author   { font-size: 12pt !important; }
  .cover .contact  { font-size: 10pt !important; }
  .cover .logo     { width: 120px !important; }

  .day { page-break-before: always !important; break-before: page !important; }

  .section-title {
    font-size: 14pt !important;
    border-bottom: 2pt solid #0b2b4f !important;
    padding-bottom: 3pt !important;
    margin: 0 0 8pt !important;
    color: #0b2b4f !important;
  }

  .passage-text {
    font-size: 9.5pt !important;
    line-height: 1.6 !important;
    padding: 6pt 10pt !important;
    border-left: 3pt solid #c4450c !important;
    background: #fafaf8 !important;
    margin: 6pt 0 !important;
  }

  li.q-en {
    font-size: 9.5pt !important;
    line-height: 1.55 !important;
    margin-bottom: 5pt !important;
  }
  li.opt-en {
    font-size: 9pt !important;
    line-height: 1.5 !important;
  }
  ol.opts-en { margin-top: 2pt !important; padding-left: 14pt !important; }

  li.dict-item { font-size: 9.5pt !important; margin-bottom: 3pt !important; }

  .side-by-side {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 1cm !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    align-items: flex-start !important;
  }
  .side-left  {
    flex: 0 0 55% !important;
    width: 55% !important;
    max-width: 55% !important;
  }
  .side-right {
    flex: 0 0 42% !important;
    width: 42% !important;
    max-width: 42% !important;
  }

  table.word-table {
    width: 100% !important;
    font-size: 9.5pt !important;
    border-collapse: collapse !important;
  }
  table.word-table th { font-size: 9pt !important; padding: 4pt 6pt !important; }
  table.word-table td { padding: 3pt 6pt !important; }

  .daily-tips {
    font-size: 9pt !important;
    line-height: 1.5 !important;
    padding: 5pt 8pt !important;
    margin: 6pt 0 !important;
    border-right: 3pt solid #f39c12 !important;
    background: #fffbe6 !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }
  .tip-item { margin-bottom: 3pt !important; padding-bottom: 2pt !important; }

  .compilation { page-break-before: always !important; break-before: page !important; }

  .footer-note {
    font-size: 9pt !important;
    padding: 8pt !important;
    margin-top: 1cm !important;
    background: #f0ede5 !important;
    page-break-inside: avoid !important;
  }

  article.passage   { page-break-inside: avoid !important; break-inside: avoid !important; }
  .questions        { page-break-inside: avoid !important; break-inside: avoid !important; }
  .dictation        { page-break-inside: avoid !important; break-inside: avoid !important; }

  h2.section-title, h3.en-title {
    page-break-after: avoid !important;
    break-after: avoid !important;
  }
}
</style>
</head>
<body>
<button class="print-btn" onclick="window.print()">🖨️ طباعة / PDF</button>
<div class="book">
'''

html += '<div class="cover">'
html += '<img src="assets/images/reyadah-logo.png" alt="Reyadah Logo" class="logo" width="150">'
html += '<h1>APNE-ITC Master Guide</h1>'
html += '<p class="subtitle">The Ultimate Preparation Course<br>by Al-Reyadah Training Institute</p>'
html += '<p class="author"><strong>English Zone Team</strong></p>'
html += '<p class="contact">📞 0546088130 | 0548775199</p>'
html += '</div>'

html += '<section class="intro">'
html += '<h2 class="section-title">📝 مقدمة الكتاب</h2>'
html += intro_text
html += '</section>'

html += '<section class="syllabus">'
html += '<h2 class="section-title">📅 المنهج الدراسي</h2>'
html += '<table class="word-table"><thead><tr><th>اليوم</th><th>القراءة</th><th>المفردات</th><th>القواعد</th></tr></thead><tbody>'
html += syllabus_rows
html += '</tbody></table></section>'

for d in range(1, 8):
    html += f'<div class="day" id="day-{d}">'
    html += f'<h1 class="section-title">🗓️ اليوم {d} – <span class="en-title" style="font-size:inherit;">{day_titles[d-1]}</span></h1>'
    html += get_daily_tips(d)
    html += build_reading(d)
    html += '<div class="side-by-side">'
    html += '<div class="side-left">'  + build_vocab(d)        + '</div>'
    html += '<div class="side-right">' + build_grammar_test(d) + '</div>'
    html += '</div>'
    html += build_dictation(d)
    html += '</div>'

html += '<section class="compilations">'
for i in range(1, 7):
    html += build_compilation(i)
html += '</section>'

html += '<div class="footer-note">'
html += '<p><strong>Al-Reyadah Training Institute</strong><br>English Zone Team<br>📞 0546088130 | 0548775199</p>'
html += '</div>'

html += '</div></body></html>'

with open('textbook.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ تم بناء الكتاب — النصوص الإنجليزية LTR والعربية RTL")
