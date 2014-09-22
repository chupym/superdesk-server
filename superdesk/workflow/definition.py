import hashlib
import superdesk
from .support import Request

def hid(value):
    return hashlib.md5(value.encode('utf_8')).hexdigest()[:24]

def tid(value):
    return hashlib.md5(value.encode('utf_8')).hexdigest()
    
class Place:

    def __init__(self, target, name, *destinations, category=None, user='%(user_id)s'):
        self.target = target
        self.name = name
        self.destinations = destinations
        self.category = category
        self.user = user
        self.id = self.target + user

    def identifier(self, markers):
        return hid(self.id % markers)

    def create(self, markers):
        place = {
            'target': tid(self.target % markers),
            'name': self.name % markers,
            'user': self.user % markers,
            'destinations': []}
        if self.category:
            place['category'] = self.category % markers
        return place

    def update(self, place, markers):
        destinations = place['destinations']
        for dtarget in self.destinations:
            dtarget = dtarget % markers
            if dtarget not in destinations:
                destinations.append(tid(dtarget))

class Definition:

    def __init__(self):
        self.id = hid(self.__class__.__name__)
        # We need to create 24 char long ids in order to be recognized by get item.

    def process(self, desk_name, members, places):
        markers = {'desk_name': desk_name}
        self._populate(self.id, self.places, markers, members, places)

    def _populate(self, did, pdefinition, markers, members, places):
        for user_id, workflows in members.items():
            if did not in workflows: continue
            markers['user_id'] = user_id
            markers['user_name'] = superdesk.get_resource_service('users').find_one(Request(), _id=user_id)['username']

            for pdefin in pdefinition:
                iden = pdefin.identifier(markers)
                place = places.get(iden)
                if place == None:
                    place = places[iden] = pdefin.create(markers)
                pdefin.update(place, markers)


class CopyTasting(Definition):
    name = 'Copy Tasting'

    places = [
        Place('ingest', 'Ingest',
              'spike', 'interesting', '%(desk_name)s'),
        Place('spike', 'Spike',
              'interesting', '%(desk_name)s'),
        Place('interesting', 'Interesting',
              'spike', '%(desk_name)s'),
        Place('%(desk_name)s', '%(desk_name)s')
    ]


class Journalist(Definition):
    name = 'Journalist'

    places = [
        Place('%(desk_name)s %(user_name)s', 'TODO in %(desk_name)s',
              'done', category='%(desk_name)s'),
        Place('done', 'Done')
    ]
    
class WebEditor(Definition):
    name = 'Web editor'

    places = [
        Place('%(desk_name)s %(user_name)s', 'TODO in %(desk_name)s',
              'done', category='%(desk_name)s'),
        Place('done', 'Done')
    ]

class ChiefEditor(Definition):
    name = 'Chief Editor'

    places = [
        Place('%(desk_name)s', '%(desk_name)s',
              '%(desk_name)s %(journalist_name)s'),
        Place('done', 'Done'),
        Place('%(desk_name)s %(journalist_name)s', '%(journalist_name)s in %(desk_name)s',
              '%(desk_name)s')
    ]
    places_journalist = [
        Place('%(desk_name)s', '%(desk_name)s',
              '%(desk_name)s %(journalist_name)s')
    ]

    def __init__(self):
        super().__init__()
        self.id_journalist = hid(Journalist.__name__)

    def process(self, desk_name, members, places):
        for user_id, workflows in members.items():
            if self.id_journalist not in workflows: continue
            markers = {'desk_name': desk_name, 'journalist_id': user_id}
            markers['journalist_name'] = superdesk.get_resource_service('users').find_one(Request(), _id=user_id)['username']
            self._populate(self.id, self.places, markers, members, places)


