import re
import ftfy

def fix_encoding(text: str) -> str:
    """Fix mojibake and standardize unicode."""
    if not text:
        return ""
    return ftfy.fix_text(text)

def remove_boilerplate(text: str) -> str:
    """Remove page numbers, confidentiality notices, etc."""
    if not text:
        return ""
    # Remove "Page X of Y" or "- X -" or "Page X"
    text = re.sub(r'(?i)^\s*(page\s+\d+(\s+of\s+\d+)?)\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'(?i)^\s*(-\s*\d+\s*-)\s*$', '', text, flags=re.MULTILINE)
    
    # Remove confidentiality notices
    text = re.sub(r'(?i)^\s*confidential\s*.*$', '', text, flags=re.MULTILINE)
    
    return text

def normalize_whitespace(text: str) -> str:
    """Collapse spaces/tabs, normalize newlines."""
    if not text:
        return ""
    # Normalize spaces/tabs
    text = re.sub(r'[ \t]+', ' ', text)
    # Normalize multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def clean_text(text: str) -> str:
    """Apply the full cleaning pipeline."""
    if not text:
        return ""
    return normalize_whitespace(remove_boilerplate(fix_encoding(text)))
