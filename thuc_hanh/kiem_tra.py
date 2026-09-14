"""Tự kiểm tra bài Python bằng unittest, không cần cài thêm gói.

Chạy từ thư mục gốc:
    .venv/Scripts/python.exe thuc_hanh/kiem_tra.py --tuan 1
    .venv/Scripts/python.exe thuc_hanh/kiem_tra.py --tat-ca --dap-an
"""

import argparse
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

# Giữ văn bản tiếng Việt đọc được khi PowerShell chuyển hướng đầu ra.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


class BaiTapTest(unittest.TestCase):
    thu_muc = "bai_tap"
    tuan = 1

    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parent / cls.thu_muc / f"tuan_{cls.tuan:02d}.py"
        spec = importlib.util.spec_from_file_location(f"bai_{cls.thu_muc}_{cls.tuan}", path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Không mở được bài tập: {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls.bai = module


class Tuan01(BaiTapTest):
    tuan = 1

    def test_01_loi_chao(self):
        self.assertEqual(self.bai.loi_chao, "Xin chào, An!")

    def test_02_tong_phut(self):
        self.assertEqual(self.bai.tong_phut, 180)

    def test_03_tong_gio(self):
        self.assertEqual(self.bai.tong_gio, 3.0)


class Tuan02(BaiTapTest):
    tuan = 2

    def test_01_ket_luan(self):
        self.assertEqual(self.bai.ket_luan, "dat")

    def test_02_doi_gio(self):
        self.assertEqual((self.bai.gio_nguyen, self.bai.phut_le), (2, 5))

    def test_03_hoan_thanh(self):
        self.assertIs(self.bai.hoan_thanh, False)


class Tuan03(BaiTapTest):
    tuan = 3

    def test_01_cong_don(self):
        self.assertEqual(self.bai.tong_phut, 135)

    def test_02_dem(self):
        self.assertEqual(self.bai.so_dat, 3)

    def test_03_binh_phuong(self):
        self.assertEqual(self.bai.tong_binh_phuong, 30)


class Tuan04(BaiTapTest):
    tuan = 4

    def test_01_chuan_hoa(self):
        self.assertEqual(self.bai.van_ban_sach, "python cho ai")

    def test_02_dao_list(self):
        self.assertEqual(self.bai.diem_dao, [6, 8, 6, 9])
        self.assertEqual(self.bai.diem_so, [9, 6, 8, 6])

    def test_03_slice(self):
        self.assertEqual(self.bai.hai_token_dau, ["ai", "python"])


class Tuan05(BaiTapTest):
    tuan = 5

    def test_01_tan_suat(self):
        self.assertEqual(self.bai.tan_suat, {"ai": 3, "python": 2, "ml": 1})

    def test_02_loai_trung(self):
        self.assertEqual(self.bai.token_duy_nhat, ["ai", "ml", "python"])

    def test_03_tong_hop(self):
        self.assertEqual(self.bai.tong_theo_nguoi, {"An": 75, "Binh": 60})


class Tuan06(BaiTapTest):
    tuan = 6

    def test_01_trung_binh(self):
        for values, expected in [([2, 4, 6], 4), ([-2, 2], 0), ([7], 7), ([0.1, 0.3], 0.2)]:
            with self.subTest(values=values):
                self.assertAlmostEqual(self.bai.trung_binh(values), expected)

    def test_02_trung_binh_rong(self):
        with self.assertRaises(ValueError):
            self.bai.trung_binh([])

    def test_03_chuan_hoa(self):
        self.assertAlmostEqual(self.bai.chuan_hoa_diem(8), 0.8)
        self.assertEqual(self.bai.chuan_hoa_diem(0, 20), 0)
        self.assertEqual(self.bai.chuan_hoa_diem(20, 20), 1)

    def test_04_diem_sai(self):
        for diem, toi_da in [(-1, 10), (11, 10), (0, 0), (0, -1)]:
            with self.subTest(diem=diem, toi_da=toi_da):
                with self.assertRaises(ValueError):
                    self.bai.chuan_hoa_diem(diem, toi_da)

    def test_05_chia_lo(self):
        values = [1, 2, 3, 4, 5]
        self.assertEqual(self.bai.chia_lo(values, 2), [[1, 2], [3, 4], [5]])
        self.assertEqual(values, [1, 2, 3, 4, 5])
        self.assertEqual(self.bai.chia_lo([], 2), [])
        self.assertEqual(self.bai.chia_lo([1, 2], 8), [[1, 2]])

    def test_06_kich_thuoc_sai(self):
        for size in (0, -2):
            with self.subTest(size=size):
                with self.assertRaises(ValueError):
                    self.bai.chia_lo([1], size)


class Tuan07(BaiTapTest):
    tuan = 7

    def test_01_doc_json(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "du_lieu.json"
            path.write_text('{"ten": "Bình", "phut": 45}', encoding="utf-8")
            self.assertEqual(self.bai.doc_json(path), {"ten": "Bình", "phut": 45})

    def test_02_file_thieu_va_json_sai(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "missing.json"
            with self.assertRaises(FileNotFoundError):
                self.bai.doc_json(path)
            path.write_text("{sai", encoding="utf-8")
            with self.assertRaises(json.JSONDecodeError):
                self.bai.doc_json(path)

    def test_03_tong_csv(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "hoc.csv"
            path.write_text("ten,phut\nAn,30\nBình,45\nAn,60\n", encoding="utf-8")
            self.assertEqual(self.bai.tong_phut_csv(path), 135)

    def test_04_csv_chi_header(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "hoc.csv"
            path.write_text("ten,phut\n", encoding="utf-8")
            self.assertEqual(self.bai.tong_phut_csv(path), 0)

    def test_05_csv_so_sai(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "hoc.csv"
            for value in ("abc", "-5", ""):
                with self.subTest(value=value):
                    path.write_text(f"ten,phut\nAn,{value}\n", encoding="utf-8")
                    with self.assertRaises(ValueError):
                        self.bai.tong_phut_csv(path)

    def test_06_ghi_json(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "ket_qua.json"
            data = [{"ten": "Bình", "phut": 45}]
            self.assertIsNone(self.bai.ghi_json(path, data))
            text = path.read_text(encoding="utf-8")
            self.assertIn("Bình", text)
            self.assertEqual(json.loads(text), data)
            # Ghi lần hai phải thay nội dung cũ và vẫn là JSON hợp lệ.
            self.bai.ghi_json(path, [])
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), [])


class Tuan08(BaiTapTest):
    tuan = 8

    def test_01_doc_phut(self):
        self.assertEqual(self.bai.doc_phut(" 45 "), 45)
        self.assertEqual(self.bai.doc_phut("0"), 0)

    def test_02_doc_phut_sai(self):
        for value in ("", "abc", "1.5", "-1"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    self.bai.doc_phut(value)

    def test_03_trung_binh(self):
        self.assertEqual(self.bai.trung_binh([2, 4, 6]), 4)
        self.assertEqual(self.bai.trung_binh([7]), 7)
        self.assertEqual(self.bai.trung_binh([-2, 2]), 0)
        self.assertAlmostEqual(self.bai.trung_binh([1, 2]), 1.5)
        self.assertAlmostEqual(self.bai.trung_binh([0.1, 0.3]), 0.2)

    def test_04_trung_binh_rong(self):
        self.assertIsNone(self.bai.trung_binh([]))

    def test_05_cac_lan_goi_doc_lap(self):
        self.assertEqual(self.bai.them_muc("a"), ["a"])
        self.assertEqual(self.bai.them_muc("b"), ["b"])

    def test_06_khong_sua_dau_vao(self):
        data = ["a"]
        self.assertEqual(self.bai.them_muc("b", data), ["a", "b"])
        self.assertEqual(data, ["a"])


CAC_TUAN = [Tuan01, Tuan02, Tuan03, Tuan04, Tuan05, Tuan06, Tuan07, Tuan08]


def main() -> int:
    parser = argparse.ArgumentParser(description="Tự kiểm tra 8 bộ bài tập Python.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--tuan", type=int, choices=range(1, 9), help="Tuần 1–8; mặc định tuần 1")
    group.add_argument("--tat-ca", action="store_true", help="Kiểm tra tất cả 8 tuần")
    parser.add_argument("--dap-an", action="store_true", help="Kiểm tra đáp án tham khảo, không phải bài làm")
    args = parser.parse_args()
    folder = "dap_an" if args.dap_an else "bai_tap"
    selected = CAC_TUAN if args.tat_ca else [CAC_TUAN[(args.tuan or 1) - 1]]
    print(f"Đang kiểm tra: {folder}.", flush=True)
    if args.dap_an:
        print("Đây là đáp án tham khảo; kết quả không phản ánh bài làm của bạn.", flush=True)
    suite = unittest.TestSuite()
    for cls in selected:
        cls.thu_muc = folder
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        print("Hãy đọc lỗi, sửa bài tập và chạy lại. Bài chưa làm báo lỗi là bình thường.")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
