import fs from 'fs';
import path from 'path';

const SRC_DIR = './src/data';
const topicsPath = path.join(SRC_DIR, 'topics.js');
const problemsPath = path.join(SRC_DIR, 'problems.js');

// ─── UTILS ────────────────────────────────────────────────────────────
function randInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function randItem(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

const names = ['Lan', 'Bình', 'Hoa', 'Huy', 'Minh', 'Tuấn', 'Mai', 'An', 'Nam', 'Trang'];
const fruits = ['quả táo 🍎', 'quả cam 🍊', 'quả chuối 🍌', 'quả dâu 🍓', 'quả bưởi 🍈'];
const animals = ['con mèo 🐱', 'con chó 🐶', 'con chim 🐦', 'con cá 🐟', 'con thỏ 🐰'];
const objects = ['cái kẹo 🍬', 'chiếc bánh 🍰', 'viên bi 🔵', 'quyển sách 📖', 'cây bút ✏️'];

// Sinh 4 đáp án (1 đúng, 3 sai), xáo trộn và trả về [choices, answerIndex]
function generateChoices(correctAnswer, offset = 10, isFloat = false) {
  let choicesSet = new Set([correctAnswer]);
  while (choicesSet.size < 4) {
    let wrong = isFloat
      ? (parseFloat(correctAnswer) + (Math.random() * offset - offset / 2)).toFixed(1)
      : parseInt(correctAnswer) + randInt(-offset, offset);
    if (wrong !== correctAnswer && wrong > 0) {
      choicesSet.add(isFloat ? wrong.toString() : wrong);
    }
  }
  let choices = Array.from(choicesSet).map(String);
  choices.sort(() => Math.random() - 0.5);
  return [choices, choices.indexOf(String(correctAnswer))];
}

// ─── GENERATE PROBLEM LOGIC (by Topic ID prefix) ──────────────────────
function generateProblemForTopic(topicId, currentProblemCount) {
  const pId = `${topicId}-gen-${currentProblemCount}`;
  let question = '';
  let answerStr = '';
  let steps = [];
  let highlight = null;
  const t = topicId;

  const n = randItem(names);
  const f = randItem(fruits);
  const a = randItem(animals);
  const o = randItem(objects);

  try {
    // === LỚP 1 ===
    if (t.includes('g1-add')) {
      let a = randInt(1, 9); let b = randInt(1, 10 - a);
      if (Math.random() > 0.5) { a = randInt(1, 50); b = randInt(1, 40); }
      question = `${n} có ${a} ${f}, được tặng thêm ${b} ${f}. Hỏi ${n} có tất cả bao nhiêu ${f}?`;
      answerStr = a + b;
      steps = [
        { text: `Sử dụng phép cộng: ${a} + ${b} = ${answerStr}`, highlight: 'phep-cong' },
        { text: `Vậy ${n} có tất cả ${answerStr} ${f}.`, highlight: null }
      ];
    } else if (t.includes('g1-sub')) {
      let a = randInt(5, 50); let b = randInt(1, a - 1);
      question = `Trên cành có ${a} ${a < 10 ? 'con chim 🐦' : 'chiếc lá 🍃'}. Có ${b} ${a < 10 ? 'con bay đi' : 'chiếc rơi xuống'}. Còn lại bao nhiêu?`;
      answerStr = a - b;
      steps = [
        { text: `Lấy tổng số ban đầu trừ đi số bị mất. Dùng phép trừ: ${a} - ${b} = ${answerStr}`, highlight: 'phep-tru' },
        { text: `Vậy còn lại ${answerStr}.`, highlight: null }
      ];
    } else if (t.includes('g1-count')) {
      let num = randInt(11, 20);
      question = `Số nào liền sau số ${num - 1}?`;
      answerStr = num;
      steps = [{ text: `Đếm tiếp 1 đơn vị từ ${num - 1} là ${num}.`, highlight: null }];
    } else if (t.includes('g1-len')) {
      let a = randInt(1, 15); let b = randInt(1, 10);
      question = `Một sợi dây dài ${a}cm nối với sợi dây dài ${b}cm. Hỏi cả hai dài bao nhiêu cm?`;
      answerStr = `${a + b}cm`;
      steps = [{ text: `${a}cm + ${b}cm = ${a + b}cm.`, highlight: 'phep-cong' }];
      const [choices, ansIdx] = generateChoices(a + b, 10);
      return { id: pId, topicId, question, choices: choices.map(c => c + 'cm'), answer: ansIdx, steps };
    }
    // === LỚP 2 ===
    else if (t.includes('g2-add')) {
      let a = randInt(15, 85); let b = randInt(10, 95 - a);
      if ((a % 10) + (b % 10) < 10) b += (10 - ((a % 10) + (b % 10))); // force carry
      question = `Tính: ${a} + ${b} = ?`;
      answerStr = a + b;
      steps = [{ text: `Cộng từ phải sang trái. Hàng đơn vị: ${a % 10} + ${b % 10} có nhớ. ${a} + ${b} = ${answerStr}.`, highlight: 'co-nho' }];
    } else if (t.includes('g2-sub')) {
      let a = randInt(30, 95); let b = randInt(15, a - 1);
      if ((a % 10) >= (b % 10)) a -= (a % 10) + 1; // force borrow
      question = `Tìm M: M = ${a} - ${b}`;
      answerStr = a - b;
      steps = [{ text: `Trừ có mượn: ${a} - ${b} = ${answerStr}.`, highlight: 'phep-tru' }];
    } else if (t.includes('g2-mul')) {
      let a = randInt(2, 5); let b = randInt(2, 9);
      question = `Tính phép nhân: ${a} × ${b}`;
      answerStr = a * b;
      steps = [{ text: `${a} nhân ${b} bằng ${answerStr}.`, highlight: 'phep-nhan' }];
    } else if (t.includes('g2-findx')) {
      let x = randInt(10, 50); let y = randInt(10, 50);
      if (Math.random() > 0.5) {
        question = `Tìm x biết: x - ${x} + x + ${y} = ${x + y}. Tính x? (đùa thôi, giải x + ${y} = ${x + y})`;
        question = `Tìm x: x + ${y} = ${x + y}`;
        answerStr = x;
        steps = [{ text: `x = ${x + y} - ${y} = ${x}`, highlight: 'phep-tru' }];
      } else {
        question = `Tìm x: x - ${y} = ${x}`;
        answerStr = x + y;
        steps = [{ text: `x = ${x} + ${y} = ${x + y}`, highlight: 'phep-cong' }];
      }
    } else if (t.includes('g2-measure')) {
      let w1 = randInt(5, 20); let w2 = randInt(5, 15);
      question = `Lợn cân nặng ${w1}kg. Chó nặng thêm ${w2}kg. Cả hai nặng bao nhiêu?`;
      answerStr = w1 + w1 + w2 + 'kg';
      steps = [{ text: `Chó: ${w1} + ${w2} = ${w1 + w2}kg. Tổng = ${w1} + ${w1 + w2} = ${w1 * 2 + w2}kg.`, highlight: 'phep-cong' }];
      const val = w1 * 2 + w2;
      const [choices, ansIdx] = generateChoices(val, 20);
      return { id: pId, topicId, question, choices: choices.map(c => c + 'kg'), answer: ansIdx, steps };
    }
    // === LỚP 3 ===
    else if (t.includes('g3-mul') || t.includes('g3-nhanchia') || t.includes('g3-nc')) {
      let a = randInt(11, 150); let b = randInt(2, 9);
      question = `${a} × ${b} = ?`;
      answerStr = a * b;
      steps = [{ text: `Đổi thành phép cộng nhiều lần hoặc đặt tính nhân: ${a} × ${b} = ${answerStr}.`, highlight: 'phep-nhan' }];
    } else if (t.includes('g3-div')) {
      let b = randInt(2, 9); let c = randInt(5, 40); let a = b * c;
      question = `Tính: ${a} ÷ ${b} = ?`;
      answerStr = c;
      steps = [{ text: `Tìm số nhân với ${b} bằng ${a}. Đó là ${c}.`, highlight: 'phep-chia' }];
    } else if (t.includes('g3-frac')) {
      let a = randInt(2, 5); let m = randInt(10, 50);
      let v = m * a;
      question = `1/${a} của ${v} là bao nhiêu?`;
      answerStr = m;
      steps = [{ text: `Lấy ${v} chia cho ${a} = ${m}.`, highlight: 'phan-so' }];
    } else if (t.includes('g3-chuvi')) {
      let mode = randInt(0, 1);
      if (mode === 0) { // square
        let c = randInt(4, 25);
        question = `Chu vi hình vuông có cạnh ${c}cm là?`;
        answerStr = `${c * 4}cm`;
        steps = [{ text: `Chu vi = 4 × cạnh = 4 × ${c} = ${c * 4}cm.`, highlight: 'hinh-vuong' }];
        const [choices, ansIdx] = generateChoices(c * 4, 15);
        return { id: pId, topicId, question, choices: choices.map(c => c + 'cm'), answer: ansIdx, steps };
      } else {
        let l = randInt(10, 30); let w = randInt(5, l - 1);
        question = `Chu vi hình chữ nhật có dài ${l}cm, rộng ${w}cm là?`;
        answerStr = `${(l + w) * 2}cm`;
        steps = [{ text: `Chu vi = (Dài + Rộng) × 2 = (${l} + ${w}) × 2 = ${(l + w) * 2}cm.`, highlight: 'hinh-chu-nhat' }];
        const [choices, ansIdx] = generateChoices((l + w) * 2, 20);
        return { id: pId, topicId, question, choices: choices.map(c => c + 'cm'), answer: ansIdx, steps };
      }
    }
    // === LỚP 4 ===
    else if (t.includes('g4-frac')) {
      let a = randInt(1, 3); let b = randInt(4, 7);
      let m = randInt(2, 5);
      question = `Rút gọn phân số ${(a * m)}/${(b * m)}.`;
      answerStr = `${a}/${b}`;
      steps = [{ text: `Chia cả tử và mẫu cho ${m}. Ta được ${a}/${b}.`, highlight: 'uoc-chung' }];
      return {
        id: pId, topicId, question,
        choices: [`${a}/${b}`, `${a + 1}/${b}`, `${a}/${b + 1}`, `${a + 2}/${b + 2}`].sort(() => Math.random() - 0.5),
        answer: -1, // fixed below
        steps
      };
    } else if (t.includes('g4-geom')) {
      let l = randInt(10, 50); let w = randInt(5, l);
      question = `Diện tích hình chữ nhật dài ${l}m, rộng ${w}m là?`;
      answerStr = `${l * w}m²`;
      steps = [{ text: `Diện tích = Dài × Rộng = ${l} × ${w} = ${l * w}m².`, highlight: 'hinh-chu-nhat' }];
      const [choices, ansIdx] = generateChoices(l * w, 50);
      return { id: pId, topicId, question, choices: choices.map(c => c + 'm²'), answer: ansIdx, steps };
    } else if (t.includes('g4-word')) {
      let n_boxes = randInt(5, 15); let items = randInt(8, 20);
      question = `Mỗi hộp đựng ${items} ${o}. Có ${n_boxes} hộp thì có tất cả bao nhiêu?`;
      answerStr = n_boxes * items;
      steps = [{ text: `${n_boxes} × ${items} = ${answerStr}.`, highlight: 'phep-nhan' }];
    } else if (t.includes('g4-logic')) {
      let a = randInt(2, 5);
      question = `Có gà và thỏ. Tổng cộng ${a} con và có ${a * 3 + (a % 2 === 0 ? 0 : 1)} chân. Lừa bạn đấy, câu logic dễ thôi: Trong 1 tháng cao nhất có bao nhiêu ngày Chủ Nhật?`;
      return {
        id: pId, topicId, question,
        choices: ['4 ngày', '5 ngày', '6 ngày', '3 ngày'],
        answer: 1,
        steps: [{ text: `Nếu mùng 1 là Chủ Nhật và tháng có 31 ngày thì mùng 1, 8, 15, 22, 29 là Chủ Nhật (5 ngày).`, highlight: null }]
      };
    } else if (t.includes('g4-div')) {
      let num = randInt(100, 999);
      while (num % 5 !== 0) num++;
      question = `Số nào dưới đây chia hết cho 5?`;
      answerStr = num;
      let w1 = num + 1, w2 = num + 2, w3 = num + 3;
      steps = [{ text: `Số chia hết cho 5 tận cùng là 0 hoặc 5.`, highlight: null }];
      let choices = [num, w1, w2, w3].map(String).sort(() => Math.random() - 0.5);
      return { id: pId, topicId, question, choices, answer: choices.indexOf(String(num)), steps };
    } else if (t.includes('g4-avg')) {
      let a = randInt(10, 50); let b = randInt(10, 50); let c = randInt(10, 50);
      let sum = a + b + c;
      if (sum % 3 !== 0) c += (3 - (sum % 3));
      question = `Trung bình cộng của ${a}, ${b}, ${c} là bao nhiêu?`;
      answerStr = (a + b + c) / 3;
      steps = [{ text: `(${a} + ${b} + ${c}) ÷ 3 = ${(a + b + c)} ÷ 3 = ${answerStr}`, highlight: 'phep-chia' }];
    }
    // === LỚP 5 ===
    else if (t.includes('g5-percent')) {
      let total = randInt(4, 20) * 10; let p = randInt(1, 9) * 10;
      question = `${p}% của ${total} là bao nhiêu?`;
      answerStr = (total * p) / 100;
      steps = [{ text: `${p}/100 × ${total} = ${answerStr}.`, highlight: 'ti-le-phan-tram' }];
    } else if (t.includes('g5-area')) {
      let a = randInt(5, 20);
      question = `Diện tích hình vuông cạnh ${a}m là bao nhiêu m²?`;
      answerStr = a * a;
      steps = [{ text: `Diện tích = ${a} × ${a} = ${answerStr}m².`, highlight: 'hinh-vuong' }];
    } else if (t.includes('g5-word')) {
      let a = randInt(2, 6) * 1000; let b = randInt(2, 5);
      question = `Một siêu thị bán bột giặt túi ${b}kg giá ${a * b} đồng. Hỏi 1kg giá bao nhiêu?`;
      answerStr = a;
      steps = [{ text: `${a * b} ÷ ${b} = ${a} đồng.`, highlight: 'phep-chia' }];
    } else if (t.includes('g5-logic')) {
      question = `Cái gì càng lớn càng nhỏ? (Đố vui toán học)`;
      return {
        id: pId, topicId, question,
        choices: ['Lỗ hổng', 'Quả bóng', 'Tuổi tác', 'Cái kẹo'], answer: 0,
        steps: [{ text: `Lỗ hổng càng lớn thì phần vật chất còn lại càng nhỏ.`, highlight: null }]
      };
    } else if (t.includes('g5-dec')) {
      let a = (randInt(10, 99) / 10).toFixed(1);
      let b = (randInt(10, 99) / 10).toFixed(1);
      question = `${a} + ${b} = ?`;
      answerStr = (parseFloat(a) + parseFloat(b)).toFixed(1);
      steps = [{ text: `Cộng số thập phân giống như số tự nhiên: ${a} + ${b} = ${answerStr}.`, highlight: 'phep-cong' }];
      const [choices, ansIdx] = generateChoices(answerStr, 5, true);
      return { id: pId, topicId, question, choices, answer: ansIdx, steps };
    } else if (t.includes('g5-vel')) {
      let v = randInt(30, 80); let h = randInt(2, 5);
      question = `Xe ôtô đi với vận tốc ${v}km/h. Trong ${h} giờ xe đi được bao nhiêu km?`;
      answerStr = v * h;
      steps = [{ text: `Quãng đường = Vận tốc × Thời gian = ${v} × ${h} = ${answerStr}km.`, highlight: 'phep-nhan' }];
    }
    // Fallback
    else {
      let a = randInt(1, 100); let b = randInt(1, 100);
      question = `${a} + ${b} = ?`; answerStr = a + b;
      steps = [{ text: `Tính ${a} + ${b} = ${answerStr}.`, highlight: 'phep-cong' }];
    }

    const [choices, ansIdx] = generateChoices(answerStr, 15);
    return {
      id: pId, topicId, question,
      choices: choices.map(String), answer: ansIdx, steps
    };

  } catch (err) {
    let a = randInt(1, 10);
    return {
      id: pId, topicId, question: `${a} + 1 = ?`, choices: Object.keys([...Array(4)]).map(x => String(Number(x) + a)), answer: 1, steps: []
    }
  }
}

// ─── EXECUTE ──────────────────────────────────────────────────────────

async function main() {
  console.log("Đang đọc dữ liệu...");
  // Using dynamic import trick for es module files without package json resolving locally 
  // Wait, we can just read the file via regex or export it to a temporary module wrapper.
  const topicsCode = fs.readFileSync(topicsPath, 'utf8');
  const problemsCode = fs.readFileSync(problemsPath, 'utf8');

  // Strip 'export const' to parse with eval
  const cleanTopics = topicsCode.replace(/^export const topics = /m, '').replace(/;?\s*$/m, '');
  let topicsData;
  eval('topicsData = ' + cleanTopics);

  const cleanProblems = problemsCode.replace(/^export const problems = /m, '').replace(/;?\s*$/m, '');
  let problemsData;
  eval('problemsData = ' + cleanProblems);

  console.log("Bắt đầu sinh dữ liệu...");

  // Generate for existing topics so each has 10
  for (let grade of [1, 2, 3, 4, 5]) {
    const list = topicsData[grade];
    if (list) {
      for (const t of list) {
        while (t.problemIds.length < 10) {
          const np = generateProblemForTopic(t.id, t.problemIds.length);
          // if it returns ansIdx = -1, update choices answer match
          if (np.answer === -1) {
            np.answer = np.choices.indexOf(np.steps[0].text.split('.')[1].trim().split(' ')[2]); // rough fix for fractions
            if (np.answer === -1) np.answer = 0;
          }
          if (!problemsData[np.id]) {
            problemsData[np.id] = np;
            t.problemIds.push(np.id);
          }
        }
      }
    }
  }

  // Add Midterm and Final for each grade
  for (let grade of [1, 2, 3, 4, 5]) {
    const list = topicsData[grade];

    if (!list.find(x => x.id === `g${grade}-midterm`)) {
      list.push({
        id: `g${grade}-midterm`, gradeId: grade, name: 'Đề Kiểm Tra Giữa Kỳ', emoji: '📝', color: '#FF6B6B', problemIds: []
      });
    }
    if (!list.find(x => x.id === `g${grade}-final`)) {
      list.push({
        id: `g${grade}-final`, gradeId: grade, name: 'Đề Kiểm Tra Cuối Kỳ', emoji: '🎓', color: '#00B894', problemIds: []
      });
    }

    const midterm = list.find(x => x.id === `g${grade}-midterm`);
    const finalTerm = list.find(x => x.id === `g${grade}-final`);

    // Collect all problem IDs from this grade's topics to randomize exam
    const allGradeProbIds = list.filter(t => !t.id.includes('midterm') && !t.id.includes('final')).map(t => t.problemIds).flat();

    while (midterm.problemIds.length < 10) {
      const rp = randItem(allGradeProbIds);
      if (!midterm.problemIds.includes(rp)) midterm.problemIds.push(rp);
    }
    while (finalTerm.problemIds.length < 10) {
      const rp = randItem(allGradeProbIds);
      if (!finalTerm.problemIds.includes(rp)) finalTerm.problemIds.push(rp); // 10
    }
  }

  // Write back topics
  const outTopics = `export const topics = ${JSON.stringify(topicsData, null, 2)};\n`;
  fs.writeFileSync(topicsPath, outTopics);

  // Write back problems
  const outProblems = `export const problems = ${JSON.stringify(problemsData, null, 2)};\n`;
  fs.writeFileSync(problemsPath, outProblems);

  console.log("Hoàn thành sinh dữ liệu: " + Object.keys(problemsData).length + " bài tập!");
}

main();
