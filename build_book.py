import json, os

def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def esc(t):
    if t is None: return ""
    return str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def reading_section(filepath):
    data = load_json(filepath)
    if not data:
        return ""
    html = ""
    passage = data.get("passage", "")
    questions = data.get("questions", [])
    html += '<div class="passage">' + esc(passage).replace('\n', '<br>') + '</div>'
    if questions:
        html += '<ol class="questions">'
        for q in questions:
            html += f'<li>{esc(q.get("q",""))}<br>'
            for i, opt in enumerate(q.get("options", [])):
                html += f'{"✅" if i == q.get("answer", -1) else "○"} {esc(opt)}<br>'
            html += '</li>'
        html += '</ol>'
    return html

def vocab_section(filepath):
    data = load_json(filepath)
    if not data:
        return "", []
    words_list = []
    words = data.get("words", [])
    if not words:
        # قد يكون الملف بصيغة أسئلة فقط (questions)
        questions = data if isinstance(data, list) else data.get("questions", [])
        if questions:
            html = '<ol>'
            for q in questions:
                html += f'<li>{esc(q.get("q",""))}<br>'
                for i, opt in enumerate(q.get("options", [])):
                    html += f'{"✅" if i == q.get("answer", -1) else "○"} {esc(opt)}<br>'
                html += '</li>'
            html += '</ol>'
            return html, []
        return "", []
    for w in words:
        words_list.append({"english": w.get("english",""), "arabic": w.get("arabic","")})
    html = '<table><tr><th>#</th><th>الإنجليزية</th><th>العربية</th></tr>'
    for i, w in enumerate(words):
        html += f'<tr><td>{i+1}</td><td><strong>{esc(w["english"])}</strong></td><td>{esc(w["arabic"])}</td></tr>'
    html += '</table>'
    return html, words_list

def grammar_lesson(filepath):
    if not os.path.exists(filepath):
        return ""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def grammar_test(filepath):
    data = load_json(filepath)
    if not data:
        return ""
    html = '<ol>'
    for q in data:
        html += f'<li>{esc(q.get("q",""))}<br>'
        for i, opt in enumerate(q.get("options", [])):
            html += f'{"✅" if i == q.get("answer", -1) else "○"} {esc(opt)}<br>'
        html += '</li>'
    html += '</ol>'
    return html

# أيام المنصة مع ملفاتها الحقيقية
DAYS = [
    (1, "Letter to the Editor", "content/reading/letter-editor.json", "content/vocabulary/topics/family-body.json", "content/grammar/present-past-simple.html", "content/grammar-tests/present-past-simple.json"),
    (2, "The Risks of Farming", "content/reading/risks-farming.json", "content/vocabulary/topics/clothing-weather.json", "content/grammar/continuous.html", "content/grammar-tests/continuous.json"),
    (3, "Voluntary Service Overseas", "content/reading/vso.json", "content/vocabulary/topics/health-medicine.json", "content/grammar/perfect.html", "content/grammar-tests/perfect.json"),
    (4, "Bicycles", "content/reading/bicycles.json", "content/vocabulary/topics/food-drink.json", "content/grammar/passive.html", "content/grammar-tests/passive.json"),
    (5, "The Red Sea", "content/reading/red-sea.json", "content/vocabulary/topics/jobs-work.json", "content/grammar/comparative.html", "content/grammar-tests/comparative.json"),
    (6, "Diabetes", "content/reading/diabetes.json", "content/vocabulary/topics/shopping-materials.json", "content/grammar/gerund.html", "content/grammar-tests/gerund.json"),
]

# بداية الكتاب
book = '<!DOCTYPE html>\n<html lang="ar" dir="rtl">\n<head>\n<meta charset="UTF-8">\n'
book += '<title>كتاب APNE-ITC – معهد الريادة للتدريب</title>\n'
book += '<style>\n'
book += '''
  @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Tajawal', sans-serif; background: #fff; color: #1a1a2e; line-height: 2; padding: 2rem; max-width: 1100px; margin: auto; }
  h1 { font-size: 2.6rem; color: #00264d; text-align: center; margin-bottom: 0.5rem; border-bottom: 4px solid #0071e3; padding-bottom: 1rem; }
  h2 { font-size: 2rem; color: #00264d; border-right: 8px solid #0071e3; padding-right: 0.8rem; margin: 3rem 0 1.2rem; }
  h3 { font-size: 1.5rem; color: #004080; margin: 1.8rem 0 1rem; background: #f4f8ff; padding: 0.4rem 1rem; border-radius: 10px; }
  h4 { font-size: 1.2rem; color: #0059b3; margin: 1rem 0 0.5rem; }
  table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
  th, td { border: 1px solid #ccc; padding: 8px 10px; text-align: right; font-size: 0.95rem; }
  th { background: #0059b3; color: #fff; }
  tr:nth-child(even) td { background: #fafcff; }
  .cover { text-align: center; margin: 2rem 0 3rem; page-break-after: always; }
  .cover h1 { border: none; font-size: 3rem; margin-bottom: 1.5rem; }
  .cover .subtitle { font-size: 1.4rem; color: #555; margin: 0.5rem 0; }
  .page-break { page-break-before: always; }
  .passage { background: #f9fafb; padding: 1.2rem; border-radius: 12px; border-right: 5px solid #0071e3; margin: 1rem 0; white-space: pre-line; }
  .questions { list-style-type: none; padding-right: 1.5rem; }
  .questions li::before { content: "📌 "; color: #0071e3; }
  .answer-key { background: #e8f5e9; padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0; }
  .footer-note { text-align: center; margin-top: 3rem; padding: 1.5rem; background: linear-gradient(135deg, #eef3fd, #fff); border-radius: 16px; color: #0059b3; }
  .toc a { color: #0071e3; text-decoration: none; }
  .toc ol { list-style: none; counter-reset: toc-counter; }
  .toc li { counter-increment: toc-counter; margin: 0.5rem 0; }
  .toc li::before { content: counter(toc-counter) ". "; font-weight: bold; color: #0071e3; }
  @media print {
    body { padding: 1.5cm 1cm; }
    @page { @bottom-center { content: counter(page); font-size: 12px; font-family: 'Tajawal'; } }
    h2 { page-break-before: always; }
  }
</style>\n</head>\n<body>\n'''

# ---------- غلاف ----------
book += '<div class="cover">\n'
book += '<h1>📚 English Grammar Master Guide</h1>\n'
book += '<p class="subtitle"><strong>APNE-ITC Preparation Course</strong></p>\n'
book += '<p class="subtitle">معهد الريادة للتدريب</p>\n'
book += '<p style="margin-top:1.5rem;">إعداد المدرب: <strong>أنس عبد الرحمن</strong></p>\n'
book += '<p>للتسجيل: <strong>0546088130</strong> – <strong>0548775199</strong></p>\n'
book += '<p style="margin-top:1rem; font-size:0.9rem; color:#888;">الموقع: english-zone.github.io/itc-apne-prep</p>\n'
book += '</div>\n'

# ---------- فهرس المحتويات ----------
book += '<div class="page-break"></div>\n'
book += '<h2>📑 فهرس المحتويات</h2>\n'
book += '<div class="toc">\n<ol>\n'
for i, (day, title, rfile, vfile, gfile, gtfile) in enumerate(DAYS, 1):
    book += f'<li><a href="#day-{i}">اليوم {i} – {title}</a></li>\n'
book += '<li><a href="#day-7">اليوم السابع – المراجعة الشاملة والاختبار التجريبي</a></li>\n'
book += '<li><a href="#compilations">📋 التجميعات (1-6)</a></li>\n'
book += '<li><a href="#glossary">📖 مسرد الكلمات</a></li>\n'
book += '<li><a href="#appendix">📎 الملاحق – مفاتيح الإجابات</a></li>\n'
book += '<li><a href="#references">📚 المصادر والمراجع</a></li>\n'
book += '</ol>\n</div>\n'

# ---------- مقدمة الكتاب الكاملة ----------
book += '<div class="page-break"></div>\n'
book += '<h2>📝 مقدمة الكتاب</h2>\n'
book += '''<p>الحمد لله الذي علّم بالقلم، علّم الإنسان ما لم يعلم، والصلاة والسلام على سيدنا محمد ﷺ، خير معلمٍ للبشرية.</p>

<p>أضع بين أيديكم هذا الكتاب التعليمي الشامل المخصص للتحضير لاختبار <strong>APNE-ITC</strong>، والذي صُمم بعناية ليكون دليلاً عملياً ومنهجاً تدريبياً متكاملاً يساعد الطلاب على بناء أساس قوي في اللغة الإنجليزية والاستعداد للاختبار بطريقة منظمة وواضحة.</p>

<p>تم إعداد هذا البرنامج التدريبي وفق خطة مكثفة تمتد على <strong>سبعة أيام تدريبية</strong>، بواقع <strong>ساعتين يومياً</strong>، بحيث يمر الطالب بشكل تدريجي على أهم المهارات المطلوبة في الاختبار من قراءة، وقواعد، ومفردات، وتمارين تطبيقية، ومراجعات عملية.</p>

<p>يحتوي هذا الكتاب على:</p>
<ul>
<li>شرح مبسط ومنظم لقواعد اللغة الإنجليزية الأكثر أهمية في الاختبار.</li>
<li>مفردات أساسية ومتكررة مع تدريبات وأسئلة تطبيقية.</li>
<li>قطع قراءة متنوعة مع أسئلة فهم تساعد على تطوير مهارة الاستيعاب والتحليل.</li>
<li>تدريبات إملاء (Dictation) وأنشطة تعليمية داعمة للتثبيت والمراجعة.</li>
<li>اختبارات وتمارين يومية لتقييم التقدم بشكل مستمر.</li>
<li><strong>ستة تجميعات تدريبية كاملة</strong> تحاكي نمط الأسئلة المتوقعة وتساعد الطالب على رفع جاهزيته للاختبار.</li>
<li>مراجعة شاملة واختبار تجريبي في نهاية البرنامج لتثبيت المهارات وتعزيز الثقة قبل الاختبار.</li>
</ul>

<p>لقد روعي في إعداد هذا الكتاب أن يكون عملياً وسهل الاستخدام، بحيث يستطيع الطالب الاستفادة منه داخل القاعة التدريبية أو بشكل ذاتي، مع التركيز على تبسيط المعلومة، وتقديمها بصورة واضحة، وربطها بأمثلة وتمارين تساعد على الفهم السريع والتطبيق المباشر.</p>

<p>إن هذا العمل هو ثمرة جهد وتجربة تعليمية هدفت إلى تقديم محتوى تدريبي منظم وفعّال يختصر الطريق على الطالب، ويساعده على الاستعداد لاختبار <strong>APNE-ITC</strong> بثقة وكفاءة بإذن الله.</p>

<p>أسأل الله أن ينفع بهذا العمل، وأن يكون سبباً في نجاح الطلبة وتحقيق طموحاتهم، وأن يجعل فيه الفائدة والتوفيق للجميع.</p>

<br>
<div style="text-align:left; margin-top:2rem;">
<strong>المؤلف والمدرب</strong><br>
أنس عبد الرحمن
</div>\n'''

# ---------- المنهج ----------
book += '<div class="page-break"></div>\n'
book += '<h2>📅 المنهج الدراسي (Syllabus)</h2>\n'
book += '<table><tr><th>اليوم</th><th>القراءة</th><th>المفردات</th><th>القواعد</th></tr>\n'
for i, (day, title, *_) in enumerate(DAYS, 1):
    book += f'<tr><td><strong>Day {i}</strong></td><td>{title}</td><td>{title.split("|")[1] if "|" in title else ""}</td><td>...</td></tr>\n'
book += '<tr><td><strong>Day 7</strong></td><td colspan="3">مراجعة شاملة + اختبار تجريبي + جميع الكلمات</td></tr>\n'
book += '</table>\n'

# ---------- أيام 1-6 ----------
all_glossary_words = []

for i, (day, title, rfile, vfile, gfile, gtfile) in enumerate(DAYS, 1):
    book += f'<div class="page-break"></div>\n'
    book += f'<h2 id="day-{i}">📘 اليوم {i} – {title}</h2>\n'
    
    # قراءة
    book += '<h3>📖 قطعة القراءة</h3>\n'
    book += reading_section(rfile)
    
    # مفردات
    book += '<h3>📝 المفردات</h3>\n'
    vhtml, words = vocab_section(vfile)
    book += vhtml
    all_glossary_words.extend(words)
    
    # درس قواعد
    book += '<h3>📚 درس القواعد</h3>\n'
    book += '<div class="grammar-content">\n'
    book += grammar_lesson(gfile)
    book += '\n</div>\n'
    
    # اختبار قواعد
    book += '<h3>📝 اختبار القواعد</h3>\n'
    book += grammar_test(gtfile)

# ---------- اليوم السابع (مراجعة) ----------
book += '<div class="page-break"></div>\n'
book += '<h2 id="day-7">📘 اليوم السابع – المراجعة الشاملة والاختبار التجريبي</h2>\n'
# نجمع كل قطع القراءة مرة أخرى
book += '<h3>📖 جميع قطع القراءة (مراجعة)</h3>\n'
for i, (day, title, rfile, *_) in enumerate(DAYS, 1):
    book += f'<h4>القطعة {i}: {title}</h4>\n'
    book += reading_section(rfile)
# الاختبار التجريبي (exam.json)
exam_path = "exam.json"
if os.path.exists(exam_path):
    exam = load_json(exam_path)
    book += '<h3>📝 الاختبار التجريبي النهائي</h3>\n'
    if isinstance(exam, list):
        for q in exam:
            book += f'<li>{esc(q.get("q",""))}<br>'
            for j, opt in enumerate(q.get("options", [])):
                book += f'{"✅" if j == q.get("answer", -1) else "○"} {esc(opt)}<br>'
            book += '</li>'

# ---------- التجميعات ----------
book += '<div class="page-break"></div>\n'
book += '<h2 id="compilations">📋 التجميعات التدريبية (1-6)</h2>\n'
for i in range(1, 7):
    cpath = f"content/exams/compilation-{i}.json"
    data = load_json(cpath)
    if data:
        book += f'<h3>تجميع {i}</h3>\n'
        if isinstance(data, list):
            book += '<ol>\n'
            for q in data:
                book += f'<li>{esc(q.get("q",""))}<br>\n'
                for j, opt in enumerate(q.get("options", [])):
                    book += f'{"✅" if j == q.get("answer", -1) else "○"} {esc(opt)}<br>\n'
                book += '</li>\n'
            book += '</ol>\n'

# ---------- مسرد الكلمات ----------
book += '<div class="page-break"></div>\n'
book += '<h2 id="glossary">📖 مسرد الكلمات (Glossary)</h2>\n'
book += '<table><tr><th>#</th><th>الإنجليزية</th><th>العربية</th></tr>\n'
seen = set()
for idx, w in enumerate(all_glossary_words):
    if w["english"] not in seen:
        seen.add(w["english"])
        book += f'<tr><td>{idx+1}</td><td><strong>{esc(w["english"])}</strong></td><td>{esc(w["arabic"])}</td></tr>\n'
book += '</table>\n'

# ---------- ملاحق (مفاتيح الإجابات) ----------
book += '<div class="page-break"></div>\n'
book += '<h2 id="appendix">📎 الملاحق – مفاتيح الإجابات</h2>\n'
book += '<h3>اختبارات القواعد</h3>\n'
for i, (day, title, _, _, gtfile) in enumerate(DAYS, 1):
    data = load_json(gtfile)
    if data:
        book += f'<h4>اليوم {i}</h4>\n<div class="answer-key">\n'
        for idx, q in enumerate(data):
            opt = q.get("options", [])
            ans = q.get("answer", -1)
            correct = opt[ans] if 0 <= ans < len(opt) else "—"
            book += f'<p><strong>{idx+1}.</strong> {esc(q.get("q",""))} → <strong>{esc(correct)}</strong></p>\n'
        book += '</div>\n'

book += '<h3>التجميعات</h3>\n'
for i in range(1, 7):
    data = load_json(f"content/exams/compilation-{i}.json")
    if data:
        book += f'<h4>تجميع {i}</h4>\n<div class="answer-key">\n'
        for idx, q in enumerate(data):
            opt = q.get("options", [])
            ans = q.get("answer", -1)
            correct = opt[ans] if 0 <= ans < len(opt) else "—"
            book += f'<p><strong>{idx+1}.</strong> {esc(q.get("q",""))} → <strong>{esc(correct)}</strong></p>\n'
        book += '</div>\n'

# ---------- المصادر ----------
book += '<div class="page-break"></div>\n'
book += '<h2 id="references">📚 المصادر والمراجع</h2>\n'
book += '''<p>استند هذا الكتاب إلى مجموعة من أمهات الكتب والمراجع العالمية في قواعد اللغة الإنجليزية وتعليمها، والتي تُعدّ من أكثر المصادر البشرية اعتباراً وانتشاراً في العالم:</p>

<p><strong>1. English Grammar in Use</strong> – Raymond Murphy (Cambridge University Press)</p>
<p><strong>2. Practical English Usage</strong> – Michael Swan (Oxford University Press)</p>
<p><strong>3. Oxford English Grammar Course</strong> – Swan & Walter (Oxford)</p>
<p><strong>4. Longman English Grammar</strong> – L.G. Alexander (Pearson)</p>
<p><strong>5. Understanding and Using English Grammar</strong> – Betty S. Azar (Pearson)</p>
<p><strong>6. Advanced Grammar in Use</strong> – Martin Hewings (Cambridge)</p>
<p><strong>7. The Official Cambridge Guide to IELTS</strong> – Cullen et al. (Cambridge)</p>
<p><strong>8. Vocabulary in Use</strong> – Stuart Redman (Cambridge)</p>'''

# ---------- تذييل ----------
book += '<div class="footer-note">\n'
book += '<h3>🏆 معهد الريادة للتدريب</h3>\n'
book += '<p>إعداد المدرب: <strong>أنس عبد الرحمن</strong></p>\n'
book += '<p>للتسجيل: <strong>0546088130</strong> | <strong>0548775199</strong></p>\n'
book += '<p style="margin-top:1rem;">الموقع: <strong>english-zone.github.io/itc-apne-prep</strong></p>\n'
book += '<p>تم بحمد الله – نتمنى لكم التوفيق والنجاح في اختبار APNE</p>\n'
book += '</div>\n'

book += '\n</body>\n</html>'

with open('book.html', 'w', encoding='utf-8') as f:
    f.write(book)

print("✅ تم إنشاء book.html بالشكل الصحيح")
