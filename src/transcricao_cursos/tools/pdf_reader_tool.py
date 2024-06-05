import requests
import fitz  # PyMuPDF
from crewai_tools import BaseTool

class PDFReaderTool(BaseTool):
    name: str = "PDFReaderTool"
    description: str = "Fetches and reads a PDF from a given URL, extracting readable text."

    def _run(self, pdf_url: str) -> str:
        try:
            # Fetch the PDF from the URL
            response = requests.get(pdf_url)
            response.raise_for_status()
            
            # Load the PDF into PyMuPDF
            pdf_document = fitz.open("pdf", response.content)
            
            # Extract text from the PDF
            text = ""
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text += page.get_text()
            
            return text
        except requests.exceptions.RequestException as e:
            return f"Failed to fetch PDF: {e}"
        except Exception as e:
            return f"An error occurred while processing the PDF: {e}"

# Example usage
"""
if __name__ == "__main__":
    tool = PDFReaderTool()
    pdf_url = "http://www.example.com/sample.pdf"
    result = tool._run(pdf_url)
    print(result)
"""
