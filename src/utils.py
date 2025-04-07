import os
import pypdfium2 as pdfium
import pathlib
from PIL import Image  # Import PIL Image

# Configuration
HIGH_DPI = 600                    # Initial high DPI for maximum fidelity
MEDIUM_DPI = 400
LOW_DPI = 300                # Fallback DPI if file exceeds 7MB
MAX_SIZE_BYTES = 7 * 1024 * 1024  # 7 MB in bytes


def render_page_to_png(page, dpi, output_path, mode="RGB"):
    """
    Render a single PDF page at the specified DPI and save as an optimized PNG.
    Returns the file size in bytes after saving.
    """
    # Convert DPI to PDFium's scale factor
    scale = dpi / 72

    # Render the page bitmap at the chosen scale
    bitmap = page.render(scale=scale, rotation=0)

    # Convert to a PIL Image
    pil_image = bitmap.to_pil()

    # Convert either to 'RGB' or 'L' (grayscale)
    pil_image = pil_image.convert(mode)
    pil_image.save(output_path, format="PNG")

    # Return the file size
    return os.path.getsize(output_path)


def convert_pdf_to_images(pdf_path: str):
    # Extract filename without extension
    file_name = pathlib.Path(pdf_path).stem
    output_dir = os.path.join("output", f"{file_name}_images")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Open the PDF
    pdf = pdfium.PdfDocument(pdf_path)
    num_pages = len(pdf)

    print(f"Processing '{pdf_path}' ({num_pages} pages)...")

    for i in range(num_pages):
        page = pdf[i]
        page_number = i + 1
        output_path = os.path.join(output_dir, f"page_{page_number:03d}.png")

        # Step 1: Render at HIGH_DPI and check size
        file_size = render_page_to_png(page, HIGH_DPI, output_path, mode="RGB")

        if file_size > MAX_SIZE_BYTES:
            print(f"Warning: Even at {MEDIUM_DPI} DPI, page {page_number} is {file_size / (1024*1024):.2f} MB (>7MB). Trying {LOW_DPI} DPI.")
            file_size = render_page_to_png(page, LOW_DPI, output_path, mode="L")
            if file_size > MAX_SIZE_BYTES:
                print(f"Warning: Even at grayscale {LOW_DPI} DPI, page {page_number} is {file_size / (1024*1024):.2f} MB (>7MB).")
            else:
                print(f"Page {page_number} now {file_size / (1024*1024):.2f} MB at {LOW_DPI} DPI.")
        else:
            print(f"Page {page_number} saved successfully ({file_size / (1024*1024):.2f} MB) at {HIGH_DPI} DPI.")

    pdf.close() # Explicitly close the PDF document
    print("Conversion complete.") 