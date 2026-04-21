1) OLTP và OLAP

OLTP là hệ thống xử lý giao dịch hằng ngày, còn OLAP là hệ thống phục vụ phân tích dữ liệu.
OLTP tối ưu cho giao dịch nhỏ, nhanh, chính xác; OLAP tối ưu cho truy vấn lớn, tổng hợp và dữ liệu lịch sử.
Ví dụ, hệ thống đặt hàng hoặc chuyển tiền là OLTP, còn dashboard doanh thu hoặc báo cáo BI là OLAP.
Trade-off là OLTP rất tốt cho vận hành nhưng không phù hợp để phân tích nặng, còn OLAP phân tích tốt nhưng không phù hợp để xử lý giao dịch thời gian thực.

2) Data Lake, Data Warehouse và Lakehouse

Data Lake là nơi lưu dữ liệu thô và đa dạng định dạng, Data Warehouse là nơi lưu dữ liệu đã chuẩn hóa để phân tích, còn Lakehouse là mô hình kết hợp hai bên.
Data Lake tối ưu cho lưu trữ linh hoạt và quy mô lớn, Data Warehouse tối ưu cho truy vấn phân tích ổn định, còn Lakehouse tối ưu cho việc vừa lưu trữ linh hoạt vừa phân tích hiệu quả.
Ví dụ, file log JSON và CSV raw thường nằm ở Data Lake, bảng doanh thu chuẩn hóa nằm ở Warehouse, còn Delta Lake/Iceberg là kiểu triển khai Lakehouse.
Trade-off là Lake linh hoạt nhưng khó quản lý hơn, Warehouse dễ dùng cho BI nhưng kém linh hoạt hơn với raw data, còn Lakehouse mạnh hơn nhưng kiến trúc và vận hành phức tạp hơn.

3) Partition và Index

Partition là cách chia dữ liệu thành các phần nhỏ theo khóa như ngày hoặc vùng, còn Index là cấu trúc phụ trợ giúp tìm bản ghi nhanh hơn.
Partition tối ưu cho việc giảm lượng dữ liệu phải quét, còn Index tối ưu cho việc tăng tốc truy cập theo điều kiện tìm kiếm.
Ví dụ, bảng đơn hàng có thể partition theo order_date, còn cột customer_id có thể được đánh index để tìm nhanh đơn của một khách hàng.
Trade-off là partition quá nhỏ gây nhiều file nhỏ và overhead, còn index giúp đọc nhanh nhưng làm ghi và cập nhật chậm hơn.

4) CSV và Parquet

CSV là định dạng text lưu dữ liệu theo dòng, còn Parquet là định dạng cột được thiết kế cho analytics.
CSV tối ưu cho trao đổi đơn giản và dễ nhìn, còn Parquet tối ưu cho lưu trữ nén tốt và truy vấn phân tích nhanh hơn.
Ví dụ, dữ liệu export thủ công thường ở CSV, còn dữ liệu trong data lake phục vụ Spark hoặc warehouse thường lưu ở Parquet.
Trade-off là CSV dễ dùng nhưng đọc chậm và tốn I/O, còn Parquet nhanh hơn cho analytics nhưng khó đọc trực tiếp bằng mắt người hơn.

5) ETL và ELT

ETL là Extract rồi Transform rồi mới Load, còn ELT là Extract rồi Load trước rồi Transform trong hệ đích.
ETL tối ưu cho kiểm soát dữ liệu trước khi nạp, còn ELT tối ưu cho việc tận dụng compute mạnh của warehouse hoặc lakehouse.
Ví dụ, nếu bạn làm sạch dữ liệu trước khi nạp vào hệ thống thì đó là ETL, còn nếu nạp raw vào BigQuery, Snowflake hay Spark rồi mới transform thì đó là ELT.
Trade-off là ETL kiểm soát đầu vào tốt hơn nhưng kém linh hoạt hơn, còn ELT linh hoạt và mạnh hơn trên hệ hiện đại nhưng đòi hỏi hệ đích đủ khả năng xử lý.

6) Idempotent pipeline

Idempotent pipeline là pipeline mà chạy nhiều lần với cùng input vẫn cho cùng kết quả cuối.
Nó tối ưu cho tính đúng đắn, khả năng retry, rerun và recovery khi pipeline bị lỗi.
Ví dụ, chạy lại job của ngày hôm qua mà bảng kết quả không bị nhân đôi dữ liệu thì đó là idempotent.
Trade-off là thiết kế idempotent thường phức tạp hơn, nhưng đổi lại pipeline an toàn và dễ vận hành hơn rất nhiều.

7) Tại sao rerun có thể phá dữ liệu

Rerun là việc chạy lại một phần hoặc toàn bộ pipeline đã từng chạy trước đó.
Mục tiêu của rerun là phục hồi dữ liệu, backfill hoặc sửa lỗi, nhưng nó chỉ an toàn khi pipeline được thiết kế đúng.
Ví dụ, nếu job append lại dữ liệu cũ thay vì upsert hoặc overwrite đúng partition thì rerun có thể tạo duplicate hoặc mất dữ liệu đúng.
Trade-off là rerun giúp sửa lỗi và khôi phục hệ thống, nhưng nếu pipeline không idempotent hoặc không kiểm soát partition/key tốt thì nó có thể phá dữ liệu.