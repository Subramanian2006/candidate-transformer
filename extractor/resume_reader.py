import fitz  # PyMuPDF


class ResumeReader:
    """
    Reads a PDF resume and returns its text.
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        try:
            document = fitz.open(self.file_path)

            text = ""

            for page in document:
                text += page.get_text()

            document.close()

            return text

        except Exception as e:
            print(f"[Resume Reader Error] {e}")
            return ""