''' Superdesk workflow.'''
from superdesk.models import BaseModel
from .support import Cursor
import superdesk
import json
from bson.objectid import ObjectId


WORKFLOW_DEFINITIONS = []


class Workflow(BaseModel):

    workflows = {}

    @classmethod
    def register(cls, definition):
        WORKFLOW_DEFINITIONS.append(definition)
        cls.workflows[definition.id] = {'_id': definition.id, 'name': definition.name}

    endpoint_name = 'workflow'
    schema = {
        'name': {
            'type': 'string'
        }
    }
    resource_methods = ['GET']
    item_methods = ['GET']

    def find_one(self, req, **lookup):
        id_ = lookup.get('_id')
        if not id_: return
        return self.workflows.get(id_)

    def get(self, req, **lookup):
        return Cursor(sorted(self.workflows.values(), key=lambda workflow: workflow['name']),
                      len(self.workflows))

class Workplace(BaseModel):
    endpoint_name = 'workplace'
    schema = {
        'name': {
            'type': 'string',
            'unique': True,
            'required': True,
        },
        'category': {
            'type': 'string'
        },
        'target': {
            'type': 'string'
        },
        'destinations': {
            'type': 'list',
            'schema': {
                'type': 'string',
            }
        },
        'workstation': {
            'type': 'objectid',
            'data_relation': {'resource': 'workstation', 'field': '_id', 'embeddable': True}
        },
        'user': {
            'type': 'objectid',
            'data_relation': {'resource': 'users', 'field': '_id', 'embeddable': True}
        }
    }
    resource_methods = ['GET']
    item_methods = ['GET']
    
    
class Workstation(BaseModel):
    endpoint_name = 'workstation'
    schema = {
        'name': {
            'type': 'string',
            'unique': True,
            'required': True,
        },
        'description': {
            'type': 'string'
        },
        'members': {
            'type': 'list',
            'minlength': 1,
            'schema': {
                'type': 'dict',
                'schema': {
                    'user': {
                        'type': 'objectid',
                        'data_relation': {'resource': 'users', 'field': '_id', 'embeddable': True}
                    },
                    'workflows': {
                        'type': 'list',
                        'schema': {
                            'type': 'string',
                            'data_relation': {'resource': 'workflow', 'field': '_id', 'embeddable': True}
                        }
                    }
                }
            }
        }
    }
    
    def on_created(self, docs):
        self._process_places(docs)

    def on_updated(self, updates, original):
        full = dict(original)
        full.update(updates)
        self._process_places([full])

    def on_replaced(self, document, original):
        self._process_places([document])

    def _process_places(self, docs):
        for doc in docs:
            superdesk.apps[Workplace.endpoint_name].delete({'workstation': doc['_id']}, False)
            places = {}
            if 'members' in doc:
                members = {}
                for member in doc['members']:
                    user_id = member['user']
                    workflows = members.get(user_id)
                    if workflows == None:
                        workflows = members[user_id] = set()
                    workflows.update(member['workflows'])
                
                for definition in WORKFLOW_DEFINITIONS:
                    definition.process(doc['name'], members, places)
            
            dplaces = []
            for place in places.values():
                place['workstation'] = doc['_id']
                dplaces.append(place)
                
            superdesk.apps[Workplace.endpoint_name].create(dplaces)


class Workitem(BaseModel):
    endpoint_name = 'workitem'
    schema = {
        'name': {
            'type': 'string',
            'unique': True,
            'required': True,
            'minlength': 1
        },
        'workplace': {
            'type': 'objectid',
            'data_relation': {'resource': 'workplace', 'field': '_id', 'embeddable': True}
        }
    }
