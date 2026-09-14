"""Tuần 4: Chuỗi và list.

Đáp án tham khảo; chỉ xem sau khi tự làm. Giữ tên biến đầu vào và đầu ra
để bộ kiểm tra tìm được. Dùng biến để tính, không chép cứng kết quả.
Sau khi đạt, sao chép sang bai_lam rồi đổi dữ liệu để thử thêm.
"""

van_ban = "  Python   cho AI  "
diem_so = [9, 6, 8, 6]
tokens = ["ai", "python", "ai", "ml"]

# Bài 1: Chuẩn hóa văn bản: chữ thường, bỏ khoảng trắng đầu/cuối, giữa từ chỉ một dấu cách.
van_ban_sach = " ".join(van_ban.lower().split())

# Bài 2: Tạo list diem_dao theo thứ tự ngược; giữ diem_so nguyên vẹn.
diem_dao = diem_so[::-1]

# Bài 3: Tạo list hai token đầu tiên bằng slicing.
hai_token_dau = tokens[:2]
