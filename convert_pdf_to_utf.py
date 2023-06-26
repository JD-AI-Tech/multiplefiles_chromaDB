import os
from PyPDF2 import PdfReader, PdfWriter
#from PyPDF2 import PdfFileReader, PdfFileWriter

def convert_utf8_to_cp1252_pdf(input_directory, output_directory):
    try:
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Get a list of PDF files in the input directory
        pdf_files = [f for f in os.listdir(input_directory) if f.endswith('.pdf')]

        for file in pdf_files:
            input_path = os.path.join(input_directory, file)
            output_path = os.path.join(output_directory, file)

            # Open the input PDF file
            with open(input_path, 'rb') as f:
                pdf = PdfReader(f)
               # pdfdoc = PyPDF2.PdfFileReader(sample_pdf)
                output_pdf = PdfWriter()

                # Iterate over each page of the input PDF
                for page_num in range (pdf.pages):
                    page = pdf.getPage(page_num)

                    # Extract the text content from the page
                    text = page.extract_text()

                    # Convert the text from UTF-8 to CP1252 encoding
                    text = text.encode('cp1252', errors='replace').decode('cp1252')

                    # Update the page content with the converted text
                    page.merge_text(text)

                    # Add the updated page to the output PDF
                    output_pdf.addPage(page)

                # Save the output PDF to the specified location
                with open(output_path, 'wb') as output_file:
                    output_pdf.write(output_file)

        print('Conversion completed successfully.')
    except Exception as e:
        print(f'An error occurred: {str(e)}')

# Example usage
if __name__ == "__main__":

    input_dir = './testdata/architect/'
    output_dir = './testdata/architect/converted/'

    #"./testdata/architect/", "./testdata/architect/converted/"
    convert_utf8_to_cp1252_pdf(input_dir, output_dir)
