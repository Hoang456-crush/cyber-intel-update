# Tiêu Chí Đánh Giá CVE Có Thể Tiếp Cận Được (Actionable CVE Criteria)

Trong thế giới an toàn thông tin, mỗi ngày có hàng chục đến hàng trăm CVE mới được công bố. Tuy nhiên, hơn 90% trong số đó là:
- Yêu cầu quyền truy cập vật lý hoặc quyền root trên máy nạn nhân.
- Lỗ hổng trong phần mềm nội bộ ít gặp hoặc ứng dụng desktop đơn lẻ.
- Lỗ hổng lý thuyết chưa có phương thức khai thác khả thi (PoC).
- DoS (Denial of Service) thuần túy không mang lại giá trị khai thác trong Bug Bounty.

Tài liệu này định nghĩa ma trận tính điểm (Actionability Matrix) giúp Agent sàng lọc chính xác các **CVE tiếp cận được (Actionable CVEs)** cho Bug Hunter.

---

## 1. Ma Trận Đánh Giá Khả Năng Tiếp Cận (Accessibility Matrix)

Điểm khả thi (Feasibility Score) được tính từ 0 đến 10 điểm dựa trên 5 khía cạnh:

| Khía Cạnh | Tiêu Chí Ưu Tiên | Điểm | Lý Do |
| :--- | :--- | :---: | :--- |
| **Attack Vector** | `Network` (Khai thác qua HTTP/HTTPS/API từ xa) | **+3** | Bug Hunter chỉ có thể tương tác qua mạng từ xa. |
| **Authentication** | `None` (Unauthenticated) | **+3** | Bất kỳ ai cũng gửi được request khai thác. |
| | `Low` (Quyền user thường / Tự đăng ký) | **+2** | Dễ dàng đăng ký tài khoản thử nghiệm trên target. |
| | `High / Admin` (Cần tài khoản quản trị) | **-2** | Khó tiếp cận trong thực tế (trừ khi kết hợp chuỗi lỗi). |
| **Loại Mục Tiêu** | Web / API / CMS / Cloud / SaaS phổ biến | **+2** | Xuất hiện dày đặc trong phạm vi (scope) Bug Bounty. |
| | Frameworks (Laravel, Spring, Next.js, Django) | **+2** | Rất nhiều công ty công nghệ sử dụng. |
| | DevOps & AI (GitLab, Jenkins, MLflow, Ollama) | **+2** | Thường bị mở public ra ngoài hoặc nội bộ dễ tấn công. |
| | Thiết bị mạng (Fortinet, Ivanti, Palo Alto) | **+1** | Phổ biến tại các tập đoàn lớn. |
| **Weaponization** | Có Nuclei Template sẵn | **+2** | Đã được chuẩn hóa thành lệnh quét tự động hóa. |
| | Có Public PoC trên GitHub / Exploit-DB | **+2** | Có mã nguồn khai thác cụ thể để tham khảo. |
| | Nằm trong CISA KEV (Known Exploited) | **+2** | Đã và đang bị tin tặc khai thác trên thực địa. |
| **Loại Lỗ Hổng** | RCE, Auth Bypass, SSRF, Arbitrary File Upload | **+2** | Tác động tối đa, tiền thưởng Critical/P1. |
| | SQL Injection, IDOR, Account Takeover | **+1** | Tác động High/P2. |
| | DoS, Self-XSS, Informational | **-3** | Không phù hợp mục tiêu Bug Bounty. |

### Ngưỡng Lựa Chọn:
- **Từ 8 - 10 điểm (Tier 1 - Ưu tiên hàng đầu)**: Bắt buộc chọn vào mục phân tích sâu và viết Bảng hướng dẫn sử dụng.
- **Từ 6 - 7 điểm (Tier 2 - Đáng chú ý)**: Đưa vào danh sách tóm tắt nhanh.
- **Dưới 6 điểm**: Bỏ qua để tiết kiệm thời gian nghiên cứu.

---

## 2. Danh Sách Nhận Diện Nhanh Các Phần Mềm Phổ Biến

### Web CMS & E-Commerce:
- WordPress (Core & top 100 plugins: WooCommerce, Elementor, Contact Form 7, v.v.)
- Craft CMS, Drupal, Joomla, Ghost, Strapi, Directus.
- Magento (Adobe Commerce), PrestaShop, Shopify Apps.

### Frameworks & Ngôn Ngữ:
- PHP / Laravel, Symfony.
- Python / Django, FastAPI, Flask.
- JavaScript / Next.js, Express, Nuxt, Node.js.
- Java / Spring Boot, Apache Struts, Log4j.
- Go / Gin, Fiber.

### Hạ Tầng, CI/CD, DevSecOps & AI:
- MLflow, Ollama, LangChain, vLLM, Gradio, Ray.
- GitLab, GitHub Enterprise, Jenkins, ArgoCD.
- Docker, Kubernetes, Portainer, Harbor.
- Atlassian Confluence, Jira.
- Grafana, Kibana, Zabbix.

### Mạng & Cổng Bảo Mật (Edge Devices / Gateways):
- Fortinet FortiOS / FortiGate.
- Ivanti Connect Secure / EPMM.
- Palo Alto PAN-OS / GlobalProtect.
- Citrix NetScaler / ADC.
- SonicWall, Check Point.

---

## 3. Cách Tra Cứu Nhanh PoC Khi Có CVE Mới
1. **GitHub Search**: `CVE-YYYY-XXXXX poc` hoặc `CVE-YYYY-XXXXX exploit`.
2. **ProjectDiscovery Nuclei Templates**: Tra cứu tại thư mục `http/cves/YYYY/CVE-YYYY-XXXXX.yaml`.
3. **VulnCheck & Sploitus**: Tra cứu trên công cụ tổng hợp mã khai thác.
4. **Packet Storm & Exploit-DB**: Kho lưu trữ PoC truyền thống.
