# Compliance mapping

| Requirement | Control | Evidence |
|---|---|---|
| Luật 91/2025 — quyền yêu cầu xoá | Delete cascade xoá thông tin chủ thể khỏi data store và ghi vết audit ledger | `agent/delete_cascade.py:L21-L68`, `tests/test_delete_cascade.py:L10-L39` |
| NĐ 356/2025 — hồ sơ xuyên biên giới 60 ngày | Danh mục kiểm soát luồng dữ liệu cho API gọi mô hình | `reports/dpia-lite.md` §3 |
| ASI03 — privilege abuse | Định danh agent riêng biệt kết hợp kiểm tra context tại Policy Enforcement Point | `agent/policy.py:L31-L43`, `agent/runner.py:L26-L45` |
| ASI01 — goal hijack | Kiến trúc Trifecta split ngắt kết nối giữa nội dung không tin cậy với việc gọi egress hoặc đọc dữ liệu khách hàng | `agent/runner.py:L62-L121`, `reports/attack-after.log` |
| ISO 42001 Clause 5-6 | Mô hình Policy-as-code tích hợp sổ nhật ký kiểm toán chống chỉnh sửa | `agent/policy.py:L39-L43`, `agent/ledger.py:L39-L87` |
