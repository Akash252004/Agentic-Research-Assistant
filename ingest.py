import os
import requests
import glob
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

ENDEE_API_URL = os.getenv("ENDEE_API_URL", "http://localhost:8080")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "static", "papers")

import os
import requests
import glob
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from endee import Endee

load_dotenv()

# Initialize model
_model = None
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

# Initialize Endee Client
def get_endee_index():
    try:
        # Use default local settings: http://127.0.0.1:8080/api/v1
        client = Endee(token="")
        # Explicitly ensure base_url is correct if needed, but default should work
        client.set_base_url(ENDEE_API_URL) 
        
        try:
            return client.get_index("nuclear_papers")
        except Exception:
            print("Index 'nuclear_papers' not found, creating it...")
            # Create index if it doesn't exist. Dimension 384 for all-MiniLM-L6-v2.
            client.create_index(
                name="nuclear_papers",
                dimension=384,
                space_type="cosine",
                version=1
            )
            return client.get_index("nuclear_papers")
            
    except Exception as e:
        print(f"Failed to connect to Endee: {e}")
        return None

def ingest_file(pdf_path):
    filename = os.path.basename(pdf_path)
    print(f"Processing {filename}...")
    model = get_model()
    index = get_endee_index()
    
    if index is None:
        print("Endee index not accessible.")
        return False, "Endee index not accessible."
    
    try:
        reader = PdfReader(pdf_path)
        batch = []
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if not text or len(text.strip()) < 50:
                continue
            
            # Create embedding
            vector = model.encode(text).tolist()
            
            # Prepare item for Endee Upsert
            item = {
                "id": f"{filename}_{i+1}",
                "vector": vector,
                "meta": {
                    "text": text,
                    "filename": filename,
                    "page_number": i + 1,
                    "source": filename
                }
            }
            batch.append(item)
            
        if batch:
            print(f"Upserting {len(batch)} chunks/pages...")
            index.upsert(batch)
            print("Upsert successful.")
            return True, f"Successfully indexed {len(batch)} pages."
        else:
            print("No valid text extracted.")
            return False, "No selectable text found (possibly scanned image)."
            
    except Exception as e:
        print(f"Failed to process {filename}: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error: {str(e)}"

def ingest_papers():
    print("Starting ingestion...")
    pdf_files = glob.glob(os.path.join(DATA_DIR, "*.pdf"))
    if not pdf_files:
        print(f"No PDFs found in {DATA_DIR}")
        return

    for pdf_path in pdf_files:
        ingest_file(pdf_path)

if __name__ == "__main__":
    ingest_papers()

def ingest_papers():
    print("Starting ingestion...")
    pdf_files = glob.glob(os.path.join(DATA_DIR, "*.pdf"))
    if not pdf_files:
        print(f"No PDFs found in {DATA_DIR}")
        return

    for pdf_path in pdf_files:
        ingest_file(pdf_path)

if __name__ == "__main__":
    ingest_papers()
