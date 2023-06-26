import os
import codecs

def convert_directory_text_files(input_dir, output_dir):
    try:
        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Iterate over all files in the input directory
        for filename in os.listdir(input_dir):
            if filename.endswith('.txt'):
                input_file = os.path.join(input_dir, filename)
                output_file = os.path.join(output_dir, filename)

                try:
                    convert_text_utf8_to_cp1252(input_file, output_file)
                    print(f"File converted: {filename}")
                except Exception as e:
                    print(f"Error converting file: {filename}. Error: {str(e)}")
    except Exception as e:
        print(f"Error converting directory: {str(e)}")

def convert_text_utf8_to_cp1252(input_file, output_file):
    try:
        with codecs.open(input_file, 'r', 'utf-8') as f_in:
            text = f_in.read()

        with codecs.open(output_file, 'w', 'cp1252') as f_out:
            f_out.write(text)
    except Exception as e:
        raise Exception(f"Error converting file: {str(e)}")


#usage:
if __name__ == "__main__":
    convert_directory_text_files("./testdata/news_articles/", "./testdata/news_articles/converted/")