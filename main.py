from src.utils import convert_pdf_to_images

# Example usage
if __name__ == "__main__":
    input_pdf = "./sources/novartis-jpm25.pdf"  # Replace with your PDF path
    # output_folder = "output_images" # No longer needed
    convert_pdf_to_images(input_pdf)
