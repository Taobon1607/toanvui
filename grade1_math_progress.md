# Tiến độ bổ sung bài tập Toán Lớp 1 (Lên 50 bài/chủ đề)

Tài liệu này ghi lại tiến trình thực hiện và trạng thái của các chủ đề toán Lớp 1.

## Danh sách chủ đề và trạng thái cập nhật

| ID Chủ đề | Tên chủ đề | Số bài ban đầu | Số bài hiện tại | Mục tiêu | Trạng thái |
|---|---|---|---|---|---|
| `g1-clock` | Xem Giờ | 5 | 50 | 50 | ✅ Đã hoàn thành |
| `g1-add` | Phép Cộng | 10 | 50 | 50 | ✅ Đã hoàn thành |
| `g1-sub` | Phép Trừ | 10 | 50 | 50 | ✅ Đã hoàn thành |
| `g1-count` | Đếm Số | 10 | 50 | 50 | ✅ Đã hoàn thành |
| `g1-len` | Đo Độ Dài (cm) | 10 | 50 | 50 | ✅ Đã hoàn thành |
| `g1-midterm` | Đề Kiểm Tra Giữa Kỳ | 4 | 50 | 50 | ✅ Đã hoàn thành |
| `g1-final` | Đề Kiểm Tra Cuối Kỳ | 3 | 50 | 50 | ✅ Đã hoàn thành |
| `g1-loivan` | Toán Có Lời Văn | 8 | 50 | 50 | ✅ Đã hoàn thành |
| `g1-nangcao` | Toán Nâng Cao | 7 | 50 | 50 | ✅ Đã hoàn thành |
| `g1-dem100` | Số Đếm Đến 100 | 10 | 50 | 50 | ✅ Đã hoàn thành |

**Tổng cộng bài tập hiện tại:** 500 bài tập (tăng thêm 423 bài tập chất lượng cao không trùng lặp).

## Nhật ký công việc

1. **Khởi tạo kế hoạch**: Đã khảo sát mã nguồn và lập kế hoạch sinh bài tập tự động bằng script Python.
2. **Khởi tạo file tiến độ**: Tạo file `grade1_math_progress.md` (chính là file này).
3. **Phát triển script sinh bài tập (`scripts/generate_grade1.py`)**: Thiết kế thuật toán sinh bài tập không trùng lặp và giải thích chi tiết đáp án.
4. **Chạy script sinh bài tập**: Đã sinh thêm 423 câu hỏi mới phân chia cho 10 chủ đề, cập nhật `src/data/topics.js` và `src/data/problems.js`.
5. **Xác minh & làm sạch**: Chạy code kiểm tra tính hợp lệ của JSON/JS, xác minh số lượng đạt chuẩn 50 bài/chủ đề và xóa bỏ các tệp tin tạm thời.

## Hướng dẫn tiếp tục công việc sau này

- Script sinh bài tập nằm tại: `scripts/generate_grade1.py`.
- Nếu muốn chạy lại hoặc sinh thêm, sử dụng lệnh: `python scripts/generate_grade1.py`.
- Dữ liệu bài tập nằm tại: `src/data/problems.js` và `src/data/topics.js`.
