''' Superdesk workflow.'''

from superdesk.base_model import BaseModel

WORKFLOW_DEFINITIONS = []

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

class Workflow(BaseModel):

    workflows = {}

    @classmethod
    def register(cls, definition):
        id_ = definition.__class__.__name__
        WORKFLOW_DEFINITIONS.append((id_, definition))
        cls.workflows[id_] = {'_id': id_, 'name': definition.name}

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
        return Cursor(sorted(self.workflows.values()), len(self.workflows))


class Workplace(BaseModel):
    endpoint_name = 'workplace'
    schema = {
        'name': {
            'type': 'string',
            'unique': True,
            'required': True,
        },
        'workstation': {
            'type': 'objectid',
            'data_relation': {'resource': 'workstation', 'field': '_id', 'embeddable': True}
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

    def __init__(self, app, model_workplace, endpoint_schema=None):
        BaseModel.__init__(self, app, endpoint_schema=endpoint_schema)
        self.model_workplace = model_workplace

    def on_created(self, docs):
        self._process_places(docs)

    def on_updated(self, updates, original):
        self._clear_places(original['_id'])
        self._process_places([updates])

    def on_replaced(self, document, original):
        self._clear_places(original['_id'])
        self._process_places([document])

    def on_deleted(self, doc):
        self._clear_places(doc['_id'])

    def _clear_places(self, id_):
        req = Request(max_results=None, page=0, sort=None, where=None,
                      projection=None, if_modified_since=None)
        for doc in self.model_workplace.get(req, {'workstation': id_}):
            # TODO: remove
            print(doc)

    def _process_places(self, docs):
        for doc in docs:
            if 'workflows' not in doc: continue
            
            places = {}
            users_places = {}
            for id_, definition in WORKFLOW_DEFINITIONS:
                users_ids = []
                for user_id, workflows_ids in doc['workflows'].items():
                    if id_ in workflows_ids:
                        users_ids.append(user_id)
                if not users_ids: continue
                definition.process(users_ids, places, users_places)
            
            if places:
                workplaces = []
                for name in places.values():
                    workplaces.append({'name': name, 'workstation': doc['_id']})
                self.model_workplace.create(workplaces)
                print(workplaces)


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


def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

# 1. list workflows
# 1. create desk (setup desk with user and workflow)
# 2. get items in a node (node id = desk_id/node name)
# 3. get available destinations nodes for an item at a specific node and user
# 4. move/copy/link item to a destination node
#
#
# 1. list nodes of a user
# 2. list tasks in a node
# 3. list destination nodes
