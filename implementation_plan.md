# Kế hoạch triển khai ứng dụng Học Toán cho Trẻ em

Mô tả: Xây dựng một ứng dụng web (sử dụng HTML, CSS và JS thuần do máy chưa dùng Node.js) giúp trẻ em học toán bằng tiếng Việt. Ứng dụng được chia trình độ theo các lớp, cung cấp các bài toán, hướng dẫn giải và liên kết kiến thức để trẻ tự tìm hiểu khi gặp khó khăn. Giao diện được thiết kế sinh động, rực rỡ, tích hợp hiệu ứng vui nhộn (micro-animations) để thân thiện với trẻ em.

## User Review Required
> [!IMPORTANT]
> Chú ý: Do máy tính của bạn hiện không cài đặt thư viện phần mềm Node.js, nên tôi sẽ xây dựng ứng dụng theo kiến trúc HTML/JS/CSS thuần (nhưng vẫn tổ chức code gọn sạch và có đầy đủ tính năng).
> Các hiệu ứng animation sẽ được tôi code thủ công mượt mà thay vì dùng các bộ thư viện có sẵn.

## Proposed Changes

### Core Setup
Xây dựng dự án tại thư mục: `c:\Users\Admin\.gemini\antigravity\playground\nodal-event`

### Data Layer
#### [NEW] js/data/mockData.js
Chứa mock data bao gồm các Grade, Topic, Problem, và Knowledge.

### UI Components (Thân thiện với trẻ)
#### [NEW] index.html
Trang chủ ứng dụng (Single Page Application).
#### [NEW] css/styles.css
Thiết lập hệ thống design token với màu sắc tươi sáng, phông chữ to rõ và các class hoạt ảnh.
#### [NEW] js/app.js
Điều khiển logic đổi view của ứng dụng (Routing nội bộ).
#### [NEW] js/components/Home.js
Trang chủ chọn cấp độ.
#### [NEW] js/components/Topics.js
Trang hiển thị chủ đề học.
#### [NEW] js/components/ProblemViewer.js
Giao diện làm bài tập. Tại dòng thông báo giải thích kết quả, các từ khóa học thuật được bôi đậm (Ví dụ: "Phép cộng có nhớ").
#### [NEW] js/components/KnowledgeModal.js
Hộp thoại dễ thương hiện lên định nghĩa dễ hiểu (tra cứu kiến thức toán học bằng tooltip/modal).

## Verification Plan
1. Trực tiếp mở file `index.html` trên trình duyệt.
2. Kiểm tra thao tác (Click chọn Lớp -> Chọn Chủ đề -> Làm bài toán).
3. Cố tình nhập sai để xem hướng dẫn giải.
4. Bấm vào từ khóa để mở KnowledgeModal xác minh luồng tra cứu kiến thức.
5. Đảm bảo giao diện thu hút trẻ nhỏ về mặt thẩm mỹ.
