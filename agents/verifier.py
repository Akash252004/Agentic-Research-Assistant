class VerifierAgent:
    def verify(self, chunks):
        """
        Filters and verifies retrieved chunks.
        Removes duplicates and low-score chunks.
        """
        seen_content = set()
        verified_chunks = []
        
        for chunk in chunks:
            content = chunk.get('metadata', {}).get('text', '')
            score = chunk.get('score', 0)
            
            # De-duplication
            if content in seen_content:
                continue
            
            # Simple threshold correlation
            if score < 0.3: # Adjustable threshold
                continue
                
            seen_content.add(content)
            verified_chunks.append(chunk)
            
        return verified_chunks
