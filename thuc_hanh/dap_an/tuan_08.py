"""Bộ bài tập tuần 8: đọc đặc tả trong từng hàm trước khi viết mã."""


# Bài 1
def doc_phut(text: str) -> int:
    """Đổi chuỗi sang số nguyên không âm; cho phép khoảng trắng đầu/cuối.
    Chuỗi rỗng, 'abc', '1.5' hoặc số âm -> ValueError với thông báo hữu ích."""
    try:
        phut = int(text)
    except ValueError as error:
        raise ValueError("Hãy nhập số phút nguyên không âm") from error
    if phut < 0:
        raise ValueError("Số phút không thể âm")
    return phut

# Bài 2
def trung_binh(values: list[float]) -> float | None:
    """Sửa lỗi chia sai mẫu số: trung bình bằng tổng / số phần tử.
    List rỗng -> None. Đầu vào là các số hữu hạn.
    Tuần 6 quy ước rỗng gây lỗi; ở bài này đặc tả yêu cầu None."""
    if not values:
        return None
    return sum(values) / len(values)

# Bài 3
def them_muc(muc: str, nhat_ky: list[str] | None = None) -> list[str]:
    """Trả về list mới có muc ở cuối. Không sửa list đầu vào.
    Các lần gọi không truyền nhat_ky phải độc lập: them_muc('a')->['a'],
    rồi them_muc('b')->['b']. Tránh đối số mặc định là list rỗng."""
    ket_qua = list(nhat_ky) if nhat_ky is not None else []
    ket_qua.append(muc)
    return ket_qua
