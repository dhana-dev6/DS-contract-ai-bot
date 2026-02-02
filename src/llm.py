import os
import json
from groq import Groq

class LLMService:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.groq_api_key) if self.groq_api_key else None

    def analyze_clause(self, clause_text, context="General"):
        """
        Analyzes a specific clause for risks and plain language explanation using Groq.
        """
        prompt = f"""
        You are a legal expert specializing in Indian Contract Law. Analyze the following contract clause:
        
        "{clause_text}"
        
        Context: {context}
        
        Provide the output in valid JSON format with the following keys:
        - "explanation": Simple plain English explanation (max 2 sentences).
        - "risk_score": Integer 1-10 (10 being highest risk).
        - "risk_reason": Why is this risky? (If risk > 3).
        - "favorable": "Buyer", "Seller", "Mutual", or "Unknown".
        - "suggestion": Suggestion for improvement if risk > 5.
        """
        return self._call_llm(prompt)

    def summarize_contract(self, full_text):
        """
        Summarizes the entire contract using Groq.
        """
        prompt = f"""
        You are a legal expert specializing in Indian Contract Law. Summarize the following contract text (truncated if necessary):
        
        "{full_text[:15000]}"... [truncated]
        
        Provide the output in valid JSON format with keys:
        - "summary": Executive summary (max 100 words).
        - "contract_type": Type of contract (e.g., NDA, Employment, Lease).
        - "key_dates": List of important dates/deadlines.
        - "key_obligations": List of major obligations for both parties.
        - "overall_risk": Low/Medium/High.
        - "specific_risks": {{
            "has_indemnity": boolean,
            "has_non_compete": boolean,
            "has_termination_for_convenience": boolean,
            "has_auto_renewal": boolean
        }}
        """
        return self._call_llm(prompt)

    def chat_about_contract(self, contract_text, user_question):
        """
        Answers a user question based on the contract text.
        """
        if not self.client:
            return "Local Mode: API Key missing. Unable to answer."
            
        prompt = f"""
        You are a legal assistant. Answer the user's question based strictly on the following contract text.
        If the answer is not in the text, say so. Keep the answer concise and professional.
        
        Contract Text:
        "{contract_text[:25000]}"... [truncated if too long]
        
        User Question: "{user_question}"
        """
        
        try:
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="openai/gpt-oss-120b"
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def translate_text(self, text, target_lang="English"):
        """Translates text using Groq."""
        if not self.client: return f"[Mock Translation to {target_lang}]: {text[:100]}..."
        
        prompt = f"Translate the following legal text to {target_lang}. Maintain legal accuracy:\n\n{text[:2000]}"
        try:
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="openai/gpt-oss-120b"
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def _call_llm(self, prompt):
        """
        Internal dispatcher to call Groq.
        """
        if not self.client:
            return {
                "explanation": "Mock explanation: Groq API key not found.",
                "risk_score": 5,
                "risk_reason": "No Groq API key provided.",
                "summary": "Mock summary: Please provide a Groq API key.",
                "contract_type": "Unknown",
                "overall_risk": "Unknown"
            }
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful and precise legal assistant. Always output JSON."},
                    {"role": "user", "content": prompt}
                ],
                model="openai/gpt-oss-120b",
                response_format={"type": "json_object"}
            )
            return self._clean_json(chat_completion.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}

    def _clean_json(self, text):
        """Helper to extract JSON from text if code blocks are used."""
        try:
            return json.loads(text)
        except:
            # simple attempt to find { ... }
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end != -1:
                try:
                    return json.loads(text[start:end])
                except:
                    pass
            return {"error": f"Failed to parse JSON response. Raw output: {text[:200]}..."}

    def batch_analyze_clauses(self, clauses):
        """
        Analyzes a list of clauses in batch (or a subset to save tokens).
        """
        if not self.client:
            return [{"id": c["id"], "explanation": "Mock analysis.", "risk_score": 1} for c in clauses]

        # For this hackathon/demo, let's analyze the first 5 significant clauses to be fast
        target_clauses = clauses[:5] 
        
        results = []
        for clause in target_clauses:
            # We treat each clause individually or could batch them. 
            # Individual calls are easier to manage for structured output per clause.
            analysis = self.analyze_clause(clause["text"], context=f"Clause {clause['id']}")
            
            # Merge the analysis with the original ID
            if isinstance(analysis, dict):
                analysis["id"] = clause["id"]
                analysis["original_text"] = clause["text"]
                results.append(analysis)
            else:
                results.append({"id": clause["id"], "error": str(analysis)})
                
        return results

    def compare_clause_with_standard(self, actual_clause, standard_clause):
        """
        Compares an actual clause against a standard version.
        """
        if not self.client:
            return {
                "similarity_score": 75,
                "deviations": "Mock: The actual clause is stricter than standard.",
                "verdict": "Fair"
            }
            
        prompt = f"""
        Compare the following two contract clauses.
        
        Standard (Fair) Clause:
        "{standard_clause}"
        
        Actual Clause from Contract:
        "{actual_clause}"
        
        Provide valid JSON output:
        - "similarity_score": Integer 0-100 (how close in intent/fairness).
        - "deviations": Explain key differences (e.g., "Actual clause imposes one-way indemnity instead of mutual").
        - "verdict": "Fair", "Strict", or "Unfavorable".
        """
        return self._call_llm(prompt)
