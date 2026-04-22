import fs from 'fs';
import path from 'path';

// Helper to generate a range of problem IDs
const genIds = (prefix, count) => Array.from({length: count}, (_, i) => `${prefix}-${i+1}`);

const g7Topics = [
  {
    id: "g7-rational",
    gradeId: 7,
    name: "Số hữu tỉ & Lũy thừa",
    emoji: "🔢",
    color: "#4285F4",
    problemIds: genIds("g7-rat", 50)
  },
  {
    id: "g7-real",
    gradeId: 7,
    name: "Số thực & Căn bậc hai",
    emoji: "♾️",
    color: "#34A853",
    problemIds: genIds("g7-real", 50)
  },
  {
    id: "g7-geometry-3d",
    gradeId: 7,
    name: "Hình khối & Lăng trụ",
    emoji: "📦",
    color: "#EA4335",
    problemIds: genIds("g7-geo3d", 50)
  },
  {
    id: "g7-angles",
    gradeId: 7,
    name: "Góc & Đ.thẳng song song",
    emoji: "📐",
    color: "#FBBC05",
    problemIds: genIds("g7-angle", 50)
  },
  {
    id: "g7-statistics",
    gradeId: 7,
    name: "Thống kê & Xác suất",
    emoji: "📊",
    color: "#8E44AD",
    problemIds: genIds("g7-stat", 50)
  },
  {
    id: "g7-triangles",
    gradeId: 7,
    name: "Quan hệ trong Tam giác",
    emoji: "🔺",
    color: "#16A085",
    problemIds: genIds("g7-tri", 50)
  },
  {
    id: "g7-exam-final",
    gradeId: 7,
    name: "Ôn tập Tổng hợp",
    emoji: "🏆",
    color: "#F39C12",
    problemIds: genIds("g7-exam", 50)
  }
];

function generateProblems() {
  const problems = {};

  // 1. Rational Numbers (50 questions)
  for (let i = 1; i <= 50; i++) {
    const a = Math.floor(Math.random() * 20) - 10;
    const b = Math.floor(Math.random() * 10) + 1;
    const c = Math.floor(Math.random() * 20) - 10;
    const d = Math.floor(Math.random() * 10) + 1;
    
    // Pattern 1: Addition/Subtraction
    if (i <= 20) {
      const isAdd = Math.random() > 0.5;
      const op = isAdd ? '+' : '-';
      const ans_num = isAdd ? (a*d + c*b) : (a*d - c*b);
      const ans_den = b*d;
      
      problems[`g7-rat-${i}`] = {
        id: `g7-rat-${i}`,
        topicId: "g7-rational",
        question: `Tính kết quả của phép tính: (${a}/${b}) ${op} (${c}/${d})`,
        choices: [
          `${ans_num}/${ans_den}`,
          `${ans_num+1}/${ans_den}`,
          `${ans_num-b}/${ans_den}`,
          `${ans_num}/${ans_den+2}`
        ],
        answer: 0,
        knowledgeKey: "số hữu tỉ"
      };
    } 
    // Pattern 2: Powers
    else {
      const base = 2 + Math.floor(Math.random() * 3);
      const n = 2 + Math.floor(Math.random() * 5);
      const m = 2 + Math.floor(Math.random() * 5);
      problems[`g7-rat-${i}`] = {
        id: `g7-rat-${i}`,
        topicId: "g7-rational",
        question: `Kết quả của ${base}^${n} * ${base}^${m} là:`,
        choices: [
          `${base}^${n+m}`,
          `${base}^${n*m}`,
          `${base}^${n-m}`,
          `${base*2}^${n+m}`
        ],
        answer: 0,
        knowledgeKey: "lũy thừa"
      };
    }
  }

  // 2. Real Numbers & Square Roots
  for (let i = 1; i <= 50; i++) {
    const n = Math.floor(Math.random() * 15) + 1;
    const n2 = n * n;
    problems[`g7-real-${i}`] = {
      id: `g7-real-${i}`,
      topicId: "g7-real",
      question: `Căn bậc hai số học của ${n2} là:`,
      choices: [
        `${n}`,
        `${n2}`,
        `${n*2}`,
        `${Math.sqrt(n2/2).toFixed(2)}`
      ],
      answer: 0,
      knowledgeKey: "căn bậc hai"
    };
  }

  // 3. Geometry 3D (Shapes)
  for (let i = 1; i <= 50; i++) {
    const a = 5 + Math.floor(Math.random() * 10);
    const b = 3 + Math.floor(Math.random() * 5);
    const h = 4 + Math.floor(Math.random() * 8);
    const V = a * b * h;
    problems[`g7-geo3d-${i}`] = {
      id: `g7-geo3d-${i}`,
      topicId: "g7-geometry-3d",
      question: `Một hình hộp chữ nhật có ba kích thước lần lượt là ${a}cm, ${b}cm, ${h}cm. Thể tích của nó là:`,
      choices: [
        `${V} cm³`,
        `${V + 10} cm³`,
        `${(a+b)*h} cm³`,
        `${a*b} cm³`
      ],
      answer: 0,
      knowledgeKey: "hình hộp chữ nhật"
    };
  }

  // 4. Angles & Parallel Lines
  for (let i = 1; i <= 50; i++) {
    const angle = 30 + Math.floor(Math.random() * 120);
    const supplement = 180 - angle;
    
    if (i <= 25) {
      problems[`g7-angle-${i}`] = {
        id: `g7-angle-${i}`,
        topicId: "g7-angles",
        question: `Hai góc kề bù có một góc bằng ${angle}°. Góc còn lại là:`,
        choices: [
          `${supplement}°`,
          `${angle}°`,
          `${90 - angle}°`,
          `180°`
        ],
        answer: 0,
        figure: { type: "adjacent-angles", val: angle },
        knowledgeKey: "goc-ke-bu",
        steps: [
            {"text": "Hai góc kề bù có tổng số đo là 180°.", "highlight": "goc-ke-bu"},
            {"text": `Góc còn lại = 180° - ${angle}° = ${supplement}°.`, "highlight": null}
        ]
      };
    } else {
      problems[`g7-angle-${i}`] = {
        id: `g7-angle-${i}`,
        topicId: "g7-angles",
        question: `Quan sát hai đường thẳng song song trong hình. Nếu một cặp góc so le trong bằng ${angle}°, thì góc so le trong còn lại bằng:`,
        choices: [
          `${angle}°`,
          `${supplement}°`,
          `90°`,
          `180°`
        ],
        answer: 0,
        figure: { type: "parallel-lines" },
        knowledgeKey: "duong-thang-song-song",
        steps: [
          {"text": "Khi hai đường thẳng song song, các cặp góc so le trong bằng nhau.", "highlight": "duong-thang-song-song"},
          {"text": `Vậy góc còn lại cũng bằng ${angle}°.`, "highlight": null}
        ]
      };
    }
  }
  
  // 5. Triangles
  for (let i = 1; i <= 50; i++) {
    const a = 40 + Math.floor(Math.random() * 60);
    const b = 30 + Math.floor(Math.random() * 40);
    const c = 180 - a - b;
    problems[`g7-tri-${i}`] = {
      id: `g7-tri-${i}`,
      topicId: "g7-triangles",
      question: `Trong một tam giác có hai góc lần lượt là ${a}° và ${b}°. Góc thứ ba là:`,
      choices: [
        `${c}°`,
        `${a+b}°`,
        `90°`,
        `${180 - a}°`
      ],
      answer: 0,
      knowledgeKey: "tam giác"
    };
  }

  // Fill others with generic data to ensure at least 50 each
  ['g7-stat', 'g7-exam'].forEach(prefix => {
    for(let i=1; i<=50; i++) {
      problems[`${prefix}-${i}`] = {
        id: `${prefix}-${i}`,
        topicId: prefix.startsWith('g7-stat') ? "g7-statistics" : "g7-exam-final",
        question: `Câu hỏi ôn tập ${prefix} số ${i}: Nội dung đang được cập nhật căn cứ trên tài liệu PDF.`,
        choices: ["Đáp án A", "Đáp án B", "Đáp án C", "Đáp án D"],
        answer: 0
      };
    }
  });

  return problems;
}

// EXECUTION
const problemsData = generateProblems();

// 1. Update topics.js
let topicsContent = fs.readFileSync('src/data/topics.js', 'utf8');
const topicsJsonMatch = topicsContent.match(/export const topics = (\{[\s\S]*\});/);
if (topicsJsonMatch) {
  const currentTopics = JSON.parse(topicsJsonMatch[1]);
  currentTopics["7"] = g7Topics;
  const newTopicsContent = `export const topics = ${JSON.stringify(currentTopics, null, 2)};\n`;
  fs.writeFileSync('src/data/topics.js', newTopicsContent);
}

// 2. Update problems.js
let problemsContent = fs.readFileSync('src/data/problems.js', 'utf8');
const problemsJsonMatch = problemsContent.match(/export const problems = (\{[\s\S]*\});/);
if (problemsJsonMatch) {
  const currentProblems = JSON.parse(problemsJsonMatch[1]);
  // Merge: generated problems will overwrite existing ones with same ID, but keep others
  Object.assign(currentProblems, problemsData);
  const newProblemsContent = `export const problems = ${JSON.stringify(currentProblems, null, 2)};\n`;
  fs.writeFileSync('src/data/problems.js', newProblemsContent);
}

console.log("Updated topics.js and problems.js with Grade 7 data!");
