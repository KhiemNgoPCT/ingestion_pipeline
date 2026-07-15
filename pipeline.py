import hashlib
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
import concurrent.futures
from typing import List, Union

from loaders import load_pdf, load_docx, load_html, load_csv
from cleaning import clean_text

@dataclass
class IngestedDocument:
    id: str
    content: str
    source: str
    format: str
    language: str
    char_count: int
    word_count: int
    metadata: dict = field(default_factory=dict)
    ingested_at: str = ""

    def to_dict(self):
        return asdict(self)

class IngestionPipeline:
    def __init__(self):
        self.loaders = {
            ".pdf": load_pdf,
            ".docx": load_docx,
            ".html": load_html,
            ".htm": load_html,
            ".csv": load_csv
        }

    def ingest(self, path: Union[str, Path]) -> IngestedDocument:
        path = Path(path)
        ext = path.suffix.lower()
        
        if ext not in self.loaders:
            raise ValueError(f"Unsupported file format: {ext}")
            
        loader = self.loaders[ext]
        
        # Loader is expected to return (raw_text, format, language, metadata)
        raw_text, doc_format, language, metadata = loader(path)
        
        content = clean_text(raw_text)
        
        doc_id = hashlib.sha256(content.encode('utf-8')).hexdigest()
        char_count = len(content)
        word_count = len(content.split())
        ingested_at = datetime.now(timezone.utc).isoformat()
        
        return IngestedDocument(
            id=doc_id,
            content=content,
            source=str(path),
            format=doc_format,
            language=language,
            char_count=char_count,
            word_count=word_count,
            metadata=metadata,
            ingested_at=ingested_at
        )

    def ingest_batch(self, paths: List[Union[str, Path]]) -> List[IngestedDocument]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(self.ingest, paths))
        return results

    def save_jsonl(self, documents: List[IngestedDocument], output_path: Union[str, Path]):
        with open(output_path, 'w', encoding='utf-8') as f:
            for doc in documents:
                f.write(json.dumps(doc.to_dict(), ensure_ascii=False) + '\n')
