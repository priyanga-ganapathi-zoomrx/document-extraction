import base64
import fitz  # PyMuPDF
import os
from typing import Tuple, List
from .state import DocumentMetadata, Slide
from colorama import Fore, Style

class PDFToolsClass:
    def __init__(self):
        pass
        
    def process_pdf(self, pdf_path: str) -> Tuple[DocumentMetadata, List[Slide]]:
        """
        Process PDF into document metadata and slides.
        """
        print(f"Processing PDF: {pdf_path}")
        
        # Check if file exists
        if not os.path.exists(pdf_path):
            print(Fore.RED + f"Error: PDF file not found at {pdf_path}" + Style.RESET_ALL)
            return DocumentMetadata(
                title="",
                company="",
                date="",
                event="",
                document_id=""
            ), []
            
        try:
            # Load PDF using PyMuPDF
            pdf_document = fitz.open(pdf_path)
            total_pages = len(pdf_document)
            
            print(f"Successfully opened PDF with {total_pages} pages")
            
            # Extract basic metadata
            # Use filename as title and document_id
            filename = os.path.basename(pdf_path)
            title = os.path.splitext(filename)[0]
            
            doc_metadata = DocumentMetadata(
                title=title,
                company="Extracted or provided",
                date="Extracted or provided",
                event="Extracted or provided",
                document_id=pdf_path  # Use file path as document_id
            )
            
            # Process slides
            slides = []
            for page_num in range(total_pages):
                try:
                    page = pdf_document.load_page(page_num)
                    # Higher zoom factor gives better resolution
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    
                    # Convert pixmap to PNG bytes
                    img_bytes = pix.tobytes("png")
                    
                    # Convert to base64
                    img_str = base64.b64encode(img_bytes).decode()
                    
                    # Create slide object (simplified further)
                    slide = Slide(
                        slide_number=page_num + 1,  # 1-indexed for user-friendliness
                        base64_image=img_str
                    )
                    slides.append(slide)
                    print(f"Processed page {page_num + 1}/{total_pages}")
                except Exception as e:
                    print(Fore.RED + f"Error processing page {page_num+1}: {str(e)}" + Style.RESET_ALL)
            
            if not slides:
                print(Fore.RED + "Warning: No slides were extracted from the PDF" + Style.RESET_ALL)
                
            return doc_metadata, slides
            
        except Exception as e:
            print(Fore.RED + f"Error processing PDF: {str(e)}" + Style.RESET_ALL)
            return DocumentMetadata(
                title="",
                company="",
                date="",
                event="",
                document_id=""
            ), []