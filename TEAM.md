# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `Thd`
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-Thd-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): `S1`.

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Đỗ Minh Thành | 2A202603793 | Kỹ sư cổng, Sản phẩm và kinh doanh, Vận hành và pháp lý | Có |
|   2 |           |      |     |             |
|   3 |           |      |     |             |
|   4 |           |      |     |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## DoMinhThanh-2A202603793

### Phần việc phụ trách

Một thành viên đảm nhiệm cả ba vai. Phạm vi gồm tiêu chí ở Phiếu A, đánh giá và cổng phòng ngừa ở Phiếu B, phân tích sự cố và quyết định Gate 1 ở Phiếu C.

### Đóng góp cụ thể

Chọn PRD v1.1 và eval card từ bài nộp Lab 9 của mình. Dùng Codex để đọc đề và code, đề xuất tiêu chí, config và quyết định, viết cổng và monitor, soạn ba phiếu, chạy đánh giá và đẩy bài.

### Bằng chứng

Nguồn tham chiếu Lab 9 và căn cứ các ngưỡng nằm ở Phiếu A. Tiêu chí ký ở `2c811cd`. Bộ nền `R-base-before-20261120-094252-b45eeb`, bản chốt `bece49b4` và lần đo `R-base-prepared-20261120-094844-ccb9d2` được dẫn trong Phiếu B (commit vòng 1 `600cdd1`). Thẻ S1 nhập ở `467f41e`, kiểm cuối bằng `R-S1-grade-20261120-095312-025d0b`, dẫn ở C12.

### Exit ticket

Điều rút ra từ trace là kiểm đúng độ trễ vẫn có thể ghi quá thẩm quyền nếu thiếu bộ đếm lỗi theo ngày. Điều cần kiểm tiếp là hai worker có cùng vượt trần khi hãng đã có một lỗi nếu bước kiểm và ghi không nằm trong cùng giao dịch.
