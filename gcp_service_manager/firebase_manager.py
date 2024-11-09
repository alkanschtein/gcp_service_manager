from google.cloud import firestore


class FirestoreManager:
    def __init__(self, collection_name):
        self.db = firestore.Client()
        self.collection_ref = self.db.collection(collection_name)
        
        
    def create_document_auto_id(self, data):
        doc_ref = self.collection_ref.add(data)
        print(f"Document added with ID: {doc_ref[1].id}")
    

    def create_document_with_id(self, doc_id, data):
        self.collection_ref.document(doc_id).set(data)
        print(f"Document with ID {doc_id} created.")
    

    def get_document_by_id(self, doc_id):
        doc_ref = self.collection_ref.document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            print(f"Document Data: {doc.to_dict()}")
            return doc.to_dict()
        else:
            print("No such document!")
            return None
    

    def get_all_documents(self):
        docs = self.collection_ref.stream()
        all_docs = {doc.id: doc.to_dict() for doc in docs}
        for doc_id, doc_data in all_docs.items():
            print(f"{doc_id} => {doc_data}")
        return all_docs
    

    def update_document(self, doc_id, data):
        doc_ref = self.collection_ref.document(doc_id)
        doc_ref.update(data)
        print(f"Document with ID {doc_id} updated.")
    

    def delete_document(self, doc_id):
        doc_ref = self.collection_ref.document(doc_id)
        doc_ref.delete()
        print(f"Document with ID {doc_id} deleted.")
