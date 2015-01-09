from pymongo import MongoClient
from bson.objectid import ObjectId
from contact import Contact

class ContactsRepository(object):
    """ Repository implementing CRUD operations on contacts collection in MongoDB """

    def __init__(self):
        # initializing the MongoClient, this helps to 
        # access the MongoDB databases and collections 
        self.client = MongoClient(host='localhost', port=27017)
        self.database = self.client['contact_db']


    def create(self, contact):
        created_id = None
        if contact is not None:
            created_id = self.database.contacts.insert(contact.get_as_json())            
        else:
            raise Exception("Nothing to save, becuase contact parameter is None")

        return created_id

    def read(self, contact_id=None):
        if contact_id is None:
            return self.database.contacts.find({})
        else:
            return self.database.contacts.find({"_id":contact_id})


    def update(self, contact):
        if contact is not None:
            # the save() method updates the document if this has an _id property 
            # which appers in the collection, otherwise it saces the data
            # as a new document in the collection
            self.database.contacts.save(project.get_as_json())            
        else:
            raise Exception("Nothing to update, becuase contact parameter is None")


    def delete(self, contact):
        if contact is not None:
            self.database.contacts.remove(contact.get_as_json())            
        else:
            raise Exception("Nothing to delete, becuase contact parameter is None")

