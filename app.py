import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv

from src.parser import parse_document
from src.nlp import extract_entities, highlight_entities
from src.llm import LLMService
from src.risk import calculate_risk_score, get_risk_level
from src.utils import generate_audit_log

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="ContractAI - Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()

# Initialize Session State
if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None
if "contract_text" not in st.session_state:
    st.session_state["contract_text"] = None

# Sidebar
st.sidebar.title("ContractAI ⚖️")
st.sidebar.info("GenAI-powered Contract Analysis & Risk Assessment")

# API Key check
groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    st.sidebar.warning("⚠️ No Groq API Key found in .env! Using mock mode.")

# Navigation
page = st.sidebar.radio("Navigate", ["Dashboard", "Analysis", "Chat Assistant", "Similarity Check", "Templates"])

def render_dashboard():
    st.title("Dashboard")
    st.markdown("### Welcome to ContractAI")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Contracts Analyzed", "12")
    with col2:
        st.metric("High Risk Detected", "2")
    with col3:
        st.metric("Avg Risk Score", "35/100")
        
    st.markdown("---")
    st.subheader("Recent Activity")
    df = pd.DataFrame({
        "Contract Name": ["Vendor_Agreement_v1.pdf", "Employment_JohnDoe.docx", "Lease_Office_BLR.pdf"],
        "Date": ["2023-10-25", "2023-10-24", "2023-10-22"],
        "Risk Level": ["Low", "High", "Medium"]
    })
    st.dataframe(df, use_container_width=True)

def render_analysis():
    st.title("Contract Analysis")
    
    uploaded_file = st.file_uploader("Upload Contract (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    
    # Language Selection
    target_lang = st.sidebar.selectbox("Analysis Language", ["English", "Hindi", "Spanish", "French"])
    
    if uploaded_file:
        if st.button("Analyze Contract"):
            generate_audit_log("User Action", f"Started analysis for {uploaded_file.name}")
            with st.spinner("Parsing and Analyzing..."):
                try:
                    # 1. Parse
                    text = parse_document(uploaded_file)
                    st.session_state["contract_text"] = text
                    
                    # Translation if needed (Mock/Simple)
                    if target_lang != "English":
                        st.info(f"Translating to {target_lang}...")
                        # In reality, we might translate specific parts or the whole thing
                        # For now, let's keep the main text as is but note the language
                        pass
                    
                    # 2. NLP Extraction
                    entities = extract_entities(text)
                    
                    # 3. LLM Analysis
                    llm = LLMService()
                    summary_json = llm.summarize_contract(text)
                    
                    if "error" in summary_json:
                        st.error(f"Analysis Failed: {summary_json['error']}")
                        st.stop()
                    
                    # 4. Clause Analysis
                    from src.nlp import split_into_clauses
                    clauses = split_into_clauses(text)
                    clause_analysis = llm.batch_analyze_clauses(clauses)
                    
                    # 5. Risk Calculation
                    # Use real clause scores if available, else fallback
                    if clause_analysis:
                        risk_score = calculate_risk_score(clause_analysis, summary_json.get("overall_risk", "Medium"))
                    else:
                        clauses_mock = [
                            {"risk_score": summary_json.get("risk_score", 5)},
                            {"risk_score": 2},
                            {"risk_score": 8 if summary_json.get("overall_risk") == "High" else 3}
                        ]
                        risk_score = calculate_risk_score(clauses_mock, summary_json.get("overall_risk", "Medium"))
                    
                    st.session_state["analysis_result"] = {
                        "text": text,
                        "entities": entities,
                        "summary": summary_json,
                        "clauses": clause_analysis,
                        "composite_risk": risk_score,
                        "risk_level": get_risk_level(risk_score)
                    }
                    
                except Exception as e:
                    st.error(f"Error during analysis: {e}")
                    
    # Display Results
    if st.session_state.get("analysis_result"):
        res = st.session_state["analysis_result"]
        
        # Header & PDF Export
        col_h1, col_h2 = st.columns([3, 1])
        with col_h1:
            risk_color = "green"
            if res["risk_level"] == "High" or res["risk_level"] == "Critical":
                risk_color = "red"
            elif res["risk_level"] == "Medium":
                risk_color = "orange"
            st.markdown(f"## Risk Assessment: :{risk_color}[{res['risk_level']} ({res['composite_risk']}/100)]")
        
        with col_h2:
            from src.export import generate_pdf_report
            try:
                pdf_bytes = generate_pdf_report(res)
                st.download_button("📄 Export Report", pdf_bytes, "contract_report.pdf", "application/pdf")
            except Exception as e:
                st.error(f"Export failed: {e}")

        tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Entities", "Clause Analysis", "Translation"])
        
        with tab1:
            st.subheader("Executive Summary")
            st.write(res["summary"].get("summary", "No summary available."))
            
            st.subheader("Key Obligations")
            for ob in res["summary"].get("key_obligations", []):
                st.write(f"- {ob}")
                
        with tab2:
            st.subheader("Extracted Entities")
            st.json(res["entities"])
            
        with tab3:
            st.subheader("Detailed Clause Analysis")
            
            # Dynamic Risk Flags from LLM
            specific_risks = res["summary"].get("specific_risks", {})
            st.markdown("### ⚠️ Critical Alerts")
            if specific_risks:
                if specific_risks.get("has_indemnity"):
                    st.warning("**Indemnity Clause Detected**: This may impose unlimited liability.")
                if specific_risks.get("has_non_compete"):
                    st.warning("**Non-Compete Clause Detected**: Restricts future employment options.")
                if specific_risks.get("has_termination_for_convenience"):
                    st.warning("**Termination for Convenience**: One party can end the contract without cause.")
                if specific_risks.get("has_auto_renewal"):
                    st.info("**Auto-Renewal Detected**: Watch out for the cancellation window.")
            else:
                 st.info("No specific critical alerts detected.")

            st.markdown("---")
            st.markdown("### Clause Breakdown")
            
            clauses = res.get("clauses", [])
            if not clauses:
                st.info("No individual clauses could be parsed. The document might not follow standard numbering.")
            else:
                for clause in clauses:
                    risk = clause.get("risk_score", 0)
                    color = "green"
                    if risk >= 8: color = "red"
                    elif risk >= 5: color = "orange"
                    
                    with st.expander(f"Clause {clause.get('id', '?')} - Risk: :{color}[{risk}/10]"):
                        st.markdown(f"**Original Text**:\n> {clause.get('original_text', '')}")
                        st.markdown(f"**Explanation:** {clause.get('explanation', 'N/A')}")
                        if risk > 3:
                            st.markdown(f"**Risk Reason:** {clause.get('risk_reason', 'N/A')}")
                        if risk > 5:
                            st.markdown(f"**Suggestion:** {clause.get('suggestion', 'N/A')}")
            
        with tab4:
             st.subheader(f"Translation to {target_lang}")
             if st.button(f"Translate Summary to {target_lang}"):
                 llm = LLMService()
                 summary_text = res["summary"].get("summary", "")
                 translated = llm.translate_text(summary_text, target_lang)
                 st.write(translated)

def render_chat():
    st.title("Legal Chat Assistant")
    if st.session_state.get("contract_text"):
        st.success("Contract Context Loaded")
    else:
        st.info("Please analyze a contract first to ask specific questions.")
        
    user_input = st.text_input("Ask a question about the contract:")
    if user_input:
        if st.session_state.get("contract_text"):
            with st.spinner("Consulting AI..."):
                llm = LLMService()
                response = llm.chat_about_contract(st.session_state["contract_text"], user_input)
                st.markdown(f"**AI:** {response}")
        else:
            st.warning("Please upload and analyze a contract first.")

def render_templates():
    st.title("Contract Templates")
    st.write("Download standardized templates.")
    
    col1, col2 = st.columns(2)
    
    import io
    
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            with open("Non Disclosure Agreement (1).docx", "rb") as f:
                nda_data = f.read()
            st.download_button(
                label="Download NDA Template",
                data=nda_data,
                file_name="Standard_NDA.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        except Exception as e:
            st.error(f"Template not found: {e}")
            
    with col2:
        try:
            with open("Employment Agreement template.docx", "rb") as f:
                emp_data = f.read()
            st.download_button(
                label="Download Employment Agreement",
                data=emp_data,
                file_name="Employment_Agreement.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        except Exception as e:
            st.error(f"Template not found: {e}")

# Main Routing
if page == "Dashboard":
    render_dashboard()
elif page == "Analysis":
    render_analysis()
elif page == "Chat Assistant":
    render_chat()
elif page == "Templates":
    render_templates()
elif page == "Similarity Check":
    from src.templates import STANDARD_CLAUSES
    
    st.title("Clause Similarity Check 🔍")
    st.info("Compare your contract's clauses against market-standard 'Fair' versions.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_type = st.selectbox("Select Clause Type", list(STANDARD_CLAUSES.keys()))
        standard_text = STANDARD_CLAUSES[selected_type]
        st.markdown(f"**Standard (Fair) {selected_type}:**")
        st.info(standard_text)
        
    with col2:
        actual_text = st.text_area("Paste Clause from Your Contract", height=150)
        
    if st.button("Compare Clauses"):
        if actual_text:
            with st.spinner("Comparing..."):
                llm = LLMService()
                comparison = llm.compare_clause_with_standard(actual_text, standard_text)
                
                if "error" in comparison:
                    st.error(comparison["error"])
                else:
                    score = comparison.get("similarity_score", 0)
                    color = "green" if score > 70 else "orange" if score > 40 else "red"
                    
                    st.markdown("### Comparison Result")
                    st.markdown(f"**Similarity Score:** :{color}[{score}/100]")
                    st.markdown(f"**Verdict:** {comparison.get('verdict', 'N/A')}")
                    st.write(f"**Deviations:** {comparison.get('deviations', 'N/A')}")
        else:
            st.warning("Please paste a clause to compare.")
