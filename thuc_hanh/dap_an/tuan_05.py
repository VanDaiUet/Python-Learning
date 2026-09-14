"""Tuần 5: Set và dictionary.

Đáp án tham khảo; chỉ xem sau khi tự làm. Giữ tên biến đầu vào và đầu ra
để bộ kiểm tra tìm được. Dùng biến để tính, không chép cứng kết quả.
Sau khi đạt, sao chép sang bai_lam rồi đổi dữ liệu để thử thêm.
"""

tokens = ["ai", "python", "ai", "ml", "python", "ai"]
nhat_ky = [
    {"ten": "An", "phut": 30},
    {"ten": "Binh", "phut": 60},
    {"ten": "An", "phut": 45},
]

# Bài 1: Tạo dictionary tan_suat đếm từng token, dùng vòng lặp và dict.get().
tan_suat = {}
for token in tokens:
    tan_suat[token] = tan_suat.get(token, 0) + 1

# Bài 2: Tạo list token_duy_nhat không trùng, sắp theo thứ tự chữ cái.
token_duy_nhat = sorted(set(tokens))

# Bài 3: Tạo dictionary tong_theo_nguoi, cộng số phút của mỗi tên.
tong_theo_nguoi = {}
for ban_ghi in nhat_ky:
    ten = ban_ghi["ten"]
    tong_theo_nguoi[ten] = tong_theo_nguoi.get(ten, 0) + ban_ghi["phut"]
