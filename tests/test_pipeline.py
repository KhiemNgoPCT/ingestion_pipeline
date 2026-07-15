from pipeline import IngestionPipeline

def test_ingest_id_is_idempotent(sample_pdf):
    pipeline = IngestionPipeline()
    doc1 = pipeline.ingest(sample_pdf)
    doc2 = pipeline.ingest(sample_pdf)
    assert doc1.id == doc2.id

def test_ingest_batch_preserves_order(sample_pdf, sample_docx, sample_html):
    pipeline = IngestionPipeline()
    paths = [sample_pdf, sample_docx, sample_html]
    docs = pipeline.ingest_batch(paths)
    
    assert len(docs) == 3
    assert docs[0].format == "pdf"
    assert docs[1].format == "docx"
    assert docs[2].format == "html"
