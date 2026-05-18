import re, sys

NEW_CSS = '''
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
  @page { margin: 1.5cm; @bottom-center { content: counter(page); font-family: 'Cairo'; } }
  .section-title { page-break-before: always; }
  .cover { page-break-after: always; }
  .vocab-flex, .grammar-flex { grid-template-columns: 1fr 1fr !important; }
  .lesson-col { border-right: 1px solid #ccc; }
}
'''

def remove_bdo_tags(html):
    return re.sub(r'<bdo dir="ltr">(.*?)</bdo>', r'\1', html, flags=re.DOTALL)

def replace_style(html, new_css):
    pattern = re.compile(r'<style>.*?</style>', re.DOTALL)
    new_block = f'<style>{new_css}</style>'
    result, n = pattern.subn(new_block, html, count=1)
    if n == 0:
        result = html.replace('</head>', f'{new_block}\n</head>', 1)
    return result

def clean_nested_documents(html):
    def clean_section(m):
        s = m.group(0)
        s = re.sub(
            r'<!DOCTYPE html>\s*<html[^>]*>\s*<head>.*?</head>\s*<body[^>]*>',
            '', s, flags=re.DOTALL
        )
        s = re.sub(r'</body>\s*</html>', '', s, flags=re.DOTALL)
        s = re.sub(r'<style>.*?</style>', '', s, flags=re.DOTALL)
        return s
    return re.sub(
        r'<section class="grammar-lesson">.*?</section>',
        clean_section,
        html,
        flags=re.DOTALL
    )

def wrap_tables_in_scrollable_div(html):
    def wrap_if_needed(m):
        inner = m.group(0)
        if 'word-table-wrap' in inner:
            return inner
        inner = re.sub(
            r'(<table class="word-table">.*?</table>)',
            r'<div class="word-table-wrap">\1</div>',
            inner,
            flags=re.DOTALL,
            count=1
        )
        return inner
    return re.sub(
        r'<div class="vocab-col">.*?</div>(?=\s*<div class="vocab-col">|\s*</div>)',
        wrap_if_needed,
        html,
        flags=re.DOTALL
    )

# Main
with open('textbook.html', encoding='utf-8') as f:
    html = f.read()

print(f'[1/5] Read {len(html):,} chars')

n_before = html.count('<bdo dir="ltr">')
html = remove_bdo_tags(html)
print(f'[2/5] Removed {n_before:,} <bdo> tags')

html = replace_style(html, NEW_CSS)
print('[3/5] CSS replaced')

html = clean_nested_documents(html)
print('[4/5] Nested HTML cleaned')

html = wrap_tables_in_scrollable_div(html)
print('[5/5] Vocab tables wrapped')

with open('textbook.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'✅ Fixed textbook.html ({len(html):,} chars)')
