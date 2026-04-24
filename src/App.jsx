import { useState, useEffect, useRef } from 'react';
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

function shuffle(array) {
  const result = [...array];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

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



function speakText(text) {
  if (isGlobalMuted) return;
  stopSpeak();
  
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'vi-VN';
  utterance.rate = 1.0;
  
  const voices = window.speechSynthesis.getVoices();
  const viVoice = voices.find(v => v.lang.includes('vi'));
  if (viVoice) utterance.voice = viVoice;

  window.speechSynthesis.speak(utterance);
}

function stopSpeak() {
  if (window.speechSynthesis) {
    window.speechSynthesis.cancel();
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

function StickTool() {
  const [count, setCount] = useState(0);
  const bundles = Math.floor(count / 10);
  const singles = count % 10;

  return (
    <div className="tool-panel">
      <div style={{ fontWeight: 'bold', marginBottom: '10px', display: 'flex', justifyContent: 'space-between' }}>
        <span>🥢 Công cụ Que tính (Lớp 1)</span>
        <span style={{ color: 'var(--clr-accent)' }}>Tổng cộng: {count}</span>
      </div>
      <div className="stick-workspace">
        <div className="stick-bundle-area">
          {[...Array(bundles)].map((_, i) => (
            <div key={i} className="stick-bundle"><div className="bundle-stick-art" /></div>
          ))}
        </div>
        <div className="stick-single-area">
          {[...Array(singles)].map((_, i) => (
            <div key={i} className="stick-single" />
          ))}
        </div>
      </div>
      <div className="stick-controls">
        <button className="btn-tool" onClick={() => setCount(Math.min(100, count + 1))}>+1 Que</button>
        <button className="btn-tool" onClick={() => setCount(Math.min(100, count + 10))}>+10 Que</button>
        <button className="btn-tool" style={{ color: '#FF6B6B' }} onClick={() => setCount(Math.max(0, count - 1))}>-1 Que</button>
        <button className="btn-tool" style={{ background: '#eee' }} onClick={() => setCount(0)}>Xóa hết</button>
      </div>
      <p style={{ fontSize: '0.8rem', color: '#666', marginTop: '10px' }}>* Mỗi bó to tương ứng với 10 que tách rời.</p>
    </div>
  );
}

function DrawingBoard() {
  const canvasRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [color, setColor] = useState('#ffffff');
  const [tool, setTool] = useState('pen'); // 'pen', 'line', 'rect', 'triangle'
  const [startPos, setStartPos] = useState({ x: 0, y: 0 });
  const [lastState, setLastState] = useState(null);
  const [useSnap, setUseSnap] = useState(true);

  const gridSize = 40; // 40px = 1 đơn vị độ dài

  const getCoords = (e, shouldSnap = false) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    
    let clientX, clientY;
    if (e.touches && e.touches.length > 0) {
      clientX = e.touches[0].clientX;
      clientY = e.touches[0].clientY;
    } else {
      clientX = e.clientX;
      clientY = e.clientY;
    }
    
    let x = (clientX - rect.left) * scaleX;
    let y = (clientY - rect.top) * scaleY;

    if (shouldSnap) {
      x = Math.round(x / gridSize) * gridSize;
      y = Math.round(y / gridSize) * gridSize;
    }

    return { x, y };
  };

  const startDrawing = (e) => {
    const { x, y } = getCoords(e, useSnap && tool !== 'pen');
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    setLastState(ctx.getImageData(0, 0, canvas.width, canvas.height));
    setStartPos({ x, y });
    
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.strokeStyle = color;
    ctx.lineWidth = 4;
    ctx.lineCap = 'round';
    setIsDrawing(true);
  };

  const drawShape = (ctx, start, end, type) => {
    ctx.beginPath();
    ctx.strokeStyle = color;
    if (type === 'line') {
      ctx.moveTo(start.x, start.y);
      ctx.lineTo(end.x, end.y);
    } else if (type === 'rect') {
      ctx.rect(start.x, start.y, end.x - start.x, end.y - start.y);
    } else if (type === 'triangle') {
      ctx.moveTo(start.x + (end.x - start.x) / 2, start.y);
      ctx.lineTo(start.x, end.y);
      ctx.lineTo(end.x, end.y);
      ctx.closePath();
    }
    ctx.stroke();
  };

  const draw = (e) => {
    if (!isDrawing) return;
    const { x, y } = getCoords(e, useSnap && tool !== 'pen');
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    if (tool === 'pen') {
      ctx.lineTo(x, y);
      ctx.stroke();
    } else {
      if (lastState) ctx.putImageData(lastState, 0, 0);
      drawShape(ctx, startPos, { x, y }, tool);
    }
  };

  return (
    <div className="tool-panel">
      <div className="drawing-container">
        <div style={{ fontWeight: 'bold', marginBottom: '8px', display: 'flex', justifyContent: 'space-between' }}>
          <span>🎨 Bảng vẽ Hình học / Nháp</span>
          <label style={{ fontSize: '0.8rem', cursor: 'pointer', color: useSnap ? 'var(--clr-accent)' : '#666' }}>
            <input type="checkbox" checked={useSnap} onChange={e => setUseSnap(e.target.checked)} /> Bắt điểm (Snap)
          </label>
        </div>
        
        <div className="drawing-layout">
          <div className="ruler-corner" />
          <div className="ruler-x">
            {[...Array(21)].map((_, i) => (
              <div key={i} className="ruler-mark" style={{ left: `${i * gridSize}px` }}>
                {i}
              </div>
            ))}
          </div>
          <div className="ruler-y">
            {[...Array(11)].map((_, i) => (
              <div key={i} className="ruler-mark" style={{ top: `${i * gridSize}px` }}>
                {i}
              </div>
            ))}
          </div>
          <div className="canvas-wrapper" style={{ background: '#2c3e50' }}>
            <div className="canvas-grid" style={{ backgroundSize: `${gridSize}px ${gridSize}px`, backgroundImage: 'linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)' }} />
            <canvas
              ref={canvasRef}
              width={800}
              height={400}
              style={{ display: 'block', width: '100%', cursor: 'crosshair' }}
              onMouseDown={startDrawing}
              onMouseMove={draw}
              onMouseUp={() => setIsDrawing(false)}
              onMouseLeave={() => setIsDrawing(false)}
              onTouchStart={startDrawing}
              onTouchMove={draw}
              onTouchEnd={() => setIsDrawing(false)}
            />
          </div>
          
          <div className="drawing-tools-bar">
            <div className="tool-group">
              <button className={`btn-tool-mini ${tool === 'pen' ? 'active' : ''}`} onClick={() => setTool('pen')}>✏️ Bút</button>
              <button className={`btn-tool-mini ${tool === 'line' ? 'active' : ''}`} onClick={() => setTool('line')}>📏 Thẳng</button>
              <button className={`btn-tool-mini ${tool === 'rect' ? 'active' : ''}`} onClick={() => setTool('rect')}>🟦 Vuông</button>
              <button className={`btn-tool-mini ${tool === 'triangle' ? 'active' : ''}`} onClick={() => setTool('triangle')}>🔺 Tam Giác</button>
            </div>
            <div className="tool-group">
              {['#ffffff', '#FFD32A', '#FF6B6B', '#54A0FF', '#2ecc71'].map(c => (
                <div 
                  key={c} 
                  className={`color-dot-mini ${color === c ? 'active' : ''}`} 
                  style={{ background: c }} 
                  onClick={() => setColor(c)}
                />
              ))}
            </div>
            <button className="btn-tool-mini" onClick={() => {
              const ctx = canvasRef.current.getContext('2d');
              ctx.clearRect(0, 0, 800, 400);
            }}>🧹 Xóa</button>
          </div>
        </div>
      </div>
    </div>
  );
}

function ClockTool() {
  const [time, setTime] = useState({ h: 10, m: 10 });
  const [isDragging, setIsDragging] = useState(null); // 'h' or 'm'

  const handlePointer = (e) => {
    if (!isDragging) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const clientX = e.clientX || e.touches?.[0].clientX;
    const clientY = e.clientY || e.touches?.[0].clientY;
    
    // atan2 gives angle from X axis. We add 90 to make 12 o'clock be 0 degrees.
    const angle = Math.atan2(clientY - cy, clientX - cx) * 180 / Math.PI + 90;
    const normalized = (angle + 360) % 360;

    if (isDragging === 'm') {
      const minutes = Math.round(normalized / 6) % 60;
      setTime(t => ({ ...t, m: minutes }));
    } else if (isDragging === 'h') {
      // 360 / 12 = 30 degrees per hour
      const hrs = Math.round(normalized / 30) % 12 || 12;
      setTime(t => ({ ...t, h: hrs }));
    }
  };

  return (
    <div className="tool-panel">
      <div style={{ fontWeight: 'bold', marginBottom: '10px' }}>🕒 Công cụ Đồng hồ</div>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '20px' }}>
        <div 
          className={`clock-face ${isDragging ? 'dragging' : ''}`} 
          onMouseMove={handlePointer}
          onTouchMove={handlePointer}
          onMouseUp={() => setIsDragging(null)}
          onMouseLeave={() => setIsDragging(null)}
          onTouchEnd={() => setIsDragging(null)}
        >
          <div className="clock-center" />
          {/* Numbers */}
          {[...Array(12)].map((_, i) => {
            const angle = (i * 30) * (Math.PI / 180);
            const r = 85; 
            const x = Math.sin(angle) * r;
            const y = -Math.cos(angle) * r;
            return (
              <div key={i} className="clock-number" style={{ transform: `translate(-50%, -50%) translate(${x}px, ${y}px)` }}>
                {i === 0 ? 12 : i}
              </div>
            );
          })}
          {/* Hands */}
          <div 
            className="clock-hand hand-hour" 
            style={{ transform: `rotate(${time.h * 30 + time.m * 0.5}deg)` }}
            onMouseDown={(e) => { e.stopPropagation(); setIsDragging('h'); }}
            onTouchStart={(e) => { e.stopPropagation(); setIsDragging('h'); }}
          />
          <div 
            className="clock-hand hand-minute" 
            style={{ transform: `rotate(${time.m * 6}deg)` }}
            onMouseDown={(e) => { e.stopPropagation(); setIsDragging('m'); }}
            onTouchStart={(e) => { e.stopPropagation(); setIsDragging('m'); }}
          />
        </div>
        <div className="digital-time">
          {String(time.h).padStart(2, '0')}:{String(time.m).padStart(2, '0')}
        </div>
        <p style={{ fontSize: '0.8rem', color: '#666' }}>* Thử kéo các kim để học xem giờ nhé!</p>
      </div>
    </div>
  );
}

function SVGFigure({ figure }) {
  if (!figure) return null;

  const [activeIds, setActiveIds] = useState([]);
  const { type, val, items } = figure;

  const handleTriClick = (id) => {
    setActiveIds(prev => prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]);
  };

  if (type === 'adjacent-angles') {
    // ... (keep existing logic)
    const angle = (val * Math.PI) / 180;
    const r = 120;
    const x2 = Math.cos(angle) * r;
    const y2 = -Math.sin(angle) * r;

    return (
      <div className="figure-container">
        <svg viewBox="0 0 300 200" className="geometry-svg">
          <defs>
            <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#34495e" />
            </marker>
          </defs>
          <g transform="translate(100, 150)">
            <line x1="0" y1="0" x2="150" y2="0" stroke="#34495e" strokeWidth="3" markerEnd="url(#arrow)" />
            <line x1="0" y1="0" x2={x2} y2={y2} stroke="#EA4335" strokeWidth="3" markerEnd="url(#arrow)" />
            <line x1="0" y1="0" x2="-100" y2="0" stroke="#34495e" strokeWidth="3" markerEnd="url(#arrow)" />
            <circle cx="0" cy="0" r="4" fill="#2c3e50" />
            <text x="10" y="20" fontSize="14" fontWeight="bold">O</text>
            <text x="60" y="-10" fontSize="14" fill="#EA4335">{val}°</text>
            <text x="-60" y="-10" fontSize="14" fill="#54A0FF">?</text>
          </g>
        </svg>
      </div>
    );
  }

  if (type === 'parallel-lines') {
    return (
      <div className="figure-container">
        <svg viewBox="0 0 400 200" className="geometry-svg">
          <line x1="50" y1="60" x2="350" y2="60" stroke="#34495e" strokeWidth="3" />
          <line x1="50" y1="140" x2="350" y2="140" stroke="#34495e" strokeWidth="3" />
          <line x1="120" y1="20" x2="280" y2="180" stroke="#EA4335" strokeWidth="3" />
          <text x="360" y="65" fontSize="14">a</text>
          <text x="360" y="145" fontSize="14">b</text>
          <text x="290" y="180" fontSize="14">c</text>
        </svg>
      </div>
    );
  }

  if (type === 'interactive-triangles') {
    return (
      <div className="figure-container" style={{ flexDirection: 'column' }}>
        <svg viewBox="0 0 400 250" className="geometry-svg">
          <defs>
            <filter id="shadow">
              <feDropShadow dx="0" dy="2" stdDeviation="2" floodOpacity="0.2"/>
            </filter>
          </defs>
          {items.map(tri => (
            <g key={tri.id}>
              <polygon
                points={tri.points}
                className={`geometric-polygon ${activeIds.includes(tri.id) ? 'active' : ''}`}
                style={{
                  fill: activeIds.includes(tri.id) ? (tri.color || 'rgba(255,107,107,0.4)') : 'rgba(0,0,0,0.05)',
                  stroke: activeIds.includes(tri.id) ? 'var(--clr-accent)' : '#333',
                  strokeWidth: activeIds.includes(tri.id) ? 3 : 2
                }}
                onClick={() => handleTriClick(tri.id)}
              />
              {/* Optional: Label for each vertex if provided in data */}
              {tri.labels && tri.labels.map((l, idx) => (
                <text 
                  key={idx} 
                  x={l.x} 
                  y={l.y} 
                  fontSize="14" 
                  fontWeight="900" 
                  fill="#333"
                  className="vertex-label"
                >
                  {l.text}
                </text>
              ))}
            </g>
          ))}
        </svg>
        <p style={{ fontSize: '0.85rem', color: '#666', marginTop: '10px', fontStyle: 'italic' }}>
          * Nhấn vào một tam giác để làm nổi bật và quan sát!
        </p>
      </div>
    );
  }

  return null;
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

function TopicList({ grade, subject, onSelectSubject, onSelect, onBack, onHome }) {
  const allTopics = topics[grade.id] || [];
  const subjects = [...new Set(allTopics.filter(t => t.subject).map(t => t.subject))];
  
  const displayTopics = subject 
    ? allTopics.filter(t => t.subject === subject)
    : (subjects.length > 0 ? [] : allTopics);

  return (
    <div>
      <div className="breadcrumb">
        <div className="breadcrumb-item" onClick={onHome}>🏠 Trang chủ</div>
        <span className="breadcrumb-sep">›</span>
        <div 
          className={`breadcrumb-item ${!subject ? 'active' : ''}`} 
          onClick={() => onSelectSubject(null)}
          style={!subject ? { background: grade.color, borderColor: grade.color, color: 'white' } : {}}
        >
          {grade.emoji} {grade.name}
        </div>
        {subject && (
          <>
            <span className="breadcrumb-sep">›</span>
            <div className="breadcrumb-item active" style={{ background: grade.color, borderColor: grade.color, color: 'white' }}>
              {subject}
            </div>
          </>
        )}
      </div>

      <div className="page-title">
        <h2>{grade.emoji} {subject || `Chủ Đề ${grade.name}`}</h2>
        <p>{subject ? `Khám phá các chuyên đề ${subject}!` : 'Chọn một môn học hoặc chủ đề bạn muốn luyện tập hôm nay!'}</p>
      </div>

      {subjects.length > 0 && !subject ? (
        <div className="grade-grid">
          {subjects.map(s => {
            // Lấy emoji và màu từ chủ đề đầu tiên trong môn học này
            const firstTopic = allTopics.find(t => t.subject === s);
            return (
              <div
                key={s}
                className="grade-card"
                style={{ background: `linear-gradient(135deg, ${firstTopic?.color || '#3498db'}, #2c3e50)` }}
                onClick={() => onSelectSubject(s)}
              >
                <span className="grade-emoji">{firstTopic?.emoji || '📚'}</span>
                <span className="grade-name">{s}</span>
                <span className="grade-desc">{allTopics.filter(t => t.subject === s).length} chuyên đề</span>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="topic-grid">
          {displayTopics.map(t => (
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
      )}
      
      {(subject || subjects.length === 0) && (
        <div style={{ marginTop: '30px', textAlign: 'center' }}>
          <button className="btn-story" onClick={onBack} style={{ background: '#ecf0f1', color: '#2c3e50' }}>
            ⬅️ Quay lại
          </button>
        </div>
      )}
    </div>
  );
}

function QuizPage({ grade, topic, onBack, onHome, onAddStars }) {
  const isExam = topic.id.includes('midterm') || topic.id.includes('final');
  
  // Khởi tạo danh sách câu hỏi (trộn và lấy tối đa 10 câu)
  const [problemList] = useState(() => {
    const all = topic.problemIds.map(id => problems[id]).filter(Boolean);
    const shuffled = [...all].sort(() => Math.random() - 0.5);
    return shuffled.slice(0, 10);
  });

  const [idx, setIdx] = useState(0);
  const [selected, setSelected] = useState(null);
  const [correct, setCorrect] = useState(0);
  const [done, setDone] = useState(false);
  const [modalKey, setModalKey] = useState(null);
  const [activeTool, setActiveTool] = useState(null); // 'sticks' hoặc 'draw'
  
  // Timer cho đề thi (giới hạn 10 phút = 600 giây)
  const [secondsLeft, setSecondsLeft] = useState(600);
  const [startTime] = useState(Date.now());

  useEffect(() => {
    if (!isExam || done) return;
    const timer = setInterval(() => {
      setSecondsLeft(prev => {
        if (prev <= 1) {
          setDone(true);
          clearInterval(timer);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [isExam, done]);

  const current = problemList[idx];
  const progress = ((idx) / problemList.length) * 100;

  function handleChoice(i) {
    if (selected !== null) return;
    setSelected(i);
    stopSpeak();
    
    if (i === current.answer) {
      playSound('correct');
      setCorrect(c => c + 1);
      onAddStars(1);
      try {
        confetti({
          particleCount: 120,
          spread: 70,
          origin: { y: 0.6 },
          colors: ['#FF6B6B', '#FF9F43', '#FECA57', '#54A0FF', '#00B894', '#5F27CD'],
        });
      } catch (e) {
        console.error("Confetti error:", e);
      }
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
      setActiveTool(null); // Reset tool for next question
    }
  }

  if (done) {
    const score = correct;
    const total = problemList.length;
    const pct = Math.round((score / total) * 100);
    const timeSpent = Math.floor((Date.now() - startTime) / 1000);
    const min = Math.floor(timeSpent / 60);
    const sec = timeSpent % 60;

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
          {isExam && (
            <div style={{ marginBottom: '20px', fontWeight: 'bold', color: '#54A0FF' }}>
              ⏱️ Thời gian hoàn thành: {min} phút {sec} giây
            </div>
          )}
          <div className="result-actions">
            <button className="btn-secondary" onClick={() => window.location.reload()}>
              🔄 Làm Bài Mới
            </button>
            <button className="next-btn" style={{ flex: 1 }} onClick={onBack}>
              📚 Chủ Đề Khác
            </button>
          </div>
        </div>
      </div>
    );
  }

  const formatTime = (s) => {
    const m = Math.floor(s / 60);
    const rs = s % 60;
    return `${m}:${rs < 10 ? '0' : ''}${rs}`;
  };

  function handleReadQuestion() {
    if (window.speechSynthesis.speaking) {
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
            {isExam && (
              <span className="progress-text" style={{ color: secondsLeft < 60 ? '#FF6B6B' : 'inherit', fontWeight: 'bold' }}>
                ⏱️ {formatTime(secondsLeft)}
              </span>
            )}
            <span className="progress-text">✅ {correct}</span>
          </div>
        </div>

        <div className="question-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <span className="question-number">Câu {idx + 1}</span>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button className="btn-read-aloud" onClick={handleReadQuestion} title="Đọc câu hỏi">
                🔊 Nghe Đọc
              </button>
            </div>
          </div>
          {(() => {
            const lines = current.question.split('\n');
            const isHeading = lines.length > 1 && /^(I{1,3}|IV|V?I{0,3}V?)\.\s/.test(lines[0]);
            if (isHeading) {
              return (
                <>
                  <p className="question-section-heading">{lines[0]}</p>
                  <p className="question-text">{lines.slice(1).join('\n')}</p>
                </>
              );
            }
            return <p className="question-text" style={{ whiteSpace: 'pre-line' }}>{current.question}</p>;
          })()}
          
          {current.images && current.images.length > 0 && (
            <div className="problem-images">
              {current.images.map((imgSrc, idx) => (
                <img key={idx} src={imgSrc} alt={`Minh họa ${idx + 1}`} style={{ maxWidth: '100%', borderRadius: '8px', marginTop: '10px' }} />
              ))}
            </div>
          )}
          
          {current.figure && <SVGFigure figure={current.figure} />}
          
          {current.illustration && (
            <div className="problem-illustration">{current.illustration}</div>
          )}
          
          <div className="tools-container">
            <div className="tool-header">
              {grade.id === 1 && (
                <button 
                  className={`btn-tool ${activeTool === 'sticks' ? 'active' : ''}`} 
                  onClick={() => setActiveTool(activeTool === 'sticks' ? null : 'sticks')}
                >
                  🥢 Dùng Que Tính
                </button>
              )}
              {(topic.id === 'g1-clock' || topic.id === 'g2-clock') && (
                <button 
                  className={`btn-tool ${activeTool === 'clock' ? 'active' : ''}`} 
                  onClick={() => setActiveTool(activeTool === 'clock' ? null : 'clock')}
                >
                  🕒 Dùng Đồng Hồ
                </button>
              )}
          {grade.id === 7 && (
                <button 
                  className={`btn-tool ${activeTool === 'draw' ? 'active' : ''}`} 
                  onClick={() => setActiveTool(activeTool === 'draw' ? null : 'draw')}
                >
                  📐 Vẽ Hình Hình Học
                </button>
              )}
              {grade.id !== 7 && (
                <button 
                  className={`btn-tool ${activeTool === 'draw' ? 'active' : ''}`} 
                  onClick={() => setActiveTool(activeTool === 'draw' ? null : 'draw')}
                >
                  🎨 Bảng Vẽ Nháp
                </button>
              )}
            </div>
            {activeTool === 'sticks' && <StickTool />}
            {activeTool === 'draw' && <DrawingBoard />}
            {activeTool === 'clock' && <ClockTool />}
          </div>
        </div>

        <div className="choices-grid">
          {current.type === 'essay' ? (
            <button 
              className={`choice-btn ${selected !== null ? 'correct' : ''}`} 
              onClick={() => handleChoice(0)} 
              disabled={selected !== null}
              style={{ gridColumn: '1 / -1' }}
            >
              📝 Xem lời giải chi tiết
            </button>
          ) : (
            current.choices.map((c, i) => {
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
            })
          )}
        </div>

        {selected !== null && (
          <div className="solution-panel">
            <div className="solution-title">
              {selected === current.answer ? '🌟 Chính xác! Xem giải thích:' : '💡 Chưa đúng! Đây là cách giải:'}
            </div>
            
            {current.solutionIllustration && (
              <div className="solution-illustration">
                {current.solutionIllustration}
              </div>
            )}

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
  const [subject, setSubject] = useState(null);
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
            subject={subject}
            onSelectSubject={s => setSubject(s)}
            onSelect={t => { setTopic(t); setView('quiz'); }}
            onBack={() => {
              if (subject) setSubject(null);
              else setView('home');
            }}
            onHome={() => { setSubject(null); setView('home'); }}
          />
        )}
        {view === 'quiz' && grade && topic && (
          <QuizPage
            key={topic.id}
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
