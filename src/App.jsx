import { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import { grades } from './data/grades';
import { topics } from './data/topics';
import { problems } from './data/problems';
import { knowledge } from './data/knowledge';
import { stories } from './data/stories';
import './index.css';

// ─── Utilities: Audio & Speech ────────────────────────────────────

const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
let isGlobalMuted = false;

function playSound(type) {
  if (isGlobalMuted) return;
  if (audioCtx.state === 'suspended') audioCtx.resume();
  const osc = audioCtx.createOscillator();
  const gainNode = audioCtx.createGain();
  osc.connect(gainNode);
  gainNode.connect(audioCtx.destination);
  
  if (type === 'correct') {
    // Tiếng chuông vui vẻ ting ting
    osc.type = 'sine';
    osc.frequency.setValueAtTime(523.25, audioCtx.currentTime); // C5
    osc.frequency.setValueAtTime(659.25, audioCtx.currentTime + 0.1); // E5
    osc.frequency.setValueAtTime(783.99, audioCtx.currentTime + 0.2); // G5
    gainNode.gain.setValueAtTime(0, audioCtx.currentTime);
    gainNode.gain.linearRampToValueAtTime(0.5, audioCtx.currentTime + 0.05);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.4);
    osc.start(audioCtx.currentTime);
    osc.stop(audioCtx.currentTime + 0.5);
  } else if (type === 'wrong') {
    // Tiếng boop buồn bã
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(146.83, audioCtx.currentTime); // D3
    osc.frequency.setValueAtTime(138.59, audioCtx.currentTime + 0.15); // C#3
    gainNode.gain.setValueAtTime(0, audioCtx.currentTime);
    gainNode.gain.linearRampToValueAtTime(0.5, audioCtx.currentTime + 0.05);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
    osc.start(audioCtx.currentTime);
    osc.stop(audioCtx.currentTime + 0.6);
  }
}

let currentAudio = null;

function speakText(text) {
  if (isGlobalMuted) return;

  // Dừng âm thanh cũ nêú đang phát
  if (currentAudio) {
    currentAudio.pause();
    currentAudio.currentTime = 0;
  }
  
  // Chia nhỏ text nếu quá dài, hoặc đọc nguyên cả câu
  const chunks = text.match(/[^.!?]+[.!?]+/g) || [text];
  let currentChunkIdx = 0;

  function playNextChunk() {
    if (isGlobalMuted || currentChunkIdx >= chunks.length) return;
    const chunkText = chunks[currentChunkIdx].trim();
    if (!chunkText) {
      currentChunkIdx++;
      playNextChunk();
      return;
    }
    
    // Sử dụng API Google Translate với client=tw-ob để tránh bị chặn 403 Forbidden
    const url = `https://translate.googleapis.com/translate_tts?client=tw-ob&ie=UTF-8&tl=vi&q=${encodeURIComponent(chunkText)}`;
    currentAudio = new Audio(url);
    
    currentAudio.onended = () => {
      currentChunkIdx++;
      playNextChunk();
    };
    
    currentAudio.onerror = () => {
      console.warn("Lỗi tải giọng đọc Google.");
      currentChunkIdx++;
      playNextChunk();
    };
    
    currentAudio.play().catch(() => {
      console.warn("Lỗi Play Audio.");
      currentChunkIdx++;
      playNextChunk();
    });
  }
  
  playNextChunk();
}

function stopSpeak() {
  if (currentAudio) {
    currentAudio.pause();
    currentAudio.currentTime = 0;
  }
}

// ─── Sub-components ───────────────────────────────────────────────

function Header({ stars, isMuted, onToggleMute, onHome, onViewStories }) {
  return (
    <header className="app-header">
      <div className="header-logo" onClick={onHome}>
        <span className="logo-icon">🧮</span>
        <span className="logo-text">Toán Vui</span>
      </div>
      <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
        <button className="btn-story" style={{ background: isMuted ? '#95a5a6' : '#2ecc71' }} onClick={onToggleMute}>
          {isMuted ? '🔇 Tắt Tiếng' : '🔊 Bật Tiếng'}
        </button>  
        <button className="btn-story" onClick={onViewStories}>📚 Chuyện Vui</button>
        <div className="header-stars">
          <span>⭐</span>
          <span>{stars} sao</span>
        </div>
      </div>
    </header>
  );
}

function KnowledgeModal({ keyId, onClose }) {
  const item = knowledge[keyId];
  if (!item) return null;
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>✕</button>
        <span className="modal-emoji">{item.emoji}</span>
        <div className="modal-term">{item.term}</div>
        <p className="modal-definition">{item.definition}</p>
        <div className="modal-example">💡 Ví dụ: {item.example}</div>
      </div>
    </div>
  );
}

function StepText({ text, highlight, onKeyword }) {
  if (!highlight) return <span className="step-text">{text}</span>;
  const parts = text.split(new RegExp(`(${highlight.replace(/[-\/]/g, '\\$&')})`, 'gi'));
  return (
    <span className="step-text">
      {text}{' '}
      {knowledge[highlight] && (
        <button className="keyword-link" onClick={() => onKeyword(highlight)}>
          📖 {knowledge[highlight].term}
        </button>
      )}
    </span>
  );
}

// ─── Pages ────────────────────────────────────────────────────────

function GradeSelector({ onSelect }) {
  return (
    <div>
      <div className="page-title">
        <h2>🎉 Chọn Lớp Của Bạn!</h2>
        <p>Hãy chọn lớp học phù hợp với trình độ của bạn</p>
      </div>
      <div className="grade-grid">
        {grades.map(g => (
          <div
            key={g.id}
            className="grade-card"
            style={{ background: g.bgGradient }}
            onClick={() => onSelect(g)}
          >
            <span className="grade-emoji">{g.emoji}</span>
            <span className="grade-name">{g.name}</span>
            <span className="grade-desc">{g.description}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function TopicList({ grade, onSelect, onBack, onHome }) {
  const topicList = topics[grade.id] || [];
  return (
    <div>
      <div className="breadcrumb">
        <div className="breadcrumb-item" onClick={onHome}>🏠 Trang chủ</div>
        <span className="breadcrumb-sep">›</span>
        <div className="breadcrumb-item active" style={{ background: grade.color, borderColor: grade.color, color: 'white' }}>
          {grade.emoji} {grade.name}
        </div>
      </div>
      <div className="page-title">
        <h2>{grade.emoji} Chủ Đề {grade.name}</h2>
        <p>Chọn một chủ đề bạn muốn luyện tập hôm nay!</p>
      </div>
      <div className="topic-grid">
        {topicList.map(t => (
          <div
            key={t.id}
            className="topic-card"
            style={{ '--topic-color': t.color }}
            onClick={() => onSelect(t)}
          >
            <span className="topic-emoji">{t.emoji}</span>
            <div className="topic-name">{t.name}</div>
            <div className="topic-count">{t.problemIds.length} bài tập</div>
            <div className="topic-dot" />
          </div>
        ))}
      </div>
    </div>
  );
}

function QuizPage({ grade, topic, onBack, onHome, onAddStars }) {
  const problemList = topic.problemIds.map(id => problems[id]).filter(Boolean);
  const [idx, setIdx] = useState(0);
  const [selected, setSelected] = useState(null);
  const [correct, setCorrect] = useState(0);
  const [done, setDone] = useState(false);
  const [modalKey, setModalKey] = useState(null);

  const current = problemList[idx];
  const progress = ((idx) / problemList.length) * 100;

  function handleChoice(i) {
    if (selected !== null) return;
    setSelected(i);
    // Dừng âm thanh đọc dở
    stopSpeak();
    
    if (i === current.answer) {
      playSound('correct');
      setCorrect(c => c + 1);
      onAddStars(1);
      confetti({
        particleCount: 120,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#FF6B6B', '#FF9F43', '#FECA57', '#54A0FF', '#00B894', '#5F27CD'],
      });
    } else {
      playSound('wrong');
    }
  }

  function handleNext() {
    if (idx + 1 >= problemList.length) {
      setDone(true);
    } else {
      setIdx(i => i + 1);
      setSelected(null);
    }
  }

  if (done) {
    const score = correct;
    const total = problemList.length;
    const pct = Math.round((score / total) * 100);
    const stars = pct >= 80 ? '⭐⭐⭐' : pct >= 50 ? '⭐⭐' : '⭐';
    const emoji = pct === 100 ? '🏆' : pct >= 80 ? '🎉' : pct >= 50 ? '👍' : '💪';
    const msg = pct === 100 ? 'Xuất Sắc!' : pct >= 80 ? 'Tuyệt Vời!' : pct >= 50 ? 'Khá Tốt!' : 'Cố Lên!';
    return (
      <div>
        <div className="breadcrumb">
          <div className="breadcrumb-item" onClick={onHome}>🏠 Trang chủ</div>
          <span className="breadcrumb-sep">›</span>
          <div className="breadcrumb-item" onClick={onBack}>{grade.emoji} {grade.name}</div>
          <span className="breadcrumb-sep">›</span>
          <div className="breadcrumb-item active">{topic.emoji} {topic.name}</div>
        </div>
        <div className="result-card">
          <span className="result-emoji">{emoji}</span>
          <div className="result-title">{msg}</div>
          <span className="result-stars">{stars}</span>
          <div className="result-score">Bạn trả lời đúng {score}/{total} câu ({pct}%)</div>
          <div className="result-actions">
            <button className="btn-secondary" onClick={() => { setIdx(0); setSelected(null); setCorrect(0); setDone(false); playSound('correct'); }}>
              🔄 Làm Lại
            </button>
            <button className="next-btn" style={{ flex: 1 }} onClick={onBack}>
              📚 Chủ Đề Khác
            </button>
          </div>
        </div>
      </div>
    );
  }

  function handleReadQuestion() {
    if (currentAudio && !currentAudio.paused) {
      stopSpeak();
      return;
    }
    const textToRead = current.question + ". Các đáp án là: " + current.choices.join(', ');
    speakText(textToRead);
  }

  return (
    <div>
      {modalKey && <KnowledgeModal keyId={modalKey} onClose={() => setModalKey(null)} />}

      <div className="breadcrumb">
        <div className="breadcrumb-item" onClick={onHome}>🏠 Trang chủ</div>
        <span className="breadcrumb-sep">›</span>
        <div className="breadcrumb-item" onClick={onBack}>{grade.emoji} {grade.name}</div>
        <span className="breadcrumb-sep">›</span>
        <div className="breadcrumb-item active">{topic.emoji} {topic.name}</div>
      </div>

      <div className="quiz-wrapper">
        <div>
          <div className="quiz-progress">
            <span className="progress-text">Câu {idx + 1}/{problemList.length}</span>
            <div className="progress-bar-bg">
              <div className="progress-bar-fill" style={{ width: `${progress}%` }} />
            </div>
            <span className="progress-text">✅ {correct}</span>
          </div>
        </div>

        <div className="question-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <span className="question-number">Câu {idx + 1}</span>
            <button className="btn-read-aloud" onClick={handleReadQuestion} title="Đọc câu hỏi">
              🔊 Nghe Đọc
            </button>
          </div>
          <p className="question-text">{current.question}</p>
          {current.illustration && (
            <div className="problem-illustration">{current.illustration}</div>
          )}
        </div>

        <div className="choices-grid">
          {current.choices.map((c, i) => {
            let cls = 'choice-btn';
            if (selected !== null) {
              if (i === current.answer) cls += ' correct';
              else if (i === selected && i !== current.answer) cls += ' wrong';
            }
            return (
              <button key={i} className={cls} onClick={() => handleChoice(i)} disabled={selected !== null}>
                {c}
              </button>
            );
          })}
        </div>

        {selected !== null && (
          <div className="solution-panel">
            <div className="solution-title">
              {selected === current.answer ? '🌟 Chính xác! Xem giải thích:' : '💡 Chưa đúng! Đây là cách giải:'}
            </div>
            <ul className="step-list">
              {current.steps.map((s, i) => (
                <li key={i} className="step-item">
                  <span className="step-num">{i + 1}</span>
                  <StepText text={s.text} highlight={s.highlight} onKeyword={setModalKey} />
                </li>
              ))}
            </ul>
          </div>
        )}

        {selected !== null && (
          <button className="next-btn" onClick={handleNext}>
            {idx + 1 >= problemList.length ? '🏁 Xem Kết Quả' : '➡️ Câu Tiếp Theo'}
          </button>
        )}
      </div>
    </div>
  );
}

// ─── Stories Page ──────────────────────────────────────────────────

function StoriesPage({ onHome }) {
  return (
    <div>
      <div className="breadcrumb">
        <div className="breadcrumb-item" onClick={onHome}>🏠 Trang chủ</div>
        <span className="breadcrumb-sep">›</span>
        <div className="breadcrumb-item active">📚 Chuyện Vui Toán Học</div>
      </div>
      <div className="page-title">
        <h2>📚 Những Câu Chuyện Toán Học</h2>
        <p>Khám phá thế giới toán học huyền diệu và các nhà toán học vĩ đại!</p>
      </div>
      <div className="story-grid">
        {stories.map(s => (
          <div key={s.id} className="story-card" style={{ '--story-color': s.color }}>
            <div className="story-title">
              <span>{s.emoji}</span> {s.title}
            </div>
            {s.image && (
              <div style={{ textAlign: 'center', margin: '24px 0' }}>
                <img 
                  src={s.image} 
                  alt={s.title} 
                  style={{ width: '100%', maxWidth: '500px', borderRadius: '16px', border: `4px solid ${s.color}66`, boxShadow: '0 8px 24px rgba(0,0,0,0.1)' }} 
                />
              </div>
            )}
            <div className="story-content">{s.content}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── App Root ─────────────────────────────────────────────────────

export default function App() {
  const [view, setView] = useState('home');
  const [grade, setGrade] = useState(null);
  const [topic, setTopic] = useState(null);
  const [stars, setStars] = useState(() => {
    try { return parseInt(localStorage.getItem('toanvui-stars') || '0'); } catch { return 0; }
  });
  const [isMuted, setIsMuted] = useState(() => {
    try { return localStorage.getItem('toanvui-muted') === 'true'; } catch { return false; }
  });

  useEffect(() => {
    try { localStorage.setItem('toanvui-stars', String(stars)); } catch {}
  }, [stars]);

  useEffect(() => {
    isGlobalMuted = isMuted;
    try { localStorage.setItem('toanvui-muted', String(isMuted)); } catch {}
    if (isMuted) stopSpeak();
  }, [isMuted]);

  function addStars(n) { setStars(s => s + n); }
  function toggleMute() { setIsMuted(m => !m); }

  return (
    <>
      <Header 
        stars={stars} 
        isMuted={isMuted} 
        onToggleMute={toggleMute} 
        onHome={() => { stopSpeak(); setView('home'); }} 
        onViewStories={() => { stopSpeak(); setView('stories'); }} 
      />
      <main className="main-content">
        {view === 'home' && (
          <GradeSelector onSelect={g => { setGrade(g); setView('topics'); }} />
        )}
        {view === 'stories' && (
          <StoriesPage onHome={() => setView('home')} />
        )}
        {view === 'topics' && grade && (
          <TopicList
            grade={grade}
            onSelect={t => { setTopic(t); setView('quiz'); }}
            onBack={() => setView('home')}
            onHome={() => setView('home')}
          />
        )}
        {view === 'quiz' && grade && topic && (
          <QuizPage
            grade={grade}
            topic={topic}
            onBack={() => setView('topics')}
            onHome={() => setView('home')}
            onAddStars={addStars}
          />
        )}
      </main>
    </>
  );
}
