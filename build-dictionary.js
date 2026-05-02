const fs = require('fs');
const path = require('path');

const vocabDir = path.join(__dirname, 'content', 'vocabulary');
const outputPath = path.join(__dirname, 'content', 'dictionary', 'dictionary-full.json');
const dictionary = {};

const files = fs.readdirSync(vocabDir).filter(f => f.endsWith('.json'));
for (const file of files) {
  const data = JSON.parse(fs.readFileSync(path.join(vocabDir, file), 'utf-8'));
  if (data.words) {
    for (const w of data.words) {
      const key = (w.english || w.word || '').toLowerCase().trim();
      if (!key) continue;
      dictionary[key] = {
        meaning_en: w.meaning_en || '',
        meaning_ar: w.arabic || w.meaning_ar || '',
        synonyms: w.synonyms || [],
        antonyms: w.antonyms || [],
        collocations: w.collocations || [],
        example: w.example || ''
      };
    }
  }
}

fs.writeFileSync(outputPath, JSON.stringify(dictionary, null, 2), 'utf-8');
console.log('✅ قاموس كامل بـ ' + Object.keys(dictionary).length + ' كلمة');
