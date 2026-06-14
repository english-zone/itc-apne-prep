import json, os, html as html_mod

def load_json(path):
    if not os.path.exists(path): return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def escape(txt):
    return html_mod.escape(str(txt)) if txt else ""

def get_correct(q):
    opts = q.get("options", [])
    ans = q.get("answer", -1)
    return opts[ans] if 0 <= ans < len(opts) else "—"

def build_reading(day_num):
    r = load_json(f"content/day-{day_num:02d}/reading.json")
    if not r: return ""
    passages = r.get("passages", [])
    if not passages and isinstance(r, list):
        passages = r
    sec = f'<div class="section"><h2>📖 قراءة اليوم {day_num}</h2>'
    for pi, p in enumerate(passages):
        title = escape(p.get("title", f"Passage {pi+1}"))
        questions = p.get("questions", [])
        sec += f'<h3>{title}</h3><ol>'
        for q in questions:
            q_text = escape(q.get("q", ""))
            correct = get_correct(q)
            sec += f'<li>{q_text} <strong style="color:#0071e3;">→ {escape(correct)}</strong></li>'
        sec += '</ol>'
    sec += '</div>'
    return sec

def build_vocab(day_num):
    v = load_json(f"content/day-{day_num:02d}/vocabulary.json")
    if not v: return ""
    words = v.get("words", [])
    sec = f'<div class="section"><h2>📝 مفردات اليوم {day_num}</h2>'
    # عرض الكلمات
    if words:
        sec += '<table style="width:100%;border-collapse:collapse;margin-bottom:1rem;"><tr><th>#</th><th>English</th><th>العربية</th></tr>'
        for i, w in enumerate(words):
            eng = escape(w.get("english",""))
            ara = escape(w.get("arabic",""))
            sec += f'<tr><td>{i+1}</td><td style="direction:ltr">{eng}</td><td>{ara}</td></tr>'
        sec += '</table>'
    # أسئلة المفردات
    all_q = [w.get("question") for w in words if w.get("question")]
    if all_q:
        sec += '<h3>أسئلة المفردات:</h3><ol>'
        for q in all_q:
            q_text = escape(q.get("q", ""))
            correct = get_correct(q)
            sec += f'<li>{q_text} <strong style="color:#0071e3;">→ {escape(correct)}</strong></li>'
        sec += '</ol>'
    sec += '</div>'
    return sec

def build_dictation(day_num):
    d = load_json(f"content/day-{day_num:02d}/dictation.json")
    if not d: return ""
    words = d.get("words", []) if isinstance(d, dict) else d
    if not words: return ""
    sec = f'<div class="section"><h2>✍️ إملاء اليوم {day_num}</h2><ol>'
    for w in words:
        if isinstance(w, dict):
            correct = escape(w.get("correct", ""))
        else:
            correct = escape(w)
        sec += f'<li><strong style="color:#0071e3;">{correct}</strong></li>'
    sec += '</ol></div>'
    return sec

def build_grammar_test(day_num):
    g = load_json(f"content/day-{day_num:02d}/grammar-test.json")
    if not g: return ""
    questions = g.get("questions", []) if isinstance(g, dict) else g
    if not questions: return ""
    sec = f'<div class="section"><h2>📝 اختبار قواعد اليوم {day_num}</h2><ol>'
    for q in questions:
        q_text = escape(q.get("q", ""))
        correct = get_correct(q)
        sec += f'<li>{q_text} <strong style="color:#0071e3;">→ {escape(correct)}</strong></li>'
    sec += '</ol></div>'
    return sec

# بناء الصفحة
html = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Teacher's Guide – APNE-ITC</title>
<style>
  body { font-family: 'Cairo', sans-serif; background: #f5f5f7; padding: 2rem; direction: rtl; }
  .container { max-width: 900px; margin: auto; background: white; border-radius: 20px; padding: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
  h1 { color: #0b2b4f; text-align: center; border-bottom: 3px solid #0071e3; padding-bottom: 1rem; }
  .section { margin: 2rem 0; page-break-inside: avoid; }
  .section h2 { background: #0071e3; color: white; padding: 0.5rem 1rem; border-radius: 8px; }
  .section h3 { color: #0b2b4f; margin: 1rem 0 0.5rem; }
  table { border-collapse: collapse; width: 100%; }
  th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: right; }
  th { background: #0059b3; color: white; }
  ol li { margin: 0.5rem 0; line-height: 1.8; }
  @media print {
    body { background: white; padding: 0; }
    .container { box-shadow: none; border-radius: 0; max-width: 100%; }
    .print-btn { display: none; }
    @page { margin: 1cm; @bottom-center { content: counter(page); font-family: 'Cairo'; } }
  }
  .print-btn { display: block; margin: 1rem auto; background: #0071e3; color: white; border: none; padding: 10px 30px; font-size: 1.1rem; border-radius: 50px; cursor: pointer; }
  #content { display: none; }
  #login { text-align: center; margin: 3rem 0; }
  #login input { padding: 10px; font-size: 1rem; border: 1px solid #ccc; border-radius: 8px; width: 200px; }
  #login button { padding: 10px 20px; background: #0071e3; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 1rem; }
</style>
</head>
<body>
<div class="container">
<h1>🔑 دليل المعلم – APNE-ITC</h1>
<p style="text-align:center; color:#555;">جميع الإجابات للقراءة، المفردات، الإملاء، واختبارات القواعد</p>

<div id="login">
  <p>أدخل كلمة المرور:</p>
  <input type="password" id="pass" placeholder="كلمة المرور">
  <button onclick="checkPass()">دخول</button>
</div>

<div id="content">
'''

# توليد الأيام من 1 إلى 7
for d in range(1, 8):
    html += f'<div class="day-block" style="page-break-before: always;"><h1 style="color:#0b2b4f;">🗓️ اليوم {d}</h1>'
    html += build_reading(d)
    html += build_vocab(d)
    html += build_dictation(d)
    html += build_grammar_test(d)
    html += '</div>'

html += '''
</div>
<button class="print-btn" onclick="window.print()">🖨️ طباعة الدليل</button>
</div>
<script>
function checkPass() {
  var pass = document.getElementById('pass').value;
  if (pass === 'reyadah2024' || pass === 'teacher123') {
    document.getElementById('login').style.display = 'none';
    document.getElementById('content').style.display = 'block';
  } else {
    alert('كلمة المرور غير صحيحة');
  }
}
</script>
</body>
</html>
'''

with open('teacher.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ teacher.html تم إنشاؤه بنجاح")
