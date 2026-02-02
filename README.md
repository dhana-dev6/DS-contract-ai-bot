# ⚖️ ContractAI - GenAI Legal Assistant

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/AI-Groq_Llama3-orange?style=for-the-badge)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**A sophisticated, GenAI-powered Data Science dashboard for SME contract analysis.**  
*Built for the Data Science Hackathon 2024.*

---

![Dashboard Preview](https://via.placeholder.com/1200x600?text=ContractAI+Dashboard+Screenshot)
*(Upload your `uploaded_media_1770010393328.png` to the repo as `dashboard.png` and update this link!)*

## 🚀 Overview

**ContractAI** transforms complex legal documents into clear, actionable insights. By leveraging **Large Language Models (LLMs)** and **Natural Language Processing (NLP)**, it bridges the gap between unstructured legal text and quantitative risk assessment.

### Why Data Science? 🧬
This project isn't just a wrapper. It implements a full **NLP Pipeline**:
*   **ETL**: Ingests PDF/DOCX.
*   **NER**: Extracts Parties & Dates using Spacy.
*   **Vector Logic**: Calculates weighted Risk Scores.
*   **Semantic Search**: Compares clauses against a Golden Source.

## ✨ Key Features

*   **📄 Universal Parsing**: Supports text extraction from PDF, DOCX, and TXT files.
*   **🤖 Clause-by-Clause Analysis**: Breaks down contracts into individual clauses and explains them in plain English.
*   **⚠️ Specific Risk Detection**: Automatically flags critical risks like *Indemnity*, *Non-Compete*, and *Termination for Convenience*.
*   **⚖️ Similarity Check**: Compares your user clauses against "Gold Standard" fair clauses to detect deviations.
*   **🇮🇳 Indian Law Context**: AI reasoning tailored to Indian Contract Act compliance.
*   **📊 Risk Scoring**: Calculates a composite risk score (0-100) based on clause severity.
*   **📁 Smart Templates**: Download standardized, pre-vetted legal templates.
*   **🔍 Audit Trail**: Logs all analysis actions for compliance and tracking.

## 🛠️ Tech Stack & Methodology

| Component | Technology | Role |
| :--- | :--- | :--- |
| **LLM** | **Llama 3 70B (via Groq)** | Core legal reasoning, summarization, and risk assessment. |
| **NLP** | **Spacy (`en_core_web_sm`)** | Named Entity Recognition (NER) for parties, dates, and money. |
| **Frontend** | **Streamlit** | Interactive web dashboard and UI. |
| **Parser** | **PDFPlumber / Python-Docx** | ETL pipeline for ingesting unstructured documents. |
| **Architecture** | **Hybrid NLP** | Combines Rule-based Regex (Clause splitting) with Generative AI. |

## ⚙️ Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/YOUR_USERNAME/contract-ai-bot.git
    cd contract-ai-bot
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    ```

3.  **Set up Environment Variables**
    Create a `.env` file in the root directory and add your Groq API key:
    ```
    GROQ_API_KEY=your_groq_api_key_here
    ```

4.  **Run the Application**
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure

```
├── app.py                  # Main Streamlit Dashboard application
├── src/
│   ├── llm.py              # LLM Service (Groq integration)
│   ├── nlp.py              # Spacy NLP & Clause Splitting logic
│   ├── risk.py             # Risk Scoring Algorithm
│   ├── parser.py           # PDF/DOCX Parsing Utilities
│   ├── templates.py        # Standard Clause Knowledge Base
│   └── export.py           # PDF Report Generation
├── samples/                # Sample contracts for testing
├── requirements.txt        # Python dependencies
└── style.css               # Custom UI styling
```

## 👨‍💻 Data Science Approach

This project implements a full Data Science pipeline:
1.  **Data Ingestion**: Unstructured text loading.
2.  **Preprocessing**: Text normalization and regex segmentation.
3.  **Inference**: Zero-shot classification and semantic reasoning via LLMs.
4.  **Quantification**: Mapping qualitative text to quantitative risk vectors.

## 📄 License
This project is open-source and available under the MIT License.
