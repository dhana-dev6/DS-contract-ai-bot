def calculate_risk_score(clauses_analysis, overall_llm_risk):
    """
    Calculates a composite risk score based on clause-level risks and overall assessment.
    
    Args:
        clauses_analysis (list): List of dicts containing risk_score for clauses.
        overall_llm_risk (str): "Low", "Medium", "High" from LLM.
    
    Returns:
        int: Composite score 0-100.
    """
    base_score = 0
    if overall_llm_risk.lower() == "high":
        base_score = 70
    elif overall_llm_risk.lower() == "medium":
        base_score = 40
    else:
        base_score = 10
        
    # Add penalty for high-risk clauses
    high_risk_clauses = [c for c in clauses_analysis if c.get('risk_score', 0) >= 8]
    medium_risk_clauses = [c for c in clauses_analysis if 5 <= c.get('risk_score', 0) < 8]
    
    base_score += (len(high_risk_clauses) * 10)
    base_score += (len(medium_risk_clauses) * 5)
    
    return min(100, base_score)

def get_risk_level(score):
    if score >= 80:
        return "Critical"
    elif score >= 60:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"
