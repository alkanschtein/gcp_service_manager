from google.cloud import firestore

class FirestoreManager:
    def __init__(self, collection_name):
        # Initialize Firestore client and set the collection reference
        self.db = firestore.Client()
        self.collection_ref = self.db.collection(collection_name)
        
    def create_document_auto_id(self, data):
        # Add document with auto-generated ID
        doc_ref = self.collection_ref.add(data)
        print(f'Document added with ID: {doc_ref[1].id}')
    
    def find_one_document_by_field(self, field_name, value):
        # Query for a single document by a specific field and value
        query = self.collection_ref.where(field_name, '==', value).limit(1)
        results = query.stream()
        
        for doc in results:
            print(f'Found document with ID: {doc.id}')
            return {**doc.to_dict(), 'id': doc.id}
        
        print('No document found with the specified criteria.')
        return None

    def find_documents_by_field(self, field_name, value):
        # Query documents by a specific field and value
        query = self.collection_ref.where(field_name, '==', value)
        results = query.stream()
        
        documents = []
        for doc in results:
            documents.append({**doc.to_dict(), 'id': doc.id})
            print(f'Found document with ID: {doc.id}')
        
        return documents
    
    def find_documents_by_fields(self, field_values):
        """
        Query documents by multiple fields and values.

        Parameters:
        - field_values (dict): A dictionary where keys are field names and values are the desired field values.

        Returns:
        - List of documents that match all the field-value conditions.
        """
        query = self.collection_ref
        
        # Dynamically add where clauses for each field
        for field_name, value in field_values.items():
            query = query.where(field_name, '==', value)
        
        results = query.stream()
        documents = []
        for doc in results:
            documents.append({**doc.to_dict(), 'id': doc.id})
            print(f'Found document with ID: {doc.id}')
        
        return documents

    def get_document_by_id(self, doc_id):
        # Get a document by ID
        doc_ref = self.collection_ref.document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            print(f'Document data exists')
            return doc.to_dict()
        else:
            print('No such document!')
            return None
    
    def get_all_documents(self):
        # Get all documents in the collection
        docs = self.collection_ref.stream()
        all_docs = {doc.id: doc.to_dict() for doc in docs}
        for doc_id, doc_data in all_docs.items():
            print(f'{doc_id}')
        return all_docs
    
    def update_document(self, doc_id, data):
        # Update specific fields in a document
        doc_ref = self.collection_ref.document(doc_id)
        doc_ref.update(data)
        print(f'Document with ID {doc_id} updated.')
    
    def delete_document(self, doc_id):
        # Delete a document by ID
        doc_ref = self.collection_ref.document(doc_id)
        doc_ref.delete()
        print(f'Document with ID {doc_id} deleted.')
