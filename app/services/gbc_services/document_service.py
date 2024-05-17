#pylint: disable=R0903:too-few-public-methods
#pylint: disable=C0114:missing-module-docstring
#pylint: disable=C0304:missing-final-newline
#pylint: disable=C0115:missing-class-docstring
#pylint: disable=C0303:trailing-whitespace

import re
import json
import uuid
from typing import List
from collections import Counter

class Document:
    def __init__(self,content, categories:List,term_vector):
        self.id = str(uuid.uuid4())
        self.content = content
        self.categories = [category.lower() for category in categories]
        self.term_vector:Counter = term_vector

# class Documents:
#     def __init__(self, documents:List[Document]):
#         self.documents = documents


class DocumentService:
        
    def json_to_doc(self,json_data,string_to_json):
        '''
        converts json structure below to list of documents with their 
        respective termvectors.
        Example:

        doc=

        [
            {
            "content": "This is the content of Document 1.",
            "categories": ["Category A", "Category B"]
            },
           ....
        ]

        [Document(doc['content'], doc['categories'],term_vector(doc))]
        '''
        try:
            if string_to_json:
                data = json_data#json.loads(json_data)
                documents_data = data
                documents = [
                    Document(doc['content'], doc['categories'],self.term_vector(doc['content']))
                    for doc in documents_data
                ]
            else:
                data = json_data
                documents_data = data
                documents = [
                    Document(doc.content, doc.categories,self.term_vector(doc.content))
                    for doc in documents_data
                ]
            # Convert JSON data to a list of Document instances
            
            # Return a Documents instance
            return documents
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
        
    def term_vector(self,doc):
        '''
        converts provided doc to a term_vector
        '''
        
        words = doc.lower().split(" ")
        unique_words = set()      
        for word in words: # Iterate over the words and add them to the set
            unique_words.add(word)
        
        tv = Counter(unique_words)
        # tv=Counter(self._pre_process(doc).split(" "))
        # tv=Counter(doc.lower().split(" "))
        return tv
    def _pre_process(self,text):
        # text = text.lower()
        # remove tags
        text = re.sub("</?.*?>", " <> ", text)  
        # remove special characters and digits
        text = re.sub("(\\d|\\W)+", " ", text)  
        return text