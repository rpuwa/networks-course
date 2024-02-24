import json
from utils import id_generator

class Product:
    def __init__(self, json_body=None):
        self.data = {'id': next(id_generator), 'name': '', 'description': '', 'icon': ''}
        self.update(json_body)
    
    def update(self, json_body=None):
        if json_body != None:
            if 'id' in json_body:
                self.data['id'] = json_body['id']
            if 'name' in json_body:
                self.data['name'] = json_body['name']
            if 'description' in json_body:
                self.data['description'] = json_body['description']
    
    def set_icon(self, icon):
        self.data['icon'] = icon.filename

    def json(self):
        return json.dumps(self.data)
    
    def id(self):
        return self.data['id']
    
    def icon(self):
        return self.data['icon']
    
    def __str__(self):
        return str(self.__dict__)