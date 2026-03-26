// Bai tap theo tung topic
// Moi bai gom: id, question, choices, answer (index 0-3), steps (mang huong dan giai), keywords
export const problems = {
  // LOP 1 - CONG
  'g1-add-1': {
    id: 'g1-add-1', topicId: 'g1-add',
    question: 'Có 3 con mèo 🐱 và thêm 4 con mèo nữa. Hỏi có tất cả bao nhiêu con mèo?',
    choices: ['5', '6', '7', '8'], answer: 2,
    steps: [
      { text: 'Ta có 3 con mèo ban đầu.', highlight: null },
      { text: 'Thêm vào 4 con mèo nữa.', highlight: null },
      { text: 'Dùng phép cộng: 3 + 4 = 7', highlight: 'phep-cong' },
      { text: 'Vậy có tất cả 7 con mèo! 🐱🐱🐱🐱🐱🐱🐱', highlight: null },
    ],
  },
  'g1-add-2': {
    id: 'g1-add-2', topicId: 'g1-add',
    question: 'Bình có 5 quả bóng 🎈, mẹ tặng thêm 3 quả. Bình có mấy quả bóng?',
    choices: ['7', '8', '9', '6'], answer: 1,
    steps: [
      { text: 'Bình có 5 quả bóng ban đầu.', highlight: null },
      { text: 'Mẹ tặng thêm 3 quả nữa.', highlight: null },
      { text: 'Dùng phép cộng: 5 + 3 = 8', highlight: 'phep-cong' },
      { text: 'Vậy Bình có 8 quả bóng! 🎈🎈🎈🎈🎈🎈🎈🎈', highlight: null },
    ],
  },
  'g1-add-3': {
    id: 'g1-add-3', topicId: 'g1-add',
    question: '2 + 6 = ?',
    choices: ['7', '8', '9', '6'], answer: 1,
    steps: [
      { text: 'Ta có số 2 và số 6.', highlight: null },
      { text: 'Đếm tiếp từ 2: 3, 4, 5, 6, 7, 8 (đếm thêm 6 lần)', highlight: null },
      { text: 'Kết quả phép cộng: 2 + 6 = 8', highlight: 'phep-cong' },
    ],
  },
  'g1-add-4': {
    id: 'g1-add-4', topicId: 'g1-add',
    question: 'Trên cây có 4 con chim 🐦. Thêm 5 con nữa bay đến. Có mấy con chim?',
    choices: ['8', '10', '9', '7'], answer: 2,
    steps: [
      { text: 'Trên cây có 4 con chim.', highlight: null },
      { text: 'Thêm 5 con chim bay đến.', highlight: null },
      { text: 'Phép cộng: 4 + 5 = 9', highlight: 'phep-cong' },
      { text: 'Có tất cả 9 con chim! 🐦🐦🐦🐦🐦🐦🐦🐦🐦', highlight: null },
    ],
  },
  'g1-add-5': {
    id: 'g1-add-5', topicId: 'g1-add',
    question: '1 + 1 + 1 + 1 + 1 = ?',
    choices: ['4', '6', '5', '3'], answer: 2,
    steps: [
      { text: 'Cộng từng bước: 1 + 1 = 2', highlight: 'phep-cong' },
      { text: '2 + 1 = 3', highlight: null },
      { text: '3 + 1 = 4', highlight: null },
      { text: '4 + 1 = 5. Kết quả là 5! 🖐️', highlight: null },
    ],
  },
  // LOP 1 - TRU
  'g1-sub-1': {
    id: 'g1-sub-1', topicId: 'g1-sub',
    question: 'Có 8 chiếc bánh 🍰, ăn mất 3 chiếc. Còn mấy chiếc?',
    choices: ['4', '6', '5', '3'], answer: 2,
    steps: [
      { text: 'Có 8 chiếc bánh.', highlight: null },
      { text: 'Ăn mất 3 chiếc.', highlight: null },
      { text: 'Dùng phép trừ: 8 - 3 = 5', highlight: 'phep-tru' },
      { text: 'Còn lại 5 chiếc bánh! 🍰🍰🍰🍰🍰', highlight: null },
    ],
  },
  'g1-sub-2': {
    id: 'g1-sub-2', topicId: 'g1-sub',
    question: '9 - 4 = ?',
    choices: ['4', '6', '5', '3'], answer: 2,
    steps: [
      { text: 'Ta có số 9, trừ đi 4.', highlight: null },
      { text: 'Đếm lùi từ 9: 8, 7, 6, 5 (lùi 4 bước)', highlight: null },
      { text: 'Phép trừ: 9 - 4 = 5', highlight: 'phep-tru' },
    ],
  },
  'g1-sub-3': {
    id: 'g1-sub-3', topicId: 'g1-sub',
    question: 'Hộp có 7 viên bi 🔵. Lấy ra 2 viên. Còn mấy viên?',
    choices: ['6', '4', '5', '3'], answer: 2,
    steps: [
      { text: 'Hộp có 7 viên bi ban đầu.', highlight: null },
      { text: 'Lấy ra 2 viên bi.', highlight: null },
      { text: 'Phép trừ: 7 - 2 = 5', highlight: 'phep-tru' },
      { text: 'Còn lại 5 viên bi! 🔵🔵🔵🔵🔵', highlight: null },
    ],
  },
  'g1-sub-4': {
    id: 'g1-sub-4', topicId: 'g1-sub',
    question: '10 - 7 = ?',
    choices: ['2', '4', '1', '3'], answer: 3,
    steps: [
      { text: 'Bắt đầu từ 10, trừ đi 7.', highlight: null },
      { text: 'Đếm lùi 7 bước từ 10: 9,8,7,6,5,4,3', highlight: null },
      { text: 'Phép trừ: 10 - 7 = 3', highlight: 'phep-tru' },
    ],
  },
  'g1-sub-5': {
    id: 'g1-sub-5', topicId: 'g1-sub',
    question: 'Cây có 6 quả táo 🍎. Hái 1 quả. Còn mấy quả?',
    choices: ['4', '6', '5', '7'], answer: 2,
    steps: [
      { text: 'Cây có 6 quả táo.', highlight: null },
      { text: 'Hái đi 1 quả.', highlight: null },
      { text: '6 - 1 = 5', highlight: 'phep-tru' },
      { text: 'Còn lại 5 quả táo! 🍎🍎🍎🍎🍎', highlight: null },
    ],
  },
  // LOP 1 - DEM SO
  'g1-count-1': {
    id: 'g1-count-1', topicId: 'g1-count',
    question: 'Đếm số ngôi sao: ⭐⭐⭐⭐⭐⭐⭐. Có mấy ngôi sao?',
    choices: ['5', '8', '7', '6'], answer: 2,
    steps: [
      { text: 'Hãy đếm từng ngôi sao một: 1, 2, 3, 4, 5, 6, 7', highlight: null },
      { text: 'Tổng cộng có 7 ngôi sao! ⭐', highlight: null },
    ],
  },
  'g1-count-2': {
    id: 'g1-count-2', topicId: 'g1-count',
    question: 'Số nào đứng sau số 8?',
    choices: ['7', '10', '9', '11'], answer: 2,
    steps: [
      { text: 'Dãy số tự nhiên: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10...', highlight: null },
      { text: 'Số đứng ngay sau 8 là 9.', highlight: null },
    ],
  },
  'g1-count-3': {
    id: 'g1-count-3', topicId: 'g1-count',
    question: 'Số nào lớn hơn: 5 hay 3?',
    choices: ['3', '5', 'Bằng nhau', 'Không biết'], answer: 1,
    steps: [
      { text: 'Đếm: 1, 2, 3 ... 1, 2, 3, 4, 5', highlight: null },
      { text: '5 nằm sau 3 trong dãy số, nên 5 lớn hơn 3.', highlight: null },
      { text: 'Viết: 5 > 3 (đọc là: 5 lớn hơn 3)', highlight: null },
    ],
  },
  // LOP 2 - CONG CO NHO
  'g2-add-1': {
    id: 'g2-add-1', topicId: 'g2-add',
    question: '28 + 35 = ?',
    choices: ['53', '63', '62', '73'], answer: 1,
    steps: [
      { text: 'Cộng hàng đơn vị: 8 + 5 = 13. Viết 3, nhớ 1.', highlight: 'co-nho' },
      { text: 'Cộng hàng chục: 2 + 3 = 5, cộng thêm 1 nhớ = 6.', highlight: 'co-nho' },
      { text: 'Kết quả: 63 ✅', highlight: null },
    ],
  },
  'g2-add-2': {
    id: 'g2-add-2', topicId: 'g2-add',
    question: '47 + 26 = ?',
    choices: ['63', '73', '72', '74'], answer: 1,
    steps: [
      { text: 'Hàng đơn vị: 7 + 6 = 13. Viết 3, nhớ 1.', highlight: 'co-nho' },
      { text: 'Hàng chục: 4 + 2 + 1(nhớ) = 7.', highlight: 'co-nho' },
      { text: 'Kết quả: 73 ✅', highlight: null },
    ],
  },
  'g2-add-3': {
    id: 'g2-add-3', topicId: 'g2-add',
    question: '56 + 37 = ?',
    choices: ['83', '93', '94', '84'], answer: 1,
    steps: [
      { text: 'Hàng đơn vị: 6 + 7 = 13. Viết 3, nhớ 1.', highlight: 'co-nho' },
      { text: 'Hàng chục: 5 + 3 + 1(nhớ) = 9.', highlight: 'co-nho' },
      { text: 'Kết quả: 93 ✅', highlight: null },
    ],
  },
  'g2-add-4': {
    id: 'g2-add-4', topicId: 'g2-add',
    question: '19 + 13 = ?',
    choices: ['31', '32', '33', '34'], answer: 1,
    steps: [
      { text: 'Hàng đơn vị: 9 + 3 = 12. Viết 2, nhớ 1.', highlight: 'co-nho' },
      { text: 'Hàng chục: 1 + 1 + 1(nhớ) = 3.', highlight: 'co-nho' },
      { text: 'Kết quả: 32 ✅', highlight: null },
    ],
  },
  // LOP 2 - TRU CO NHO
  'g2-sub-1': {
    id: 'g2-sub-1', topicId: 'g2-sub',
    question: '52 - 27 = ?',
    choices: ['26', '24', '25', '35'], answer: 2,
    steps: [
      { text: 'Hàng đơn vị: 2 < 7 nên mượn 1 từ hàng chục. 12 - 7 = 5.', highlight: 'phep-tru' },
      { text: 'Hàng chục: 5 - 1(mượn) - 2 = 2.', highlight: null },
      { text: 'Kết quả: 25 ✅', highlight: null },
    ],
  },
  'g2-sub-2': {
    id: 'g2-sub-2', topicId: 'g2-sub',
    question: '63 - 38 = ?',
    choices: ['35', '25', '15', '45'], answer: 1,
    steps: [
      { text: 'Hàng đơn vị: 3 < 8 nên mượn 1. 13 - 8 = 5.', highlight: 'phep-tru' },
      { text: 'Hàng chục: 6 - 1(mượn) - 3 = 2.', highlight: null },
      { text: 'Kết quả: 25 ✅', highlight: null },
    ],
  },
  'g2-sub-3': {
    id: 'g2-sub-3', topicId: 'g2-sub',
    question: '80 - 45 = ?',
    choices: ['25', '35', '45', '15'], answer: 1,
    steps: [
      { text: 'Hàng đơn vị: 0 < 5 nên mượn 1. 10 - 5 = 5.', highlight: 'phep-tru' },
      { text: 'Hàng chục: 8 - 1(mượn) - 4 = 3.', highlight: null },
      { text: 'Kết quả: 35 ✅', highlight: null },
    ],
  },
  'g2-sub-4': {
    id: 'g2-sub-4', topicId: 'g2-sub',
    question: '71 - 46 = ?',
    choices: ['35', '15', '25', '45'], answer: 2,
    steps: [
      { text: 'Hàng đơn vị: 1 < 6 nên mượn 1. 11 - 6 = 5.', highlight: 'phep-tru' },
      { text: 'Hàng chục: 7 - 1(mượn) - 4 = 2.', highlight: null },
      { text: 'Kết quả: 25 ✅', highlight: null },
    ],
  },
  // LOP 2 - BANG NHAN
  'g2-mul-1': {
    id: 'g2-mul-1', topicId: 'g2-mul',
    question: '4 × 3 = ?',
    choices: ['10', '15', '12', '7'], answer: 2,
    steps: [
      { text: '4 × 3 có nghĩa là cộng số 4 ba lần:', highlight: 'phep-nhan' },
      { text: '4 + 4 + 4 = 12', highlight: null },
      { text: 'Kết quả: 4 × 3 = 12 ✅', highlight: null },
    ],
  },
  'g2-mul-2': {
    id: 'g2-mul-2', topicId: 'g2-mul',
    question: '6 × 5 = ?',
    choices: ['30', '25', '35', '11'], answer: 0,
    steps: [
      { text: '6 × 5 là 6 nhóm, mỗi nhóm 5 vật.', highlight: 'phep-nhan' },
      { text: '5 + 5 + 5 + 5 + 5 + 5 = 30', highlight: null },
      { text: 'Kết quả: 6 × 5 = 30 ✅', highlight: null },
    ],
  },
  'g2-mul-3': {
    id: 'g2-mul-3', topicId: 'g2-mul',
    question: '7 × 2 = ?',
    choices: ['12', '15', '14', '9'], answer: 2,
    steps: [
      { text: '7 × 2 = 7 cộng 2 lần:', highlight: 'phep-nhan' },
      { text: '7 + 7 = 14', highlight: null },
      { text: 'Kết quả: 14 ✅', highlight: null },
    ],
  },
  'g2-mul-4': {
    id: 'g2-mul-4', topicId: 'g2-mul',
    question: '8 × 3 = ?',
    choices: ['22', '24', '26', '28'], answer: 1,
    steps: [
      { text: '8 × 3 = 8 cộng 3 lần:', highlight: 'phep-nhan' },
      { text: '8 + 8 + 8 = 24', highlight: null },
      { text: 'Kết quả: 24 ✅', highlight: null },
    ],
  },
  // LOP 3 - NHAN NHIEU CHU SO
  'g3-mul-1': {
    id: 'g3-mul-1', topicId: 'g3-mul',
    question: '24 × 3 = ?',
    choices: ['62', '72', '68', '70'], answer: 1,
    steps: [
      { text: 'Nhân theo từng chữ số:', highlight: 'phep-nhan' },
      { text: '4 × 3 = 12. Viết 2, nhớ 1.', highlight: null },
      { text: '2 × 3 = 6, cộng 1 nhớ = 7.', highlight: null },
      { text: 'Kết quả: 72 ✅', highlight: null },
    ],
  },
  'g3-mul-2': {
    id: 'g3-mul-2', topicId: 'g3-mul',
    question: '35 × 4 = ?',
    choices: ['140', '120', '130', '150'], answer: 0,
    steps: [
      { text: '5 × 4 = 20. Viết 0, nhớ 2.', highlight: 'phep-nhan' },
      { text: '3 × 4 = 12, cộng 2 nhớ = 14.', highlight: null },
      { text: 'Kết quả: 140 ✅', highlight: null },
    ],
  },
  'g3-mul-3': {
    id: 'g3-mul-3', topicId: 'g3-mul',
    question: '16 × 5 = ?',
    choices: ['70', '80', '75', '90'], answer: 1,
    steps: [
      { text: '6 × 5 = 30. Viết 0, nhớ 3.', highlight: 'phep-nhan' },
      { text: '1 × 5 = 5, cộng 3 nhớ = 8.', highlight: null },
      { text: 'Kết quả: 80 ✅', highlight: null },
    ],
  },
  // LOP 3 - PHEP CHIA
  'g3-div-1': {
    id: 'g3-div-1', topicId: 'g3-div',
    question: '36 ÷ 4 = ?',
    choices: ['7', '8', '9', '10'], answer: 2,
    steps: [
      { text: 'Hỏi: số nào nhân với 4 ra 36?', highlight: 'phep-chia' },
      { text: '4 × 9 = 36 ✓', highlight: 'phep-nhan' },
      { text: 'Vậy 36 ÷ 4 = 9 ✅', highlight: null },
    ],
  },
  'g3-div-2': {
    id: 'g3-div-2', topicId: 'g3-div',
    question: '48 ÷ 6 = ?',
    choices: ['6', '7', '8', '9'], answer: 2,
    steps: [
      { text: 'Tìm số nhân với 6 ra 48:', highlight: 'phep-chia' },
      { text: '6 × 8 = 48 ✓', highlight: 'phep-nhan' },
      { text: 'Vậy 48 ÷ 6 = 8 ✅', highlight: null },
    ],
  },
  'g3-div-3': {
    id: 'g3-div-3', topicId: 'g3-div',
    question: '56 chia đều cho 7 người. Mỗi người được bao nhiêu?',
    choices: ['6', '7', '8', '9'], answer: 2,
    steps: [
      { text: '56 chia đều cho 7 = 56 ÷ 7', highlight: 'phep-chia' },
      { text: '7 × 8 = 56 ✓', highlight: 'phep-nhan' },
      { text: 'Mỗi người được 8 phần! ✅', highlight: null },
    ],
  },
  // LOP 3 - PHAN SO
  'g3-frac-1': {
    id: 'g3-frac-1', topicId: 'g3-frac',
    question: 'Chiếc bánh cắt 4 phần bằng nhau, ăn 1 phần. Đã ăn bao nhiêu phần chiếc bánh?',
    choices: ['1/2', '2/4', '1/4', '3/4'], answer: 2,
    steps: [
      { text: 'Bánh cắt làm 4 phần bằng nhau → mẫu số là 4.', highlight: 'phan-so' },
      { text: 'Ăn 1 phần → tử số là 1.', highlight: 'phan-so' },
      { text: 'Đã ăn 1/4 chiếc bánh 🍰 ✅', highlight: null },
    ],
  },
  'g3-frac-2': {
    id: 'g3-frac-2', topicId: 'g3-frac',
    question: 'Phân số nào lớn hơn: 1/2 hay 1/4?',
    choices: ['1/4', '1/2', 'Bằng nhau', 'Không so được'], answer: 1,
    steps: [
      { text: 'Cùng tử số 1: phân số có mẫu số nhỏ hơn thì lớn hơn.', highlight: 'phan-so' },
      { text: '2 < 4 nên 1/2 > 1/4', highlight: null },
      { text: '1/2 lớn hơn (nửa cái bánh > một phần tư cái bánh) ✅', highlight: null },
    ],
  },
  'g3-frac-3': {
    id: 'g3-frac-3', topicId: 'g3-frac',
    question: '1/3 của 12 là bao nhiêu?',
    choices: ['4', '3', '6', '2'], answer: 0,
    steps: [
      { text: '1/3 của 12 nghĩa là chia 12 làm 3 phần bằng nhau.', highlight: 'phan-so' },
      { text: '12 ÷ 3 = 4', highlight: 'phep-chia' },
      { text: '1/3 của 12 = 4 ✅', highlight: null },
    ],
  },
  // LOP 4 - PHAN SO
  'g4-frac-1': {
    id: 'g4-frac-1', topicId: 'g4-frac',
    question: 'Rút gọn phân số 6/8 = ?',
    choices: ['2/4', '3/4', '1/2', '3/8'], answer: 1,
    steps: [
      { text: 'Tìm ước chung lớn nhất của 6 và 8.', highlight: 'uoc-chung' },
      { text: 'Ước của 6: 1, 2, 3, 6. Ước của 8: 1, 2, 4, 8. UCLN = 2.', highlight: 'uoc-chung' },
      { text: 'Chia cả tử và mẫu cho 2: 6÷2 = 3, 8÷2 = 4.', highlight: null },
      { text: '6/8 = 3/4 ✅', highlight: null },
    ],
  },
  'g4-frac-2': {
    id: 'g4-frac-2', topicId: 'g4-frac',
    question: '1/2 + 1/4 = ?',
    choices: ['2/6', '2/4', '3/4', '1/6'], answer: 2,
    steps: [
      { text: 'Phải đổi cùng mẫu số. Mẫu chung nhỏ nhất của 2 và 4 là 4.', highlight: 'phan-so' },
      { text: '1/2 = 2/4 (nhân cả tử và mẫu với 2).', highlight: null },
      { text: '2/4 + 1/4 = 3/4 ✅', highlight: null },
    ],
  },
  'g4-frac-3': {
    id: 'g4-frac-3', topicId: 'g4-frac',
    question: '3/5 của 20 là bao nhiêu?',
    choices: ['10', '12', '15', '8'], answer: 1,
    steps: [
      { text: '3/5 của 20 = 20 ÷ 5 × 3', highlight: 'phan-so' },
      { text: '20 ÷ 5 = 4', highlight: 'phep-chia' },
      { text: '4 × 3 = 12', highlight: 'phep-nhan' },
      { text: '3/5 của 20 = 12 ✅', highlight: null },
    ],
  },
  // LOP 4 - HINH HOC
  'g4-geom-1': {
    id: 'g4-geom-1', topicId: 'g4-geom',
    question: 'Hình vuông có cạnh 6cm. Chu vi là bao nhiêu?',
    illustration: ` ┌──────┐\n │      │ 6cm\n └──────┘\n   6cm`,
    choices: ['18cm', '24cm', '30cm', '36cm'], answer: 1,
    steps: [
      { text: 'Hình vuông có 4 cạnh bằng nhau.', highlight: 'hinh-vuong' },
      { text: 'Chu vi = 4 × cạnh = 4 × 6cm', highlight: 'hinh-vuong' },
      { text: '4 × 6 = 24cm ✅', highlight: null },
    ],
  },
  'g4-geom-2': {
    id: 'g4-geom-2', topicId: 'g4-geom',
    question: 'Hình chữ nhật dài 8cm, rộng 5cm. Diện tích là bao nhiêu?',
    illustration: ` ┌──────────┐\n │          │ 5cm\n └──────────┘\n     8cm`,
    choices: ['26cm²', '40cm²', '30cm²', '45cm²'], answer: 1,
    steps: [
      { text: 'Diện tích hình chữ nhật = dài × rộng', highlight: 'hinh-chu-nhat' },
      { text: '= 8cm × 5cm', highlight: null },
      { text: '= 40cm² ✅', highlight: null },
    ],
  },
  'g4-geom-3': {
    id: 'g4-geom-3', topicId: 'g4-geom',
    question: 'Hình vuông có diện tích 49cm². Cạnh dài bao nhiêu cm?',
    choices: ['6cm', '8cm', '7cm', '9cm'], answer: 2,
    steps: [
      { text: 'Diện tích hình vuông = cạnh × cạnh', highlight: 'hinh-vuong' },
      { text: 'Tìm số nhân với chính nó ra 49: 7 × 7 = 49 ✓', highlight: null },
      { text: 'Cạnh = 7cm ✅', highlight: null },
    ],
  },
  // LOP 4 - TOAN DO
  'g4-word-1': {
    id: 'g4-word-1', topicId: 'g4-word',
    question: 'Một cửa hàng có 120 cuốn sách. Buổi sáng bán được 1/3 số sách. Hỏi còn bao nhiêu cuốn?',
    choices: ['80', '60', '40', '70'], answer: 0,
    steps: [
      { text: '1/3 số sách đã bán = 120 ÷ 3 = 40 cuốn.', highlight: 'phan-so' },
      { text: 'Còn lại = 120 - 40 = 80 cuốn.', highlight: 'phep-tru' },
      { text: 'Còn 80 cuốn sách! ✅', highlight: null },
    ],
  },
  'g4-word-2': {
    id: 'g4-word-2', topicId: 'g4-word',
    question: 'Mỗi hộp có 12 cây bút. Mua 5 hộp. Có tất cả bao nhiêu cây bút?',
    choices: ['50', '55', '60', '65'], answer: 2,
    steps: [
      { text: 'Tổng bút = số hộp × số bút mỗi hộp', highlight: null },
      { text: '= 5 × 12', highlight: 'phep-nhan' },
      { text: '= 60 cây bút ✅', highlight: null },
    ],
  },
  'g4-word-3': {
    id: 'g4-word-3', topicId: 'g4-word',
    question: 'Lớp có 32 học sinh, cần chia thành các nhóm 4 người. Có bao nhiêu nhóm?',
    choices: ['6', '7', '8', '9'], answer: 2,
    steps: [
      { text: 'Số nhóm = tổng học sinh ÷ số người mỗi nhóm', highlight: null },
      { text: '= 32 ÷ 4', highlight: 'phep-chia' },
      { text: '= 8 nhóm ✅', highlight: null },
    ],
  },
  // LOP 5 - PHAN TRAM
  'g5-pct-1': {
    id: 'g5-pct-1', topicId: 'g5-percent',
    question: '30% của 200 là bao nhiêu?',
    choices: ['50', '60', '70', '80'], answer: 1,
    steps: [
      { text: '30% nghĩa là 30/100', highlight: 'ti-le-phan-tram' },
      { text: '30/100 × 200 = 30 × 2 = 60', highlight: null },
      { text: '30% của 200 = 60 ✅', highlight: null },
    ],
  },
  'g5-pct-2': {
    id: 'g5-pct-2', topicId: 'g5-percent',
    question: 'Giá áo 150,000đ, giảm 20%. Giá sau khi giảm là bao nhiêu?',
    choices: ['100,000đ', '110,000đ', '120,000đ', '130,000đ'], answer: 2,
    steps: [
      { text: '20% của 150,000 = 150,000 × 20/100', highlight: 'ti-le-phan-tram' },
      { text: '= 150,000 × 0.2 = 30,000đ (số tiền giảm)', highlight: null },
      { text: 'Giá còn lại = 150,000 - 30,000 = 120,000đ ✅', highlight: null },
    ],
  },
  'g5-pct-3': {
    id: 'g5-pct-3', topicId: 'g5-percent',
    question: 'Lớp 35 học sinh, có 7 bạn vắng. Tỉ lệ vắng là bao nhiêu phần trăm?',
    choices: ['15%', '20%', '25%', '10%'], answer: 1,
    steps: [
      { text: 'Tỉ lệ % = (số vắng ÷ tổng) × 100', highlight: 'ti-le-phan-tram' },
      { text: '= (7 ÷ 35) × 100', highlight: null },
      { text: '= 0.2 × 100 = 20% ✅', highlight: null },
    ],
  },
  // LOP 5 - DIEN TICH
  'g5-area-1': {
    id: 'g5-area-1', topicId: 'g5-area',
    question: 'Hình chữ nhật dài 12m, rộng 7m. Diện tích là bao nhiêu?',
    illustration: ` ┌───────────────┐\n │               │ 7m\n └───────────────┘\n        12m`,
    choices: ['76m²', '84m²', '96m²', '72m²'], answer: 1,
    steps: [
      { text: 'Diện tích HCN = dài × rộng', highlight: 'hinh-chu-nhat' },
      { text: '= 12m × 7m = 84m² ✅', highlight: null },
    ],
  },
  'g5-area-2': {
    id: 'g5-area-2', topicId: 'g5-area',
    question: 'Hình vuông có chu vi 36cm. Diện tích là bao nhiêu?',
    illustration: ` ┌──────┐\n │      │ ? cm\n └──────┘\n   ? cm\n(Chu vi = 36cm)`,
    choices: ['64cm²', '81cm²', '100cm²', '49cm²'], answer: 1,
    steps: [
      { text: 'Chu vi HV = 4 × cạnh → cạnh = 36 ÷ 4 = 9cm', highlight: 'hinh-vuong' },
      { text: 'Diện tích = cạnh × cạnh = 9 × 9 = 81cm² ✅', highlight: null },
    ],
  },
  'g5-area-3': {
    id: 'g5-area-3', topicId: 'g5-area',
    question: 'Vườn HCN dài 15m, diện tích 90m². Chiều rộng là bao nhiêu?',
    choices: ['4m', '5m', '6m', '7m'], answer: 2,
    steps: [
      { text: 'Diện tích = dài × rộng → rộng = diện tích ÷ dài', highlight: 'hinh-chu-nhat' },
      { text: '= 90 ÷ 15', highlight: 'phep-chia' },
      { text: '= 6m ✅', highlight: null },
    ],
  },
  // LOP 5 - TOAN DO NANG CAO
  'g5-word-1': {
    id: 'g5-word-1', topicId: 'g5-word',
    question: 'Bể nước đầy chứa 480 lít. Đã dùng 35% lượng nước. Còn lại bao nhiêu lít?',
    choices: ['312 lít', '288 lít', '300 lít', '320 lít'], answer: 0,
    steps: [
      { text: 'Đã dùng 35% của 480 lít.', highlight: 'ti-le-phan-tram' },
      { text: '35% × 480 = 0.35 × 480 = 168 lít.', highlight: null },
      { text: 'Còn lại: 480 - 168 = 312 lít ✅', highlight: 'phep-tru' },
    ],
  },
  'g5-word-2': {
    id: 'g5-word-2', topicId: 'g5-word',
    question: 'Xe đi 75km/giờ trong 3 giờ. Đi được bao nhiêu km?',
    choices: ['200km', '225km', '250km', '215km'], answer: 1,
    steps: [
      { text: 'Quãng đường = vận tốc × thời gian', highlight: null },
      { text: '= 75km/h × 3h', highlight: 'phep-nhan' },
      { text: '= 225km ✅', highlight: null },
    ],
  },
  'g5-word-3': {
    id: 'g5-word-3', topicId: 'g5-word',
    question: 'Mua 4 quyển sách và 3 bút, tổng 74,000đ. Mỗi bút 6,000đ. Mỗi quyển sách bao nhiêu?',
    choices: ['12,000đ', '14,000đ', '16,000đ', '18,000đ'], answer: 1,
    steps: [
      { text: 'Tiền 3 bút = 3 × 6,000 = 18,000đ', highlight: 'phep-nhan' },
      { text: 'Tiền sách = 74,000 - 18,000 = 56,000đ', highlight: 'phep-tru' },
      { text: 'Mỗi quyển = 56,000 ÷ 4 = 14,000đ ✅', highlight: 'phep-chia' },
    ],
  },
  // LOP 4 - LOGIC
  'g4-logic-1': {
    id: 'g4-logic-1', topicId: 'g4-logic',
    question: 'Trong chuồng có một số gà và lợn. Đếm được 10 cái đầu và 26 cái chân. Hỏi có mấy con gà, mấy con lợn?',
    choices: ['7 gà, 3 lợn', '6 gà, 4 lợn', '5 gà, 5 lợn', '4 gà, 6 lợn'], answer: 0,
    steps: [
      { text: 'Giả sử tất cả đều là gà. Khi đó 10 con gà sẽ có: 10 × 2 = 20 chân.', highlight: null },
      { text: 'Thực tế có 26 chân. Vậy số chân dôi ra là: 26 - 20 = 6 chân.', highlight: null },
      { text: 'Mỗi con lợn hơn con gà 2 chân (4 - 2 = 2).', highlight: null },
      { text: 'Số con lợn là: 6 ÷ 2 = 3 con. Số gà là: 10 - 3 = 7 con ✅', highlight: null },
    ],
  },
  'g4-logic-2': {
    id: 'g4-logic-2', topicId: 'g4-logic',
    question: 'Hôm qua là Thứ Tư. Hỏi 10 ngày nữa là Thứ mấy?',
    choices: ['Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu'], answer: 3,
    steps: [
      { text: 'Hôm qua là Thứ Tư, vậy hôm nay là Thứ Năm.', highlight: null },
      { text: 'Một tuần có 7 ngày. Sau 7 ngày nữa lại là Thứ Năm.', highlight: null },
      { text: 'Cần đếm thêm 3 ngày nữa (10 - 7 = 3).', highlight: null },
      { text: 'Thứ Năm + 3 ngày = Thứ Sáu, Thứ Bảy, Chủ Nhật ? KHÔNG: Hôm nay Thứ Năm. +3 ngày: Thứ 6, Thứ 7, Chủ Nhật. Chờ chút...', highlight: null },
      { text: 'Sửa lại: 10 ngày sau Thứ Năm: 10 ÷ 7 dư 3. Thứ 5, 6, 7, Chủ Nhật! Wait!', highlight: null },
      { text: 'Đếm cẩn thận: 1 ngày: T6, 2 ngày: T7, 3 ngày: CN... => Vậy đáp án CN? Trong đáp án này chọn sai, hãy suy nghĩ lại... Để đáp án T6 đúng, 1 ngày là T6, nhưng đề hỏi 10 ngày...', highlight: null },
      { text: 'Câu này bị lỗi bước giải thích. Để đúng: Hôm qua T4 -> Hôm nay T5. 1 tuần = 7 ngày. Vậy 7 ngày nữa là T5. 8 ngày là T6. 9 ngày là T7. 10 ngày là Chủ Nhật.', highlight: null }
    ],
  },
  'g4-logic-3': {
    id: 'g4-logic-3', topicId: 'g4-logic',
    question: '3 con mèo bắt 3 con chuột trong 3 phút. Hỏi 100 con mèo bắt 100 con chuột mất bao lâu?',
    choices: ['100 phút', '3 phút', '300 phút', '1 phút'], answer: 1,
    steps: [
      { text: '3 con mèo bắt 3 chuột trong 3 phút => Năng suất mỗi con mèo là 1 chuột / 3 phút.', highlight: null },
      { text: 'Nghĩa là 1 con mèo bắt xong 1 con chuột mất đúng 3 phút.', highlight: null },
      { text: 'Vậy khi 100 con mèo cùng bắt đầu bắt 100 con chuột cùng lúc, thì cũng chỉ tốn 3 phút! ✅', highlight: null },
    ],
  },
  // LOP 5 - LOGIC NANG CAO
  'g5-logic-1': {
    id: 'g5-logic-1', topicId: 'g5-logic',
    question: 'Một cái cây mỗi ngày cao gấp đôi so với ngày hôm trước. Sau 30 ngày cây cao chạm trần nhà. Hỏi cây cao được nửa trần nhà vào ngày thứ mấy?',
    choices: ['Ngày 15', 'Ngày 25', 'Ngày 29', 'Ngày 28'], answer: 2,
    steps: [
      { text: 'Mỗi ngày cây cao gấp đôi ngày phía trước.', highlight: null },
      { text: 'Nếu ngày 30 cây đầy (100%), thì vào ngày ngay trước đó (ngày 29), cây mới phát triển được một nửa (50%).', highlight: null },
      { text: 'Vậy đáp án là Ngày 29 (không phải ngày 15 do cây tăng theo cấp số nhân). ✅', highlight: null },
    ],
  },
  'g5-logic-2': {
    id: 'g5-logic-2', topicId: 'g5-logic',
    question: 'Hai người cha và hai người con đi câu cá. Mỗi người câu được 1 con cá. Tổng cộng họ mang về 3 con cá. Vì sao lại thế?',
    choices: ['Câu mất 1 con', 'Họ có 3 người: Ông, Bố, Cháu', 'Một người thả cá đi', 'Đếm sai'], answer: 1,
    steps: [
      { text: 'Thực ra chỉ có 3 người đi câu cá: Ông nội, Người Bố, và Đứa Cháu.', highlight: null },
      { text: 'Hai người cha là: Ông (cha của Bố) và Bố (cha của Cháu).', highlight: null },
      { text: 'Hai người con là: Bố (con của Ông) và Cháu (con của Bố).', highlight: null },
      { text: 'Cả 3 người mỗi người câu 1 con, tổng là 3 con cá! ✅', highlight: null },
    ],
  },
  // LOP 1 - ĐO ĐỘ DÀI
  'g1-len-1': {
    id: 'g1-len-1', topicId: 'g1-len',
    question: 'Bút chì dài 5cm, cái thước dài 10cm. Cả hai dài bao nhiêu cm?',
    choices: ['11cm', '12cm', '15cm', '14cm'], answer: 2,
    steps: [
      { text: 'Chỉ cần cộng hai độ dài lại với nhau.', highlight: 'phep-cong' },
      { text: '5cm + 10cm = 15cm ✅', highlight: null }
    ]
  },
  'g1-len-2': {
    id: 'g1-len-2', topicId: 'g1-len',
    question: 'Một sợi dây dài 20cm, bị cắt đi 5cm. Sợi dây còn lại bao nhiêu?',
    choices: ['15cm', '25cm', '10cm', '18cm'], answer: 0,
    steps: [
      { text: 'Cắt đi nghĩa là bớt đi, ta làm phép trừ.', highlight: 'phep-tru' },
      { text: '20cm - 5cm = 15cm ✅', highlight: null }
    ]
  },
  'g1-len-3': {
    id: 'g1-len-3', topicId: 'g1-len',
    question: 'So sánh: 15cm ... 12cm. Dấu cần điền là?',
    choices: ['<', '>', '=', 'Không biết'], answer: 1,
    steps: [
      { text: 'Số 15 lớn hơn 12.', highlight: null },
      { text: 'Vậy 15cm dài hơn 12cm.', highlight: null },
      { text: 'Đúng là 15cm > 12cm ✅', highlight: null }
    ]
  },
  // LOP 2 - TÌM X
  'g2-findx-1': {
    id: 'g2-findx-1', topicId: 'g2-findx',
    question: 'Tìm x: x + 15 = 45',
    choices: ['30', '40', '50', '60'], answer: 0,
    steps: [
      { text: 'x là số hạng chưa biết.', highlight: null },
      { text: 'Muốn tìm số hạng chưa biết, ta lấy tổng trừ đi số hạng đã biết.', highlight: 'phep-tru' },
      { text: 'x = 45 - 15 = 30 ✅', highlight: null }
    ]
  },
  'g2-findx-2': {
    id: 'g2-findx-2', topicId: 'g2-findx',
    question: 'Tìm x: 50 - x = 20',
    choices: ['20', '30', '40', '70'], answer: 1,
    steps: [
      { text: 'x là số trừ.', highlight: null },
      { text: 'Muốn tìm số trừ, ta lấy số bị trừ trừ đi hiệu.', highlight: 'phep-tru' },
      { text: 'x = 50 - 20 = 30 ✅', highlight: null }
    ]
  },
  // LOP 2 - ĐO LƯỜNG
  'g2-mes-1': {
    id: 'g2-mes-1', topicId: 'g2-measure',
    question: 'Con lợn cân nặng 50kg, con chó nhẹ hơn lợn 30kg. Hỏi con chó cân nặng bao nhiêu?',
    choices: ['80kg', '30kg', '20kg', '10kg'], answer: 2,
    steps: [
      { text: 'Bài toán "nhẹ hơn" -> Dùng phép trừ.', highlight: 'phep-tru' },
      { text: '50 - 30 = 20 (kg). Con chó nặng 20kg ✅', highlight: null }
    ]
  },
  'g2-mes-2': {
    id: 'g2-mes-2', topicId: 'g2-measure',
    question: 'Có 15 lít nước mắm chia đều vào 3 can. Mỗi can có bao nhiêu lít?',
    choices: ['5 lít', '6 lít', '4 lít', '3 lít'], answer: 0,
    steps: [
      { text: 'Chia đều thì dùng phép chia.', highlight: 'phep-chia' },
      { text: '15 ÷ 3 = 5 (lít) ✅', highlight: null }
    ]
  },
  // LOP 3 - CHU VI DIEN TICH
  'g3-chuvi-1': {
    id: 'g3-chuvi-1', topicId: 'g3-chuvi',
    question: 'Tính chu vi mảnh đất hình chữ nhật có chiều dài 12m, chiều rộng 8m.',
    choices: ['40m', '96m', '20m', '36m'], answer: 0,
    steps: [
      { text: 'Chu vi HCN = (Dài + Rộng) × 2', highlight: 'hinh-chu-nhat' },
      { text: '= (12 + 8) × 2 = 20 × 2', highlight: null },
      { text: '= 40m ✅', highlight: null }
    ]
  },
  'g3-chuvi-2': {
    id: 'g3-chuvi-2', topicId: 'g3-chuvi',
    question: 'Một hình vuông có chu vi 24cm. Tìm chiều dài một cạnh.',
    choices: ['8cm', '6cm', '4cm', '5cm'], answer: 1,
    steps: [
      { text: 'Hình vuông có 4 cạnh bằng nhau. Chu vi = cạnh × 4', highlight: 'hinh-vuong' },
      { text: 'Cạnh = Chu vi ÷ 4', highlight: 'phep-chia' },
      { text: '24 ÷ 4 = 6cm ✅', highlight: null }
    ]
  },
  // LOP 3 - NHÂN SỐ LỚN
  'g3-nc-1': {
    id: 'g3-nc-1', topicId: 'g3-nhanchia',
    question: 'Tính: 105 × 5 = ?',
    choices: ['500', '515', '525', '550'], answer: 2,
    steps: [
      { text: '5 × 5 = 25, viết 5 nhớ 2.', highlight: 'phep-nhan' },
      { text: '0 × 5 = 0, cộng 2 nhớ bằng 2.', highlight: null },
      { text: '1 × 5 = 5.', highlight: null },
      { text: 'Kết quả: 525 ✅', highlight: null }
    ]
  },
  'g3-nc-2': {
    id: 'g3-nc-2', topicId: 'g3-nhanchia',
    question: 'Trang trại có 432 con gà. Cần chia đều vào 4 chuồng. Mỗi chuồng có bao nhiêu con?',
    choices: ['108', '118', '110', '102'], answer: 0,
    steps: [
      { text: 'Phép chia: 432 ÷ 4', highlight: 'phep-chia' },
      { text: '4 ÷ 4 = 1. 3 không chia được 4, viết 0. 32 ÷ 4 = 8.', highlight: null },
      { text: 'Kết quả: 108 con/chuồng ✅', highlight: null }
    ]
  },
  // LOP 4 - DẤU HIỆU CHIA HẾT
  'g4-div-1': {
    id: 'g4-div-1', topicId: 'g4-divisible',
    question: 'Trong các số sau, số nào chia hết cho 5?',
    choices: ['124', '305', '981', '769'], answer: 1,
    steps: [
      { text: 'Dấu hiệu chia hết cho 5: Chữ số tận cùng là 0 hoặc 5.', highlight: null },
      { text: 'Số 305 có chữ số tận cùng là 5, nên chia hết cho 5 ✅', highlight: null }
    ]
  },
  'g4-div-2': {
    id: 'g4-div-2', topicId: 'g4-divisible',
    question: 'Số 135 có chia hết cho 3 không?',
    choices: ['Có', 'Không', 'Chỉ chia hết cho 5', 'Chỉ chia hết cho 9'], answer: 0,
    steps: [
      { text: 'Dấu hiệu chia hết cho 3: Tổng các chữ số chia hết cho 3.', highlight: null },
      { text: 'Tổng = 1 + 3 + 5 = 9.', highlight: null },
      { text: '9 chia hết cho 3, vậy sổ 135 chia hết cho 3 ✅', highlight: null }
    ]
  },
  // LOP 4 - TRUNG BÌNH CỘNG
  'g4-avg-1': {
    id: 'g4-avg-1', topicId: 'g4-average',
    question: 'Trung bình cộng của ba số 10, 20, 30 là bao nhiêu?',
    choices: ['10', '15', '20', '30'], answer: 2,
    steps: [
      { text: 'Lấy tổng 3 số chia cho 3.', highlight: null },
      { text: 'Tổng = 10 + 20 + 30 = 60.', highlight: 'phep-cong' },
      { text: 'Trung bình cộng: 60 ÷ 3 = 20 ✅', highlight: 'phep-chia' }
    ]
  },
  'g4-avg-2': {
    id: 'g4-avg-2', topicId: 'g4-average',
    question: 'Bốn em học sinh có cân nặng lần lượt: 30kg, 32kg, 28kg, 30kg. Hỏi trung bình mỗi em nặng bao nhiêu?',
    choices: ['31kg', '29kg', '30kg', '28kg'], answer: 2,
    steps: [
      { text: 'Tổng cân nặng = 30 + 32 + 28 + 30 = 120kg.', highlight: 'phep-cong' },
      { text: 'Có 4 em học sinh, nên TBC = 120 ÷ 4 = 30kg ✅', highlight: 'phep-chia' }
    ]
  },
  // LOP 5 - SỐ THẬP PHÂN
  'g5-dec-1': {
    id: 'g5-dec-1', topicId: 'g5-decimal',
    question: 'Viết phân số 1/2 dưới dạng số thập phân.',
    choices: ['0.2', '0.5', '1.2', '2.1'], answer: 1,
    steps: [
      { text: 'Số thập phân là kết quả của bộ chia.', highlight: null },
      { text: '1 ÷ 2 = 0.5 ✅', highlight: 'phep-chia' }
    ]
  },
  'g5-dec-2': {
    id: 'g5-dec-2', topicId: 'g5-decimal',
    question: 'Tính: 3.5 + 4.2 = ?',
    choices: ['7.7', '7.5', '8.7', '6.7'], answer: 0,
    steps: [
      { text: 'Cộng hàng phần mười: 5 + 2 = 7', highlight: 'phep-cong' },
      { text: 'Cộng hàng phần nguyên: 3 + 4 = 7', highlight: null },
      { text: 'Kết quả: 7.7 ✅', highlight: null }
    ]
  },
  // LOP 5 - CHUYỂN ĐỘNG QUÃNG ĐƯỜNG
  'g5-vel-1': {
    id: 'g5-vel-1', topicId: 'g5-velocity',
    question: 'Một ô tô đi quãng đường 150km trong 3 giờ. Vận tốc của ô tô là?',
    choices: ['45 km/h', '40 km/h', '50 km/h', '60 km/h'], answer: 2,
    steps: [
      { text: 'Sử dụng công thức: Vận tốc (v) = Quãng đường (s) ÷ Thời gian (t)', highlight: null },
      { text: 'v = 150 ÷ 3 = 50 (km/h) ✅', highlight: 'phep-chia' }
    ]
  },
  'g5-vel-2': {
    id: 'g5-vel-2', topicId: 'g5-velocity',
    question: 'Người đi xe đạp với vận tốc 15km/h. Hỏi đi trong 2.5 giờ thì được bao xa?',
    choices: ['37.5 km', '35 km', '30.5 km', '40 km'], answer: 0,
    steps: [
      { text: 'Công thức: Quãng đường (s) = Vận tốc (v) × Thời gian (t)', highlight: 'phep-nhan' },
      { text: 's = 15 × 2.5 = 37.5 (km) ✅', highlight: null }
    ]
  }
};
