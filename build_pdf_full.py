import json, os, textwrap
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
        if self.page_no() > 1:
            if os.path.exists('assets/images/reyadah-logo.png'):
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
        reshaped = arabic_reshaper.reshape(str(txt))
        return get_display(reshaped)

    # -------- خلية عربية (سطر واحد) --------
    def ar_cell(self, txt, bold=False, size=12, align='R', w=0, h=8, border=0):
        if not txt: return
        self.set_font('Amiri', 'B' if bold else '', size)
        self.cell(w, h, self.reshaped(txt), border=border, align=align)

    # -------- خلية إنجليزية (سطر واحد) --------
    def en_cell(self, txt, bold=False, size=12, align='L', w=0, h=8, border=0):
        if not txt: return
        self.set_font('Helvetica', 'B' if bold else '', size)
        self.cell(w, h, str(txt), border=border, align=align)

    # -------- نص عربي متعدد الأسطر (يُجزّأ تلقائياً) --------
    def ar_multi(self, txt, bold=False, size=12, align='R'):
        if not txt: return
        self.set_font('Amiri', 'B' if bold else '', size)
        # تقسيم النص إلى فقرات صغيرة حتى لا يتجاوز عرض الصفحة
        for paragraph in txt.split('\n'):
            paragraph = paragraph.strip()
            if not paragraph:
                self.ln(4)
                continue
            # إذا كان النص طويلاً جداً، نقسمه إلى جمل قصيرة
            if len(paragraph) > 200:
                chunks = textwrap.wrap(paragraph, width=150)
            else:
                chunks = [paragraph]
            for chunk in chunks:
                self.multi_cell(0, 7, self.reshaped(chunk), align=align)

    # -------- عنوان قسم --------
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

    # -------- خط فاصل --------
    def add_line(self):
        self.set_draw_color(200)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

def load_json(path):
    if not os.path.exists(path): return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def print_questions(pdf, questions, size=10):
    """طباعة قائمة أسئلة (اختيار من متعدد)"""
    for i, q in enumerate(questions):
        if isinstance(q, dict):
            q_text = q.get('q', '')
            opts = q.get('options', [])
            ans = q.get('answer', -1)
        else:
            q_text = str(q)
            opts = []
            ans = -1
        pdf.ar_multi(f"{i+1}. {q_text}", size=size)
        for j, opt in enumerate(opts):
            mark = "✓" if j == ans else "○"
            pdf.ar_cell(f"  {mark} {opt}", size=size)
            pdf.ln(5)
        pdf.ln(2)

def extract_html_text(filepath):
    """استخراج النص من ملف HTML الخاص بدرس القواعد"""
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

# ========== الغلاف ==========
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

# ========== مقدمة ==========
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

# ========== المنهج ==========
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

# ========== أيام 1 – 6 ==========
day_titles = [
    "Letter to the Editor", "The Risks of Farming", "Voluntary Service Overseas",
    "Bicycles", "The Red Sea", "Diabetes"
]

for day in range(6):
    day_dir = f"content/day-{day+1:02d}"
    pdf.add_page()
    pdf.section_title(f'اليوم {day+1} – {day_titles[day]}', level=1)

    # ----- قطع القراءة -----
    reading = load_json(f"{day_dir}/reading.json")
    if reading:
        passages = reading.get('passages', [])
        if not passages and isinstance(reading, list):
            passages = reading
        pdf.section_title(f'قطع القراءة ({len(passages)} قطع)', level=2)
        for p_idx, passage in enumerate(passages):
            title = passage.get('title', f'القطعة {p_idx+1}')
            text = passage.get('text', '')
            questions = passage.get('questions', [])
            pdf.section_title(title, level=3)
            pdf.ar_multi(text, size=10)
            pdf.ln(3)
            if questions:
                pdf.set_font('Amiri', 'B', 11)
                pdf.ar_cell('أسئلة الفهم:', size=11)
                pdf.ln(6)
                print_questions(pdf, questions, 10)
            pdf.add_line()
    else:
        pdf.ar_cell('⚠️ ملف القراءة غير موجود', size=10)
        pdf.ln(6)

    # ----- المفردات -----
    vocab = load_json(f"{day_dir}/vocabulary.json")
    if vocab:
        pdf.section_title('المفردات', level=2)
        words = vocab.get('words', [])
        if words:
            # جدول الكلمات
            col_v = [10, 70, 70]
            pdf.set_font('Amiri', 'B', 10)
            pdf.cell(col_v[0], 8, '#', border=1)
            pdf.cell(col_v[1], 8, 'English', border=1)
            pdf.cell(col_v[2], 8, 'العربية', border=1)
            pdf.ln()
            pdf.set_font('Amiri', '', 9)
            for idx, w in enumerate(words):
                pdf.cell(col_v[0], 7, str(idx+1), border=1)
                pdf.en_cell(w.get('english',''), size=9, w=col_v[1], h=7, border=1)
                pdf.cell(col_v[2], 7, pdf.reshaped(w.get('arabic','')), border=1)
                pdf.ln()
        # أسئلة المفردات
        questions = vocab.get('questions', [])
        if not questions and isinstance(vocab, list):
            questions = vocab
        if questions:
            pdf.set_font('Amiri', 'B', 11)
            pdf.ar_cell('أسئلة المفردات:', size=11)
            pdf.ln(6)
            print_questions(pdf, questions, 10)
        pdf.add_line()
    else:
        pdf.ar_cell('⚠️ ملف المفردات غير موجود', size=10)
        pdf.ln(6)

    # ----- الإملاء (إن وجد) -----
    dict_data = load_json(f"{day_dir}/dictation.json")
    if dict_data:
        pdf.section_title('الإملاء', level=2)
        dict_words = dict_data.get('words', []) if isinstance(dict_data, dict) else dict_data
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

    # ----- درس القواعد -----
    grammar_html = f"{day_dir}/grammar.html"
    if os.path.exists(grammar_html):
        pdf.section_title('درس القواعد', level=2)
        grammar_text = extract_html_text(grammar_html)
        pdf.ar_multi(grammar_text, size=10)
        pdf.add_line()
    else:
        pdf.ar_cell('⚠️ درس القواعد غير موجود', size=10)
        pdf.ln(6)

    # ----- اختبار القواعد -----
    gramtest = load_json(f"{day_dir}/grammar-test.json")
    if gramtest:
        pdf.section_title('اختبار القواعد', level=2)
        questions = gramtest.get('questions', []) if isinstance(gramtest, dict) else gramtest
        if questions:
            print_questions(pdf, questions, 10)
        pdf.add_line()
    else:
        pdf.ar_cell('⚠️ اختبار القواعد غير موجود', size=10)
        pdf.ln(6)

# ========== اليوم السابع (مراجعة) ==========
pdf.add_page()
pdf.section_title('اليوم السابع – المراجعة الشاملة', level=1)
pdf.ar_multi("مراجعة عامة على جميع المهارات والاختبار التجريبي النهائي.", size=12)

# ========== التجميعات ==========
comp_dir = "content/exams"
if os.path.exists(comp_dir):
    pdf.add_page()
    pdf.section_title('التجميعات التدريبية (1-6)', level=1)
    for i in range(1, 7):
        cdata = load_json(f"{comp_dir}/compilation-{i}.json")
        if cdata:
            pdf.section_title(f'تجميع {i}', level=2)
            if isinstance(cdata, list):
                print_questions(pdf, cdata, 9)
            elif isinstance(cdata, dict):
                qs = cdata.get('questions', [])
                if qs:
                    print_questions(pdf, qs, 9)
            pdf.add_line()

# ========== مسرد الكلمات ==========
pdf.add_page()
pdf.section_title('مسرد الكلمات (Glossary)', level=1)
all_words = []
for day in range(6):
    v = load_json(f"content/day-{day+1:02d}/vocabulary.json")
    if v:
        words = v.get('words', [])
        all_words.extend(words)
seen = set()
col_v = [10, 70, 70]
pdf.set_font('Amiri', 'B', 10)
pdf.cell(col_v[0], 8, '#', border=1)
pdf.cell(col_v[1], 8, 'English', border=1)
pdf.cell(col_v[2], 8, 'العربية', border=1)
pdf.ln()
pdf.set_font('Amiri', '', 9)
idx = 0
for w in all_words:
    eng = w.get('english','')
    if eng not in seen:
        seen.add(eng)
        idx += 1
        pdf.cell(col_v[0], 7, str(idx), border=1)
        pdf.en_cell(eng, size=9, w=col_v[1], h=7, border=1)
        pdf.cell(col_v[2], 7, pdf.reshaped(w.get('arabic','')), border=1)
        pdf.ln()

# ========== ملاحق (مفاتيح الإجابات) ==========
pdf.add_page()
pdf.section_title('ملاحق – مفاتيح الإجابات', level=1)
for day in range(6):
    gramtest = load_json(f"content/day-{day+1:02d}/grammar-test.json")
    if gramtest:
        pdf.section_title(f'اليوم {day+1} – اختبار القواعد', level=2)
        questions = gramtest.get('questions', []) if isinstance(gramtest, dict) else gramtest
        for i, q in enumerate(questions):
            if isinstance(q, dict):
                q_text = q.get('q', '')
                opts = q.get('options', [])
                ans = q.get('answer', -1)
                correct = opts[ans] if 0 <= ans < len(opts) else "—"
            else:
                q_text = str(q)
                correct = "—"
            pdf.ar_cell(f"{i+1}. {q_text[:80]} - {correct}", size=9)
            pdf.ln(4)

# ========== المصادر والمراجع ==========
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

# ========== تذييل ==========
pdf.ln(10)
pdf.ar_cell('معهد الريادة للتدريب', bold=True, size=14, align='C')
pdf.ln(8)
pdf.ar_cell('إعداد المدرب: أنس عبد الرحمن', size=12, align='C')
pdf.ln(6)
pdf.ar_cell('للتسجيل: 0546088130 | 0548775199', size=12, align='C')

pdf.output('APNE-ITC-Book.pdf')
print("✅ تم إنشاء PDF الكامل بنجاح – حجم الملف:", round(os.path.getsize('APNE-ITC-Book.pdf')/1024, 1), "KB")
