#pylint: disable=R0903:too-few-public-methods
#pylint: disable=C0114:missing-module-docstring
#pylint: disable=C0304:missing-final-newline
#pylint: disable=C0115:missing-class-docstring


import json
import uuid
from typing import List

class Document:
    def __init__(self,  title, content, categories:List):
        self.id = str(uuid.uuid4())
        self.title = title
        self.content = content
        self.categories = categories

# class Documents:
#     def __init__(self, documents:List[Document]):
#         self.documents = documents


class DocumentService:
    def json_to_documents(self,json_data):
        '''
        converts json structure below to list of documents
        [
            {
            "title": "Document 1",
            "content": "This is the content of Document 1.",
            "categories": ["Category A", "Category B"]
            },
            {
            "title": "Document 2",
            "content": "Content of Document 2 goes here.",
            "categories": ["Category B", "Category C"]
            }
        ]
        '''
        try:
            data = json.loads(json_data)
            documents_data = data#data.get('documents', [])
            # Convert JSON data to a list of Document instances
            documents = [
                Document(doc['title'], doc['content'], doc['categories'])
                for doc in documents_data
            ]
            # Return a Documents instance
            return documents
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None