# Multi-Format Ingestion Pipeline

Ingestion Pipeline là hệ thống tự động xử lý và làm sạch tài liệu từ nhiều định dạng khác nhau (PDF, DOCX, HTML, CSV) để xuất ra một JSON schema thống nhất. Pipeline này rất cần thiết để chuẩn bị dữ liệu chất lượng cao, loại bỏ nhiễu và boilerplate trước khi đưa vào vector database cho hệ thống RAG.

## Yêu cầu hệ thống (System Dependencies)

Để hỗ trợ OCR cho các file PDF scan, bạn cần cài đặt Tesseract trên hệ thống:

- **macOS**: `brew install tesseract`
- **Ubuntu/Debian**: `apt install tesseract-ocr`

## Cài đặt Python packages

Tạo môi trường ảo và cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

## Format Support Table

Dưới đây là các định dạng được hỗ trợ và thư viện tương ứng được sử dụng:

| Format   | Thư viện chính     | Fallback / Phụ trợ                    |
| :------- | :----------------- | :------------------------------------ |
| **PDF**  | `PyMuPDF` (`fitz`) | `pytesseract` (OCR cho scanned PDF)   |
| **DOCX** | `python-docx`      | -                                     |
| **HTML** | `trafilatura`      | `BeautifulSoup4` (loại bỏ nav/footer) |
| **CSV**  | `pandas`           | `tabulate` (chuyển sang markdown)     |

## Ví dụ sử dụng

```python
from pipeline import IngestionPipeline

pipeline = IngestionPipeline()

# Xử lý một file đơn lẻ
doc = pipeline.ingest("report.pdf")
print(doc.language, doc.word_count)

# Xử lý nhiều file song song (Batch processing)
docs = pipeline.ingest_batch(["a.pdf", "b.docx", "c.html", "d.csv"])

# Lưu kết quả ra file JSON Lines
pipeline.save_jsonl(docs, "output.jsonl")
```

## Chạy kiểm thử (Unit Tests)

Đảm bảo bạn đang ở trong thư mục `ingestion_pipeline` và đã kích hoạt môi trường ảo:

```bash
PYTHONPATH=. pytest tests/ -v
```
