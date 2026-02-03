import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class PlannerAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    def plan(self, user_query):
        """
        Decomposes the user query into sub-queries for better retrieval.
        """
        system_prompt = """
        You are a Planner Agent for a Nuclear Physics research assistant.
        Your goal is to break down complex user queries into atomic, retrieval-friendly sub-queries.
        1. For simple definition/fact questions, generate 2-3 sub-queries max.
        2. For complex comparisons, generate 3-5 sub-queries.
        Do not answer the question. Only output the list of sub-queries, one per line.
        """
        
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Decompose this query: {user_query}"}
            ],
            model="llama-3.3-70b-versatile",
        )
        
        sub_queries = response.choices[0].message.content.strip().split('\n')
        # clean up bullet points if present
        clean_queries = [q.strip('- ').strip() for q in sub_queries if q.strip()]
        return clean_queries
