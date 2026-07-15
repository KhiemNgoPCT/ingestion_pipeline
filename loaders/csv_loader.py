from pathlib import Path
import pandas as pd

def load_csv(path: Path):
    df = pd.read_csv(path)
    
    # Convert to markdown table
    raw_text = df.to_markdown(index=False)
    
    metadata = {
        "columns": df.columns.tolist(),
        "row_count": len(df)
    }
    
    return raw_text, "csv", "en", metadata
