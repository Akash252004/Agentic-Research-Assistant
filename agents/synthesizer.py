import os
from groq import Groq

class SynthesizerAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def synthesize(self, query, verified_chunks):
        """
        Generates the final answer with citations.
        """
        context_str = ""
        for i, chunk in enumerate(verified_chunks):
            meta = chunk.get('metadata', {})
            source = f"{meta.get('filename', 'unknown')} (p. {meta.get('page_number', '?')})"
            text = meta.get('text', '')
            context_str += f"Source {i+1} [{source}]:\n{text}\n\n"
            
        system_prompt = """
        You are an expert AI Research Assistant. Your goal is to provide a comprehensive, evidence-backed answer.
        
        Guidelines:
        1. **Structure**: Start with a direct summary. Then, use bullet points to detail key facts or concepts comfortably.
        2. **Narrative**: Ensure the answer flows logically and professionally. Do not just list disconnected facts.
        3. **Citations**: STRICTLY cite your source at the end of every claim using the format `[filename, p. X]`.
        4. **Honesty**: If the context does not contain the answer, say "I cannot find the answer in the provided documents."
        """
        
        user_prompt = f"Query: {query}\n\nContext:\n{context_str}"
        
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
        )
        
        return response.choices[0].message.content
