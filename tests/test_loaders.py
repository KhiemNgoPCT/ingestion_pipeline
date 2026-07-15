from loaders.pdf_loader import load_pdf
from loaders.docx_loader import load_docx
from loaders.html_loader import load_html
from loaders.csv_loader import load_csv

def test_load_pdf_returns_document(sample_pdf):
    raw_text, doc_format, language, metadata = load_pdf(sample_pdf)
    assert doc_format == "pdf"
    assert "Hello from PDF" in raw_text

def test_load_docx_extracts_headings(sample_docx):
    raw_text, doc_format, language, metadata = load_docx(sample_docx)
    assert doc_format == "docx"
    assert "Test Heading" in raw_text

def test_load_html_strips_nav_footer(sample_html):
    raw_text, doc_format, language, metadata = load_html(sample_html)
    assert doc_format == "html"
    assert "Main Content" in raw_text
    assert "Navigation links" not in raw_text
    assert "Footer notes" not in raw_text

def test_load_csv_metadata_columns(sample_csv):
    raw_text, doc_format, language, metadata = load_csv(sample_csv)
    assert doc_format == "csv"
    assert metadata["columns"] == ["name", "value"]
