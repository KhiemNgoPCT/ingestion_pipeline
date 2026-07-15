from pathlib import Path
from pipeline import IngestionPipeline

def main():
    pipeline = IngestionPipeline()
    
    # Path to the sample files we generated
    fixtures_dir = Path("tests/fixtures")
    
    files_to_process = [
        fixtures_dir / "sample.pdf",
        fixtures_dir / "sample.docx",
        fixtures_dir / "sample.html",
        fixtures_dir / "sample.csv"
    ]
    
    print(f"Bắt đầu xử lý {len(files_to_process)} file bằng ingest_batch...")
    
    # Run batch processing
    documents = pipeline.ingest_batch(files_to_process)
    
    print("\nKết quả xử lý:")
    for doc in documents:
        print("-" * 50)
        print(f"File: {doc.source}")
        print(f"Format: {doc.format}")
        print(f"ID: {doc.id}")
        print(f"Metadata: {doc.metadata}")
        print(f"Content (trích đoạn): {doc.content[:100]}...")
        
    # Save to JSONL
    output_file = "output.jsonl"
    pipeline.save_jsonl(documents, output_file)
    print("\n" + "=" * 50)
    print(f"Đã lưu kết quả thành công vào file: {output_file}")
    
    # Đọc lại và in ra cấu trúc của dòng đầu tiên trong file jsonl
    import json
    with open(output_file, 'r', encoding='utf-8') as f:
        first_line = json.loads(f.readline())
        print("\nCấu trúc JSON Schema thực tế được xuất ra (Document đầu tiên):")
        print(json.dumps(first_line, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
