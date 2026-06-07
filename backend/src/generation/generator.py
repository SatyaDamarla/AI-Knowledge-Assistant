import os
from dotenv import load_dotenv
import google.generativeai as genai


class Generator:
    """
    Gemini-based generator:
    - Query rewriting (for better retrieval)
    - Final answer generation
    """

    def __init__(self, model_name: str = "models/gemini-2.5-flash"):
        load_dotenv()

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is missing from .env")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    
    #  Query Rewriting
    
    def rewrite_query(self, query: str) -> str:
        prompt = f"""
Rewrite the user's query to be explicit and suitable for searching inside a document.

Examples:
"name" → "What is the name mentioned in the document?"
"education" → "What education details are listed in the document?"

Only return the rewritten query.

Query:
{query}

Rewritten:
""".strip()

        try:
            response = self.model.generate_content(prompt)

            if hasattr(response, "text") and response.text:
                return response.text.strip()

            return query

        except:
            return query

    
    def generate(self, query: str, context: str) -> str:
        prompt = self._build_prompt(query, context)

        try:
            response = self.model.generate_content(prompt)

            # Handle multiple Gemini response formats
            if hasattr(response, "text") and response.text:
                return response.text.strip()

            # fallback: extract from candidates
            if hasattr(response, "candidates") and response.candidates:
                parts = response.candidates[0].content.parts
                text = "".join([p.text for p in parts if hasattr(p, "text")])

                if text:
                    return text.strip()

            return "I couldn't generate a proper answer from the model."

        except Exception as e:
            print("GENERATION ERROR:", e)
            return "Error generating response."
    
    def _build_prompt(self, query: str, context: str) -> str:
        return f"""
You are a grounded AI assistant.

Answer the question ONLY using the provided context.

If the answer is not explicitly present, say:
"I don't have enough information in the provided sources."

Keep answers short and precise.

Context:
{context}

Question:
{query}

Answer:
""".strip()