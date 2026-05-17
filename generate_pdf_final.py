import json, os
from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display

class PDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font('Amiri', '', 'assets/fonts/Amiri-Regular.ttf')
        self.add_font('Amiri', 'B', 'assets/fonts/Amiri-Bold.ttf')
        self.set_auto_page_break(True, 20)
        self.alias_nb_pages()

    def header(self):
        if self.page_no() > 1 and os.path.exists('assets/images/reyadah-logo.png'):
            self.image('assets/images/reyadah-logo.png', 170, 8, 25)
            self.set_font('Amiri', '', 10)
            self.cell(0, 6, 'معهد الريادة للتدريب – كتاب APNE-ITC', align='C')
            self.ln(12)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font('Amiri', '', 8)
            self.cell(0, 10, str(self.page_no()), align='C')

    def reshaped(self, txt):
        if not txt: return ''
        reshaped = arabic_reshaper.reshape(txt)
        return get_display(reshaped)

    def ar_cell(self, txt, bold=False, size=12, align='R', w=0, h=8):
        if not txt: return
        self.set_font('Amiri', 'B' if bold else '', size)
        self.cell(w, h, self.reshaped(txt), align=align)

    def ar_multi(self, txt, bold=False, size=12, align='R'):
        if not txt: return
        self.set_font('Amiri', 'B' if bold else '', size)
        self.multi_cell(0, 7, self.reshaped(txt), align=align)

    def en_cell(self, txt, bold=False, size=12, align='L', w=0, h=8):
        if not txt: return
        self.set_font('Helvetica', 'B' if bold else '', size)
        self.cell(w, h, txt, align=align)

    def en_multi(self, txt, bold=False, size=12, align='L'):
        if not txt: return
        self.set_font('Helvetica', 'B' if bold else '', size)
        self.multi_cell(0, 7, txt, align=align)

    def section_title(self, title, level=1):
        if level == 1:
            self.set_font('Amiri', 'B', 18)
            self.ar_cell(title, True, 18, 'R', w=0, h=12)
            self.ln(8)
        elif level == 2:
            self.set_font('Amiri', 'B', 14)
            self.ar_cell(title, True, 14, 'R', w=0, h=10)
            self.ln(6)
        elif level == 3:
            self.set_font('Amiri', 'B', 12)
            self.ar_cell(title, True, 12, 'R', w=0, h=8)
            self.ln(4)

    def add_line(self):
        self.set_draw_color(200)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

def load_json(path):
    if not os.path.exists(path): return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def safe_question(q):
    if isinstance(q, dict):
        return q.get('q', ''), q.get('options', []), q.get('answer', -1)
    else:
        return str(q), [], -1

def print_questions(pdf, questions, size=10):
    for i, q in enumerate(questions):
        q_text, opts, ans = safe_question(q)
        pdf.ar_multi(f"{i+1}. {q_text}", size=size)
        for j, opt in enumerate(opts):
            mark = "✓" if j == ans else "○"
            pdf.ar_cell(f"  {mark} {opt}", size=size)
            pdf.ln(5)
        pdf.ln(2)

def extract_html_text(filepath):
    if not os.path.exists(filepath):
        return "الدرس غير متوفر حالياً."
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    from html.parser import HTMLParser
    class TextExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.text = []
        def handle_data(self, data):
            self.text.append(data.strip())
    extractor = TextExtractor()
    extractor.feed(html)
    return ' '.join([t for t in extractor.text if t])

pdf = PDF()
pdf.set_margin(20)

# ---------- غلاف ----------
pdf.add_page()
if os.path.exists('assets/images/reyadah-logo.png'):
    pdf.image('assets/images/reyadah-logo.png', x=75, y=40, w=60)
pdf.ln(70)
pdf.set_font('Amiri', 'B', 28)
pdf.ar_cell('English Grammar Master Guide', True, 28, 'C', w=0, h=14)
pdf.ln(12)
pdf.set_font('Amiri', 'B', 16)
pdf.ar_cell('APNE-ITC Preparation Course', True, 16, 'C')
pdf.ln(6)
pdf.ar_cell('معهد الريادة للتدريب', True, 16, 'C')
pdf.ln(20)
pdf.set_font('Amiri', '', 14)
pdf.ar_cell('إعداد المدرب: أنس عبد الرحمن', False, 14, 'C')
pdf.ln(8)
pdf.ar_cell('للتسجيل: 0546088130 – 0548775199', False, 12, 'C')

# ---------- مقدمة ----------
pdf.add_page()
pdf.section_title('مقدمة الكتاب')
intro = (
    "الحمد لله الذي علّم بالقلم، علّم الإنسان ما لم يعلم، والصلاة والسلام على سيدنا محمد ﷺ، خير معلمٍ للبشرية.\n\n"
    "أضع بين أيديكم هذا الكتاب التعليمي الشامل المخصص للتحضير لاختبار APNE-ITC، والذي صُمم بعناية ليكون دليلاً عملياً ومنهجاً تدريبياً متكاملاً يساعد الطلاب على بناء أساس قوي في اللغة الإنجليزية والاستعداد للاختبار بطريقة منظمة وواضحة.\n\n"
    "تم إعداد هذا البرنامج التدريبي وفق خطة مكثفة تمتد على سبعة أيام تدريبية، بواقع ساعتين يومياً.\n\n"
    "يحتوي هذا الكتاب على شرح مبسط للقواعد، مفردات مع تدريبات، قطع قراءة بأسئلة فهم، إملاء، اختبارات يومية، ستة تجميعات، مراجعة شاملة واختبار تجريبي.\n\n"
    "أسأل الله أن ينفع بهذا العمل وأن يكون سبباً في نجاح الطلبة."
)
pdf.ar_multi(intro, size=12)
pdf.ln(4)
pdf.ar_cell('المؤلف والمدرب', bold=True, size=12, align='L')
pdf.ar_cell('أنس عبد الرحمن', size=12, align='L')

# ---------- المنهج ----------
pdf.add_page()
pdf.section_title('المنهج الدراسي (Syllabus)')
syllabus = [
    ("اليوم 1", "Letter to the Editor", "Family & Body Parts", "Present/Past Simple"),
    ("اليوم 2", "The Risks of Farming", "Clothing & Weather", "Continuous Tenses"),
    ("اليوم 3", "Voluntary Service Overseas", "Health & Medicine", "Perfect Tenses"),
    ("اليوم 4", "Bicycles", "Food & Drink", "Passive Voice"),
    ("اليوم 5", "The Red Sea", "Jobs & Work", "Comparative/Superlative"),
    ("اليوم 6", "Diabetes", "Shopping & Materials", "Gerund/Infinitive"),
    ("اليوم 7", "مراجعة شاملة", "كل الكلمات", "مراجعة شاملة"),
]
col_w = [20, 45, 40, 45]
pdf.set_font('Amiri', 'B', 11)
for title, w in zip(['اليوم','القراءة','المفردات','القواعد'], col_w):
    pdf.cell(w, 8, title, border=1, align='C')
pdf.ln()
pdf.set_font('Amiri', '', 10)
for row in syllabus:
    for i, cell in enumerate(row):
        pdf.cell(col_w[i], 8, pdf.reshaped(cell), border=1, align='C')
    pdf.ln()

# ---------- أيام 1-6 ----------
day_titles = [
    "Letter to the Editor", "The Risks of Farming", "Voluntary Service Overseas",
    "Bicycles", "The Red Sea", "Diabetes"
]

for day in range(6):
    day_dir = f"content/day-{day+1:02d}"
    pdf.add_page()
    pdf.section_title(f'اليوم {day+1} – {day_titles[day]}', level=1)
    
    # --- قراءة (3 قطع) ---
    reading_path = f"{day_dir}/reading.json"
    reading_data = load_json(reading_path)
    if reading_data:
        passages = reading_data.get('passages', [])
        if not passages and isinstance(reading_data, list):
            passages = reading_data
        pdf.section_title(f'قطع القراءة ({len(passages)} قطع)', level=2)
        for pi, passage in enumerate(passages):
            title = passage.get('title', f'القطعة {pi+1}')
            text = passage.get('text', '')
            questions = passage.get('questions', [])
            pdf.section_title(title, level=3)
            pdf.ar_multi(text, size=10)
            pdf.ln(3)
            if questions:
                pdf.set_font('Amiri', 'B', 11)
                pdf.cell(0, 8, pdf.reshaped('أسئلة الفهم:'), align='R')
                pdf.ln(8)
                pdf.set_font('Amiri', '', 10)
                print_questions(pdf, questions, 10)
            pdf.add_line()
    
    # --- مفردات ---
    vocab_path = f"{day_dir}/vocabulary.json"
    vocab_data = load_json(vocab_path)
    if vocab_data:
        pdf.section_title('المفردات', level=2)
        words = vocab_data.get('words', [])
        if words:
            col_w_v = [10, 70, 70]
            pdf.set_font('Amiri', 'B', 10)
            pdf.cell(col_w_v[0], 8, '#', border=1)
            pdf.cell(col_w_v[1], 8, 'English', border=1)
            pdf.cell(col_w_v[2], 8, 'العربية', border=1)
            pdf.ln()
            pdf.set_font('Amiri', '', 9)
            for idx, w in enumerate(words):
                pdf.cell(col_w_v[0], 7, str(idx+1), border=1)
                pdf.cell(col_w_v[1], 7, w.get('english',''), border=1)
                pdf.cell(col_w_v[2], 7, pdf.reshaped(w.get('arabic','')), border=1)
                pdf.ln()
        questions = vocab_data.get('questions', [])
        if not questions and isinstance(vocab_data, list):
            questions = vocab_data
        if questions:
            pdf.set_font('Amiri', 'B', 11)
            pdf.cell(0, 8, pdf.reshaped('أسئلة المفردات:'), align='R')
            pdf.ln(8)
            pdf.set_font('Amiri', '', 10)
            print_questions(pdf, questions, 10)
        pdf.add_line()
    
    # --- إملاء (إن وجد) ---
    dict_path = f"{day_dir}/dictation.json"
    dict_data = load_json(dict_path)
    if dict_data:
        pdf.section_title('الإملاء', level=2)
        dict_words = dict_data.get('words', [])
        if not dict_words and isinstance(dict_data, list):
            dict_words = dict_data
        for w in dict_words:
            if isinstance(w, dict):
                correct = w.get('correct', '')
                options = w.get('options', [])
            else:
                correct = w
                options = []
            pdf.ar_cell(f"الكلمة الصحيحة: {correct}", size=10)
            pdf.ln(5)
            if options:
                pdf.ar_cell(f"الخيارات الخاطئة: {', '.join(options)}", size=10)
                pdf.ln(5)
        pdf.add_line()
    
    # --- درس قواعد ---
    grammar_html_path = f"{day_dir}/grammar.html"
    if os.path.exists(grammar_html_path):
        pdf.section_title('درس القواعد', level=2)
        grammar_text = extract_html_text(grammar_html_path)
        pdf.ar_multi(grammar_text, size=10)
        pdf.add_line()
    
    # --- اختبار قواعد ---
    gramtest_path = f"{day_dir}/grammar-test.json"
    gramtest_data = load_json(gramtest_path)
    if gramtest_data:
        pdf.section_title('اختبار القواعد', level=2)
        questions = gramtest_data.get('questions', []) if isinstance(gramtest_data, dict) else gramtest_data
        if questions:
            print_questions(pdf, questions, 10)
        pdf.add_line()
    
    # --- واجب منزلي (إن وجد) ---
    hw_path = f"{day_dir}/homework.json"
    hw_data = load_json(hw_path)
    if hw_data:
        pdf.section_title('الواجب المنزلي', level=2)
        hw_passages = hw_data.get('reading', []) if isinstance(hw_data, dict) else hw_data
        if isinstance(hw_passages, list):
            for hp in hw_passages:
                if isinstance(hp, dict):
                    htitle = hp.get('title', 'قطعة')
                    htext = hp.get('text', '')
                    hquestions = hp.get('questions', [])
                    pdf.section_title(htitle, level=3)
                    pdf.ar_multi(htext, size=10)
                    if hquestions:
                        print_questions(pdf, hquestions, 10)
        pdf.add_line()

# ---------- اليوم السابع (مراجعة) ----------
pdf.add_page()
pdf.section_title('اليوم السابع – المراجعة الشاملة', level=1)
pdf.ar_multi("مراجعة عامة على جميع المهارات والاختبار التجريبي النهائي.", size=12)

# ---------- التجميعات (إن وجدت) ----------
comp_dir = "content/exams"
if os.path.exists(comp_dir):
    pdf.add_page()
    pdf.section_title('التجميعات التدريبية', level=1)
    for i in range(1, 7):
        cpath = f"{comp_dir}/compilation-{i}.json"
        cdata = load_json(cpath)
        if cdata:
            pdf.section_title(f'تجميع {i}', level=2)
            if isinstance(cdata, list):
                print_questions(pdf, cdata, 9)

# ---------- مسرد الكلمات (من جميع الأيام) ----------
pdf.add_page()
pdf.section_title('مسرد الكلمات', level=1)
all_words = []
for day in range(6):
    vocab_path = f"content/day-{day+1:02d}/vocabulary.json"
    vdata = load_json(vocab_path)
    if vdata:
        words = vdata.get('words', [])
        if words:
            all_words.extend(words)
seen = set()
col_w_v = [10, 70, 70]
pdf.set_font('Amiri', 'B', 10)
pdf.cell(col_w_v[0], 8, '#', border=1)
pdf.cell(col_w_v[1], 8, 'English', border=1)
pdf.cell(col_w_v[2], 8, 'العربية', border=1)
pdf.ln()
pdf.set_font('Amiri', '', 9)
idx = 0
for w in all_words:
    eng = w.get('english','')
    if eng not in seen:
        seen.add(eng)
        idx += 1
        pdf.cell(col_w_v[0], 7, str(idx), border=1)
        pdf.en_cell(col_w_v[1], 7, eng)  # إنجليزي يسار
        pdf.cell(col_w_v[2], 7, pdf.reshaped(w.get('arabic','')), border=1)  # عربي يمين
        pdf.ln()

# ---------- ملاحق (مفاتيح الإجابات) ----------
pdf.add_page()
pdf.section_title('ملاحق – مفاتيح الإجابات', level=1)
for day in range(6):
    gramtest_path = f"content/day-{day+1:02d}/grammar-test.json"
    gdata = load_json(gramtest_path)
    if gdata:
        pdf.section_title(f'اليوم {day+1} – اختبار القواعد', level=2)
        questions = gdata.get('questions', []) if isinstance(gdata, dict) else gdata
        for i, q in enumerate(questions):
            q_text, opts, ans = safe_question(q)
            correct = opts[ans] if 0 <= ans < len(opts) else "—"
            pdf.ar_cell(f"{i+1}. {q_text} - {correct}", size=10)
            pdf.ln(5)

# ---------- المصادر والمراجع ----------
pdf.add_page()
pdf.section_title('المصادر والمراجع', level=1)
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
    pdf.ar_cell(f"• {r}", size=11)
    pdf.ln(7)

# تذييل
pdf.ln(10)
pdf.ar_cell('معهد الريادة للتدريب', bold=True, size=14, align='C')
pdf.ln(8)
pdf.ar_cell('إعداد المدرب: أنس عبد الرحمن', size=12, align='C')
pdf.ln(6)
pdf.ar_cell('للتسجيل: 0546088130 | 0548775199', size=12, align='C')

pdf.output('APNE-ITC-Book.pdf')
print("✅ تم إنشاء PDF الكامل بنجاح")
