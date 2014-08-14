
class CopyTasting:
    name = 'Copy Tasting'

    places = {
        'input': {
            'name': 'Copy Tasting'
        },
        'spike': {
            'name': 'Spike'
        },
        'interesting': {
            'name': 'Interesting'
        },
        'output': {
            'name': 'Valid'
        }
    }

    relations = {
        'input': [
            'spike',
            'interesting',
            'output'
        ],
        'spike': [
            'interesting',
            'output'
        ],
        'interesting': [
            'spike',
            'output'
        ]
    }

    def process(self, users_ids, places, users_places):
        places.update({id_: place['name'] for id_, place in self.places.items()})


class ChiefEditor:
    name = 'Chief Editor'

    places = {
        'unassigned': {
            'name': 'Unassigned'
        },
        'output': {
            'name': 'Done'
        }
    }

    relations = {
        'input': [
            'output'
        ]
    }

    def process(self, users_ids, places, users_places):
        places.update({id_: place['name'] for id_, place in self.places.items()})
