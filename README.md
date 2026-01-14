# 🛒 GROCERY MANAGEMENT SYSTEM

**Website Quản Lý Cửa Hàng Tạp Hóa**

---

## I. Giới thiệu dự án

- **Tên hệ thống:** Grocery Management
- **Mục tiêu:**  
  Hệ thống được xây dựng nhằm thay thế phương pháp ghi chép sổ tay truyền thống bằng phần mềm, giúp quản lý hàng tồn kho, hỗ trợ thanh toán nhanh chóng và theo dõi lịch sử bán hàng một cách chính xác.
- **Đối tượng sử dụng:**

  - Chủ cửa hàng tạp hóa
  - Nhân viên bán hàng

- **Tài liệu phân tích chi tiết (Google Docs):**  
  👉 https://docs.google.com/document/d/1UP29VTzBU0s1DtjUibPeDHIciSeTllRIimfbf7LhCrM/edit?usp=sharing

---

## II. Phân tích yêu cầu chức năng

Hệ thống gồm 03 phân hệ cốt lõi:

### 1. Phân hệ quản lý hàng hóa

- Thêm mới sản phẩm (tên, đơn vị tính, mã vạch, giá bán).
- Cập nhật thông tin sản phẩm (không bao gồm tồn kho).
- Xem danh sách sản phẩm và số lượng tồn kho hiện tại.

---

### 2. Phân hệ quản lý nhập hàng

- Tạo phiếu nhập hàng.
- Cho phép **tạo mới sản phẩm trực tiếp trong quá trình nhập hàng** nếu sản phẩm chưa tồn tại.
- Ghi nhận số lượng nhập và giá vốn.
- Tự động cập nhật tồn kho sau khi xác nhận phiếu nhập.

---

### 3. Phân hệ thanh toán (tạo hóa đơn)

- Tìm sản phẩm theo mã vạch hoặc tên.
- Nhập số lượng bán.
- Đơn giá được **lấy tự động từ cơ sở dữ liệu**, không nhập tay.
- Tính tổng tiền hóa đơn.
- Lưu lịch sử bán hàng và trừ tồn kho.

---

## III. Thiết kế cơ sở dữ liệu

### 1. Bảng `sanpham` (Danh mục hàng hóa)

| Trường dữ liệu | Kiểu dữ liệu | Mô tả                 |
| -------------- | ------------ | --------------------- |
| Masp (PK)      | String / Int | Mã sản phẩm / mã vạch |
| Tensp          | String       | Tên sản phẩm          |
| Donvitinh      | String       | Chai, gói, lon, kg... |
| Giaban         | Decimal      | Giá bán hiện tại      |
| Soluongton     | Int          | Số lượng tồn kho      |

---

### 2. Bảng `phieunhap` (Lịch sử nhập hàng)

| Trường dữ liệu | Kiểu dữ liệu | Mô tả          |
| -------------- | ------------ | -------------- |
| Manhap (PK)    | Auto Int     | Mã phiếu nhập  |
| Masp (FK)      | String / Int | Mã sản phẩm    |
| Ngaynhap       | Datetime     | Ngày nhập      |
| Tongtiennhap   | Decimal      | Tổng tiền nhập |

---

### 3. Bảng `hoadon` (Lịch sử bán hàng)

| Trường dữ liệu | Kiểu dữ liệu | Mô tả             |
| -------------- | ------------ | ----------------- |
| Mahd (PK)      | Auto Int     | Mã hóa đơn        |
| Ngayban        | Datetime     | Ngày bán          |
| Tongtien       | Decimal      | Tổng tiền hóa đơn |

---

### 4. Bảng `chitiethoadon` (Chi tiết hóa đơn)

| Trường dữ liệu | Kiểu dữ liệu | Mô tả                           |
| -------------- | ------------ | ------------------------------- |
| Mahd (FK)      | Int          | Thuộc hóa đơn                   |
| Masp (FK)      | String / Int | Sản phẩm                        |
| Soluong        | Int          | Số lượng bán                    |
| Giabanlucdo    | Decimal      | Giá bán tại thời điểm giao dịch |

---

## IV. Logic nghiệp vụ hệ thống

### 1. Logic nhập hàng & tạo sản phẩm

- Phiếu nhập hàng là **nguồn duy nhất** làm tăng tồn kho.
- Khi nhập hàng:
  - Nếu sản phẩm chưa tồn tại → cho phép tạo mới sản phẩm.
  - Nếu sản phẩm đã tồn tại → cộng dồn tồn kho.
- Công thức cập nhật:

```

soluongton_moi = soluongton_cu + soluong_nhap

```

---

### 2. Logic sửa thông tin sản phẩm

- Cho phép sửa:
- Tên sản phẩm
- Đơn vị tính
- Giá bán
- **Không cho phép sửa:**
- Tồn kho
- Mã sản phẩm / mã vạch

---

### 3. Logic tạo hóa đơn

- Nhân viên:
- Chỉ chọn sản phẩm
- Nhập số lượng bán
- Giá bán:
- Lấy tự động từ bảng `sanpham`
- Hệ thống tự động:
- Tính tiền
- Trừ tồn kho
- Lưu hóa đơn

---

### 4. Logic hủy giao dịch

- Trong quá trình tạo hóa đơn:
- Có thể thêm nhiều sản phẩm (Add item).
- Nếu người dùng **hủy hoặc thoát** khi chưa xác nhận:
  - Không lưu hóa đơn
  - Không lưu hóa đơn nháp
  - Không ảnh hưởng tồn kho

---

### 5. Logic xem và quản lý hóa đơn

- Chỉ cho phép **xem hóa đơn**.
- Không cho phép:
- Sửa hóa đơn
- Xóa hóa đơn
- Thay đổi chi tiết bán hàng

---

## V. Quy trình nghiệp vụ

### 1. Quy trình nhập hàng

1. Chủ cửa hàng chọn chức năng nhập hàng.
2. Chọn hoặc tạo sản phẩm.
3. Nhập số lượng và giá vốn.
4. Xác nhận → hệ thống cập nhật tồn kho.

---

### 2. Quy trình bán hàng

1. Nhân viên quét/chọn sản phẩm.
2. Nhập số lượng.
3. Hệ thống tính tiền tự động.
4. Xác nhận thanh toán:

- Tạo hóa đơn
- Lưu chi tiết hóa đơn
- Trừ tồn kho

---

## VI. Hạn chế của hệ thống (Limitations)

1. Chưa có phân quyền người dùng (Admin / Nhân viên).
2. Chưa hỗ trợ quản lý công nợ khách hàng.
3. Chưa có báo cáo thống kê nâng cao.
4. Chưa hỗ trợ trả hàng / hoàn tiền.
5. Phụ thuộc thao tác nhập liệu thủ công nếu không có máy quét mã vạch.
6. Chưa có cơ chế sao lưu và phục hồi dữ liệu tự động.

---

## VII. Hướng phát triển trong tương lai

- Phân quyền người dùng.
- Báo cáo doanh thu và tồn kho.
- Quản lý khách hàng và công nợ.
- Tích hợp máy quét mã vạch.
- Tự động sao lưu dữ liệu.

---

## 📌 Kết luận

Hệ thống Grocery Management đáp ứng tốt nhu cầu quản lý cửa hàng tạp hóa quy mô nhỏ, giúp giảm sai sót thủ công, tăng hiệu quả quản lý và tạo nền tảng mở rộng trong tương lai.
