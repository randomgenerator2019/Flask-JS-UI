
class ModelObject(object):
    '''Demo object for model usage'''
    def __init__(self, api):
        self.counter = 0
        self.model_objects = []
        self.api = api

    def get(self, id):
        '''retrieve model_object from model'''
        for item in self.model_objects:
            if item['id'] == id:
                return item
        self.api.abort(404, "model_object {} doesn't exist".format(id))

    def create(self, data):
        '''create a model_object'''
        data['id'] = self.counter = self.counter + 1
        self.model_objects.append(data)
        return data

    def update(self, id, data):
        ''' Update a model_object'''
        item = self.get(id)
        item.update(data)
        return item

    def delete(self, id):
        ''' Delete a model_object'''
        item = self.get(id)
        self.model_objects.remove(item)
