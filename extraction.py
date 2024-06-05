import json
import re
from document import Document


def extract_document_collection(file_path: str) -> list[Document]:
    """
    Reads a text file and extracts individual fables or stories.
    :param file_path: Path to the text file containing the fables.
    :return: A list of Document objects.
    """
    documents = []  # List to store the Document objects.

    # Open and read the file content
    with open(file_path, 'r') as file:
        content = file.read()

    # Split content into fables based on three consecutive newline characters
    fables = re.split(r'\n\s*\n\s*\n', content)

    # Skip the introductory and table of contents sections
    fables = fables[1:]

    for index, fable in enumerate(fables):
        sections = fable.split('\n\n', 1)
        if len(sections) == 2:
            title = sections[0].strip()
            full_text = sections[1].replace('\n', ' ').strip()
            terms = full_text.split()
            document = Document()
            document.document_id = index
            document.title = title
            document.raw_text = full_text
            document.terms = terms
            documents.append(document)

    return documents


def save_documents_as_json(documents: list[Document], file_path: str) -> None:
    """
    Saves a list of Document objects to a JSON file.
    :param documents: List of Document objects to save.
    :param file_path: Path to the JSON file.
    """
    serializable_docs = []
    for document in documents:
        serializable_docs.append({
            'document_id': document.document_id,
            'title': document.title,
            'raw_text': document.raw_text,
            'terms': document.terms,
            'filtered_terms': document.filtered_terms,
            'stemmed_terms': document.stemmed_terms
        })

    with open(file_path, "w") as json_file:
        json.dump(serializable_docs, json_file)


def load_documents_from_json(file_path: str) -> list[Document]:
    """
    Loads a list of Document objects from a JSON file.
    :param file_path: Path to the JSON file.
    :return: List of Document objects.
    """
    try:
        with open(file_path, "r") as json_file:
            json_collection = json.load(json_file)

        documents = []
        for doc_data in json_collection:
            document = Document()
            document.document_id = doc_data.get('document_id')
            document.title = doc_data.get('title')
            document.raw_text = doc_data.get('raw_text')
            document.terms = doc_data.get('terms')
            document.filtered_terms = doc_data.get('filtered_terms')
            document.stemmed_terms = doc_data.get('stemmed_terms')
            documents.append(document)

        return documents
    except FileNotFoundError:
        print('No existing collection found. Starting with an empty collection.')
        return []
