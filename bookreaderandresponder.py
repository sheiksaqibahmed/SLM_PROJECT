import os
from transformers import pipeline
from PyPDF2 import PdfReader
from docx import Document

class SmallLanguageModel:
    def _init_(self):
        # Load a pre-trained question-answering model
        self.qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

    def read_file(self, file_path):
        """Reads the content of a file based on its type."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        elif file_path.endswith('.pdf'):
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        else:
            raise ValueError("Unsupported file format. Please use .txt, .pdf, or .docx files.")

    def answer_question(self, context, question):
        """Uses the QA model to answer a question based on the provided context."""
        result = self.qa_pipeline(question=question, context=context)
        return result['answer']

def main():
    slm = SmallLanguageModel()

    # Prompt user for file path
    file_path = input("Enter the path to the file: ")

    try:
        # Read the file content
        context = slm.read_file(file_path)
        print(f"File loaded successfully. Context length: {len(context)} characters.\n")

        while True:
            # Ask the user for a question
            question = input("Ask a question about the file (type 'exit' to quit): ")
            if question.lower() == 'exit':
                break

            # Get the answer
            answer = slm.answer_question(context, question)
            print(f"Answer: {answer}\n")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()