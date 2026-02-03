import os
from sentence_transformers import SentenceTransformer
from endee import Endee

class RetrieverAgent:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2') 
        try:
            self.client = Endee(token="")
            endee_url = os.getenv("ENDEE_API_URL", "http://localhost:8080/api/v1")
            self.client.set_base_url(endee_url)
            
            try:
                self.index = self.client.get_index("nuclear_papers")
            except Exception:
                print("Index 'nuclear_papers' not found (retriever), creating it...")
                self.client.create_index(
                    name="nuclear_papers",
                    dimension=384,
                    space_type="cosine",
                    version=1
                )
                self.index = self.client.get_index("nuclear_papers")

        except Exception as e:
            print(f"Error connecting to Endee: {e}")
            self.index = None

    def retrieve(self, query):
        """
        Embeds the query and searches the Endee database.
        """
        if not self.index:
            print("Index not available.")
            return []
            
        query_embedding = self.model.encode(query).tolist()
        
        try:
            # Endee library query method
            results = self.index.query(
                vector=query_embedding,
                top_k=5,
                include_vectors=False
            )
            
            # Reformat results to match what the Synthesizer expects
            # Library returns list of dicts: {'id':..., 'similarity':..., 'meta':...}
            formatted_results = []
            for res in results:
                formatted_results.append({
                    "score": res.get("similarity"),
                    "metadata": res.get("meta", {})
                })
                
            return formatted_results
            
        except Exception as e:
            print(f"Error retrieving for query '{query}': {e}")
            return []
