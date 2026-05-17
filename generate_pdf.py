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
        if self.page_no() > 1:
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
        self.multi_cell(0, 8, self.reshaped(txt), align=align)

    def section_title(self, title, level=1):
        if level == 1:
            self.set_font('Amiri', 'B', 18)
            self.ar_cell(title, True, 18, 'R', w=0, h=12)
            self.ln(8)
        elif level == 2:
            self.set_font('Amiri', 'B', 14)
            self.ar_cell(title, True, 14, 'R', w=0, h=10)
            self.ln(6)

    def add_line(self):
        self.set_draw_color(200)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def safe_question(self, q):
        """يتعامل مع الأسئلة سواء كانت dict أو str"""
        if isinstance(q, dict):
            return q.get('q', ''), q.get('options', []), q.get('answer', -1)
        else:
            return str(q), [], -1

def load_json(path):
    if not os.path.exists(path): return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

pdf = PDF()
pdf.set_margin(20)

# ---------- غلاف ----------
pdf.add_page()
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
    "أضع بين أيديكم هذا الكتاب التعليمي الشامل المخصص للتحضير لاختبار APNE-ITC...\n"
    "أسأل الله أن ينفع بهذا العمل."
)
pdf.ar_multi(intro, size=12)
pdf.ln(4)
pdf.ar_cell('المؤلف والمدرب', bold=True, size=12, align='L')
pdf.ar_cell('أنس عبد الرحمن', size=12, align='L')

# ---------- منهج ----------
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
pdf.cell(col_w[0], 8, 'اليوم', border=1, align='C')
pdf.cell(col_w[1], 8, 'القراءة', border=1, align='C')
pdf.cell(col_w[2], 8, 'المفردات', border=1, align='C')
pdf.cell(col_w[3], 8, 'القواعد', border=1, align='C')
pdf.ln()
pdf.set_font('Amiri', '', 10)
for row in syllabus:
    for i, cell in enumerate(row):
        pdf.cell(col_w[i], 8, pdf.reshaped(cell), border=1, align='C')
    pdf.ln()

# ---------- أيام 1-6 ----------
reading_files = [
    ("letter-editor.json", "Letter to the Editor"),
    ("risks-farming.json", "The Risks of Farming"),
    ("vso.json", "Voluntary Service Overseas"),
    ("bicycles.json", "Bicycles"),
    ("red-sea.json", "The Red Sea"),
    ("diabetes.json", "Diabetes"),
]
vocab_files = [
    "family-body.json", "clothing-weather.json", "health-medicine.json",
    "food-drink.json", "jobs-work.json", "shopping-materials.json"
]
grammar_files = [
    "present-past-simple.html", "continuous.html", "perfect.html",
    "passive.html", "comparative.html", "gerund.html"
]
grammar_test_files = [
    "present-past-simple.json", "continuous.json", "perfect.json",
    "passive.json", "comparative.json", "gerund.json"
]

def print_questions(questions, size=10):
    for i, q in enumerate(questions):
        q_text, opts, ans = pdf.safe_question(q)
        pdf.ar_multi(f"{i+1}. {q_text}", size=size)
        for j, opt in enumerate(opts):
            mark = "✓" if j == ans else "○"
            pdf.ar_cell(f"  {mark} {opt}", size=size)
            pdf.ln(5)
        pdf.ln(2)

for day in range(6):
    pdf.add_page()
    pdf.section_title(f'اليوم {day+1} – {reading_files[day][1]}', level=1)
    
    pdf.section_title('قطع القراءة', level=2)
    rdata = load_json(f"content/reading/{reading_files[day][0]}")
    if rdata:
        passage = rdata.get("passage", "")
        questions = rdata.get("questions", [])
        pdf.ar_multi(passage, size=10)
        pdf.ln(3)
        if questions:
            pdf.set_font('Amiri', 'B', 11)
            pdf.cell(0, 8, 'الأسئلة:', ln=True)
            pdf.set_font('Amiri', '', 10)
            print_questions(questions, 10)
    pdf.add_line()
    
    pdf.section_title('المفردات', level=2)
    vdata = load_json(f"content/vocabulary/topics/{vocab_files[day]}")
    if vdata:
        words = vdata.get('words', [])
        if not words:
            questions = vdata if isinstance(vdata, list) else vdata.get('questions', [])
            if questions:
                print_questions(questions, 10)
        else:
            col_w = [10, 70, 70]
            pdf.set_font('Amiri', 'B', 10)
            pdf.cell(col_w[0], 8, '#', border=1)
            pdf.cell(col_w[1], 8, 'English', border=1)
            pdf.cell(col_w[2], 8, 'العربية', border=1)
            pdf.ln()
            pdf.set_font('Amiri', '', 9)
            for idx, w in enumerate(words):
                pdf.cell(col_w[0], 7, str(idx+1), border=1)
                pdf.cell(col_w[1], 7, w.get('english',''), border=1)
                pdf.cell(col_w[2], 7, pdf.reshaped(w.get('arabic','')), border=1)
                pdf.ln()
    pdf.add_line()
    
    pdf.section_title('درس القواعد', level=2)
    gpath = f"content/grammar/{grammar_files[day]}"
    if os.path.exists(gpath):
        with open(gpath, 'r', encoding='utf-8') as f:
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
        grammar_text = ' '.join([t for t in extractor.text if t])
        pdf.ar_multi(grammar_text, size=10)
    pdf.add_line()
    
    pdf.section_title('اختبار القواعد', level=2)
    gtdata = load_json(f"content/grammar-tests/{grammar_test_files[day]}")
    if gtdata:
        print_questions(gtdata, 10)

# ---------- اليوم السابع ----------
pdf.add_page()
pdf.section_title('اليوم السابع – المراجعة الشاملة والاختبار التجريبي', level=1)
pdf.ar_multi("في هذا اليوم يتم مراجعة جميع قطع القراءة والمفردات والقواعد، وحل الاختبار التجريبي النهائي.", size=11)

# ---------- تجميعات ----------
pdf.add_page()
pdf.section_title('التجميعات التدريبية (1-6)', level=1)
for i in range(1, 7):
    cdata = load_json(f"content/exams/compilation-{i}.json")
    if cdata:
        pdf.section_title(f'تجميع {i}', level=2)
        if isinstance(cdata, list):
            print_questions(cdata, 9)

# ---------- مسرد ----------
pdf.add_page()
pdf.section_title('مسرد الكلمات', level=1)
all_words = []
for day in range(6):
    vdata = load_json(f"content/vocabulary/topics/{vocab_files[day]}")
    if vdata:
        words = vdata.get('words', [])
        all_words.extend(words)
seen = set()
col_w = [10, 70, 70]
pdf.set_font('Amiri', 'B', 10)
pdf.cell(col_w[0], 8, '#', border=1)
pdf.cell(col_w[1], 8, 'English', border=1)
pdf.cell(col_w[2], 8, 'العربية', border=1)
pdf.ln()
pdf.set_font('Amiri', '', 9)
idx = 0
for w in all_words:
    eng = w.get('english','')
    if eng not in seen:
        seen.add(eng)
        idx += 1
        pdf.cell(col_w[0], 7, str(idx), border=1)
        pdf.cell(col_w[1], 7, eng, border=1)
        pdf.cell(col_w[2], 7, pdf.reshaped(w.get('arabic','')), border=1)
        pdf.ln()

# ---------- ملاحق ----------
pdf.add_page()
pdf.section_title('ملاحق – مفاتيح الإجابات', level=1)
pdf.section_title('اختبارات القواعد', level=2)
for day in range(6):
    gtdata = load_json(f"content/grammar-tests/{grammar_test_files[day]}")
    if gtdata:
        pdf.section_title(f'اليوم {day+1}', level=3)
        for i, q in enumerate(gtdata):
            q_text, opts, ans = pdf.safe_question(q)
            correct = opts[ans] if 0 <= ans < len(opts) else "—"
            pdf.ar_cell(f"{i+1}. {q_text} → {correct}", size=10)
            pdf.ln(5)

pdf.section_title('التجميعات', level=2)
for i in range(1, 7):
    cdata = load_json(f"content/exams/compilation-{i}.json")
    if cdata:
        pdf.section_title(f'تجميع {i}', level=3)
        for idx, q in enumerate(cdata):
            q_text, opts, ans = pdf.safe_question(q)
            correct = opts[ans] if 0 <= ans < len(opts) else "—"
            pdf.ar_cell(f"{idx+1}. {q_text} → {correct}", size=10)
            pdf.ln(5)

# ---------- مصادر ----------
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

# ---------- تذييل ----------
pdf.ln(10)
pdf.ar_cell('معهد الريادة للتدريب', bold=True, size=14, align='C')
pdf.ln(8)
pdf.ar_cell('إعداد المدرب: أنس عبد الرحمن', size=12, align='C')
pdf.ln(6)
pdf.ar_cell('للتسجيل: 0546088130 | 0548775199', size=12, align='C')

pdf.output('APNE-ITC-Book.pdf')
print("✅ تم إنشاء PDF بنجاح")
