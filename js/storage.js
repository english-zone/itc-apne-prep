const Storage = {
  get(key, fallback = null) {
    try {
      const raw = localStorage.getItem('itc_' + key);
      return raw ? JSON.parse(raw) : fallback;
    } catch { return fallback; }
  },
  set(key, value) {
    try { localStorage.setItem('itc_' + key, JSON.stringify(value)); } catch {}
  },
  update(key, updater) {
    const current = this.get(key, {});
    const updated = typeof updater === 'function' ? updater(current) : { ...current, ...updater };
    this.set(key, updated);
    return updated;
  },
  // Specific helpers
  getProgress() { return this.get('progress', { streak: 0, lastStudy: null, readingCount: 0 }) },
  updateProgress(data) { return this.update('progress', p => ({ ...p, ...data })) },
  getExamScores() { return this.get('examScores', []) },
  addExamScore(score) { this.set('examScores', [...this.getExamScores(), { ...score, date: new Date().toISOString() }]) },
  getVocabulary() { return this.get('vocabulary', {}) },
  updateWord(word, state) { this.update('vocabulary', v => { v[word] = state; return v; }) },
  getMistakes() { return this.get('mistakes', []) },
  addMistake(mistake) {
    const mistakes = this.getMistakes();
    mistakes.push({ ...mistake, id: Date.now(), date: new Date().toISOString(), mastered: false });
    this.set('mistakes', mistakes);
  },
  markMastered(id) {
    const mistakes = this.getMistakes().map(m => m.id === id ? { ...m, mastered: true } : m);
    this.set('mistakes', mistakes);
  },
  getReadingHistory() { return this.get('readingHistory', []) },
  addReadingHistory(entry) { this.set('readingHistory', [...this.getReadingHistory(), { ...entry, date: new Date().toISOString() }]) },
  getTheme() { return this.get('theme', 'light') },
  setTheme(t) { this.set('theme', t); document.documentElement.setAttribute('data-theme', t); },
};
