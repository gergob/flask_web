from bson.objectid import ObjectId
from datetime import datetime

class Contact(object):
    """A class for storing Contact information"""

    def __init__(self, contact_id=None, first_name=None, last_name=None, birthday=None, website=None, home_phone=None, mobile_phone=None, work_phone=None, email=None):
        if contact_id is None:
            self._id = ObjectId()
        else:
            self._id = contact_id
        self.first_name = first_name
        self.last_name = last_name

        if birthday is not None:
            if type(birthday) == datetime:
                self.birthday = birthday
            else: 
                try:
                    tmpBd = datetime.strptime(birthday,"%Y-%m-%dT%H:%M")
                    self.birthday = tmpBd
                except ValueError as e:
                    self.birthday = None
                    print(e)
        else:
            self.birthday = None
        self.website = website
        self.home_phone = home_phone
        self.work_phone = work_phone
        self.mobile_phone = mobile_phone
        self.email = email

    def get_as_json(self):
        """ Method returns the JSON representation of the Contac object, this can be saved to MongoDB """
        return self.__dict__
    

    @staticmethod    
    def build_from_json(json_data):
        """ Method used to build Contact objects from JSON data returned from MongoDB """
        if json_data is not None:
            try:                            
                return Contact(json_data.get('_id', None),
                    json_data['first_name'],
                    json_data['last_name'],
                    json_data['birthday'],
                    json_data['website'],
                    json_data['home_phone'],
                    json_data['mobile_phone'],
                    json_data['work_phone'],
                    json_data['email'])
            except KeyError as e:
                raise Exception("Key not found in json_data: {}".format(e.message))
        else:
            raise Exception("No data to create Contact from!")

