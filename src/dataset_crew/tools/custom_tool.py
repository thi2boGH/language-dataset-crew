from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import tempfile
import os
from PyPDF2 import PdfReader


class PDFReaderInput(BaseModel):
    """Input schema for PDFReaderTool."""

    pdf_url: str = Field(..., description="URL of the PDF file to read")
    max_pages: int = Field(
        10, description="Maximum number of pages to read (default: 10)"
    )


class PDFReaderTool(BaseTool):
    name: str = "PDF Reader Tool"
    description: str = "A tool that can extract text from PDF files given a URL."
    args_schema: Type[BaseModel] = PDFReaderInput

    def _run(self, pdf_url: str, max_pages: int = 10) -> str:
        """
        Extract text from a PDF file.

        Args:
            pdf_url: URL of the PDF file to read
            max_pages: Maximum number of pages to read (default: 10)

        Returns:
            Extracted text from the PDF
        """
        try:
            # Download the PDF file
            response = requests.get(pdf_url, stream=True)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Create a temporary file to save the PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file_path = temp_file.name
                # Write the PDF content to the temporary file
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)

            # Extract text from the PDF
            text = ""
            try:
                reader = PdfReader(temp_file_path)
                num_pages = min(len(reader.pages), max_pages)

                for i in range(num_pages):
                    page = reader.pages[i]
                    text += f"\n--- Page {i+1} ---\n"
                    text += page.extract_text()

                if len(reader.pages) > max_pages:
                    text += f"\n\n[Note: Only showing first {max_pages} pages out of {len(reader.pages)} total pages]"
            finally:
                # Clean up the temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)

            return text
        except Exception as e:
            return f"Error extracting text from PDF: {str(e)}"
