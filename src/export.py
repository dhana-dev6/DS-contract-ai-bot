from fpdf import FPDF
import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'ContractAI - Legal Risk Assessment Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(analysis_result):
    """
    Generates a PDF report from the analysis result.
    Returns bytes of the PDF.
    """
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    def clean_text(text):
        """Sanitizes text to be latin-1 compatible."""
        if not text: return ""
        # Replace common unicode chars causing issues
        replacements = {
            '\u2013': '-', '\u2014': '-', '\u201c': '"', '\u201d': '"',
            '\u2018': "'", '\u2019': "'", '\u2022': '*', '\u2011': '-'
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        # Final safety net
        return text.encode('latin-1', 'replace').decode('latin-1')

    # Title Info
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Analysis Date: {datetime.date.today()}", 0, 1)
    pdf.ln(5)
    
    # Risk Score
    score = analysis_result.get('composite_risk', 'N/A')
    level = analysis_result.get('risk_level', 'N/A')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, clean_text(f"Overall Risk Score: {score}/100 ({level})"), 0, 1)
    
    # Summary
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Executive Summary", 0, 1)
    pdf.set_font("Arial", size=10)
    summary_text = analysis_result.get('summary', {}).get('summary', 'No summary.')
    pdf.multi_cell(0, 10, clean_text(summary_text))
    
    # Key Obligations
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Key Obligations", 0, 1)
    pdf.set_font("Arial", size=10)
    for ob in analysis_result.get('summary', {}).get('key_obligations', []):
        pdf.multi_cell(0, 10, clean_text(f"- {ob}"))
        
    return pdf.output(dest='S').encode('latin-1', 'replace')
