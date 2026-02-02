import spacy
import re

# Global variable to cache the model
NLP_MODEL = None

def load_nlp_model():
    """Loads the Spacy NLP model."""
    global NLP_MODEL
    if NLP_MODEL is None:
        try:
            NLP_MODEL = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback or instruction to download
            # In a real app, might want to download programmatically or warn
            print("Downloading spacy model...")
            from spacy.cli import download
            download("en_core_web_sm")
            NLP_MODEL = spacy.load("en_core_web_sm")
    return NLP_MODEL

def extract_entities(text):
    """
    Extracts named entities (Parties, Dates, Money, Locations) from text.
    """
    nlp = load_nlp_model()
    doc = nlp(text)
    
    entities = {
        "Parties": [],
        "Dates": [],
        "Money": [],
        "Locations": []
    }
    
    for ent in doc.ents:
        if ent.label_ == "ORG" or ent.label_ == "PERSON":
            if ent.text not in entities["Parties"]:
                entities["Parties"].append(ent.text)
        elif ent.label_ == "DATE":
            if ent.text not in entities["Dates"]:
                entities["Dates"].append(ent.text)
        elif ent.label_ == "MONEY":
            if ent.text not in entities["Money"]:
                entities["Money"].append(ent.text)
        elif ent.label_ == "GPE":
            if ent.text not in entities["Locations"]:
                entities["Locations"].append(ent.text)
                
    return entities

def highlight_entities(text):
    """
    Returns HTML text with highlighted entities for UI display.
    """
    nlp = load_nlp_model()
    doc = nlp(text)
    html = spacy.displacy.render(doc, style="ent", page=True)
    return html

def split_into_clauses(text):
    """
    Splits text into clauses based on common numbering patterns.
    Returns a list of dicts: {'id': '1', 'text': '...'}
    """
    # Pattern for "1. ", "1.1 ", "ARTICLE 1", "Section 1"
    # This is a simple heuristic; legal docs vary wildly.
    pattern = r'(?:\n|^)\s*(?:ARTICLE\s+[IVX]+|SECTION\s+\d+|[0-9]+\.)\s+'
    
    splits = re.split(pattern, text, flags=re.IGNORECASE)
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    
    clauses = []
    
    # re.split includes the part before the first match (often preamble/title)
    if splits[0].strip():
        clauses.append({"id": "Preamble", "text": splits[0].strip()})
        
    for i, match in enumerate(matches):
        if i + 1 < len(splits):
            clause_text = splits[i+1].strip()
            if clause_text:
                # Clean up the ID from the match (remove newlines/spaces)
                clause_id = match.strip()
                clauses.append({"id": clause_id, "text": clause_text})
                
    return clauses
