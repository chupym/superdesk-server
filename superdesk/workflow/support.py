''' Support classes.'''

class Cursor:

    def __init__(self, documents, total_size):
        self.documents = documents
        self.total_size = total_size

    def __iter__(self):
        return iter(self.documents)

    def count(self, **kwargs):
        return self.total_size


class Request:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.projection = None
        
    def __getattr__(self, name):
        return