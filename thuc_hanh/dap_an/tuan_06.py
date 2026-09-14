"""Bộ bài tập tuần 6: đọc đặc tả trong từng hàm trước khi viết mã."""


# Bài 1
def trung_binh(values: list[float]) -> float:
    """Trả về trung bình. List rỗng: raise ValueError.
    Ví dụ: [2, 4, 6] -> 4.0. Đầu vào là các số hữu hạn."""
    if not values:
        raise ValueError("Danh sách không được rỗng")
    return sum(values) / len(values)

# Bài 2
def chuan_hoa_diem(diem: float, toi_da: float = 10) -> float:
    """Trả về diem / toi_da. Yêu cầu toi_da > 0 và 0 <= diem <= toi_da;
    vi phạm thì raise ValueError. Ví dụ (8, 10) -> 0.8."""
    if toi_da <= 0 or not 0 <= diem <= toi_da:
        raise ValueError("Điểm hoặc thang điểm không hợp lệ")
    return diem / toi_da

# Bài 3
def chia_lo(values: list, kich_thuoc: int) -> list[list]:
    """Chia list thành các list con tối đa kich_thuoc phần tử, giữ thứ tự.
    kich_thuoc nguyên dương; <= 0 thì raise ValueError. Không sửa values.
    Ví dụ ([1,2,3,4,5], 2) -> [[1,2],[3,4],[5]]; [] -> []."""
    if kich_thuoc <= 0:
        raise ValueError("Kích thước phải dương")
    return [values[i:i + kich_thuoc] for i in range(0, len(values), kich_thuoc)]
