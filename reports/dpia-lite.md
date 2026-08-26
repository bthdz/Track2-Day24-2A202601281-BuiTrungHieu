# DPIA-lite

## 1. Dữ liệu gì

Hệ thống Agent xử lý các nhóm dữ liệu cá nhân sau:
- **Dữ liệu nhạy cảm và nhận diện khách hàng**: Số CCCD 12 chữ số, số điện thoại 10 chữ số, số tài khoản ngân hàng từ 8 đến 16 chữ số, họ tên và email cá nhân. Các thông tin này được lưu trữ tại `data/customers.json` và truy xuất thông qua tool `read_customer`.
- **Nội dung ticket phản hồi**: Văn bản yêu cầu từ phía người dùng được tìm kiếm qua `search_docs` trong thư mục `corpus/`, có thể chứa dữ liệu cá nhân hoặc các chỉ thị không tin cậy do bên ngoài chèn vào.

## 2. Mục đích gì

- **Tổng hợp và phản hồi ticket**: Đọc dữ liệu từ các ticket dạng Markdown trong thư mục `corpus/` để tóm tắt và hỗ trợ người dùng giải quyết thắc mắc.
- **Tra cứu thông tin khách hàng**: Tra cứu chi tiết hồ sơ từ nguồn tin cậy dựa trên danh sách `related_tickets` trong file `customers.json` nhằm phục vụ công tác hỗ trợ kỹ thuật và kiểm toán nội bộ.

## 3. Chảy đi đâu

- **Nhật ký kiểm toán nội bộ**: Mọi thao tác truy cập dữ liệu và gọi tool cho phép hoặc từ chối đều được ghi nhận vào file `reports/ledger.jsonl` với cơ chế chuỗi hash SHA256 chống chỉnh sửa.
- **Điểm đích thử nghiệm exfil sink**: Môi trường mô phỏng máy chủ đích của kẻ tấn công tại cổng 9999. Luồng dữ liệu này bị ngăn chặn tuyệt đối bởi các điểm kiểm soát `policy.py` và `runner.py`, bảo đảm không có bất kỳ thông tin cá nhân nào rò rỉ ra sink.
- **API nhà cung cấp mô hình**: Khi vận hành với mô hình Claude qua API, dữ liệu prompt được truyền qua kết nối bảo mật HTTPS tới máy chủ của Anthropic. Đây là luồng chuyển dữ liệu xuyên biên giới theo Nghị định 356/2025/NĐ-CP. Hệ thống kiểm soát bằng cơ chế ẩn danh dữ liệu `pii.py` trước khi đưa vào context để tuân thủ quy định bảo vệ dữ liệu cá nhân.
