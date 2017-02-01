'''gobject.py'''

from .exception import Status, UnsupportedDataTypeError


class Location(object):
    def __init__(self, coordinates):
        self.lat = coordinates['lat']
        self.lng = coordinates['lng']

    def __repr__(self):
        return '<lat: {0} ; lng: {1}>'.format(self.lat, self.lng)

    def __eq__(self, other):
        i = (self.lat == other.lat)
        j = (self.lng == other.lng)

        if (i and j):
            return True
        else:
            return False


class AddressComponent(object):
    def __init__(self, long_name, short_name, types):
        self.long_name = long_name
        self.short_name = short_name
        self.types = types

    def __repr__(self):
        return '<long name: {0}, short name: {1}, types: {2}>'.format(
            self.long_name, self.short_name, self.types)

    def __eq__(self, other):
        i = (self.long_name == other.long_name)
        j = (self.short_name == other.short_name)
        k = (self.types == other.types)

        if (i and j and k):
            return True
        else:
            return False


class GeoPair(object):
    '''Wraps two named coordinate pairs.

    Bounds and viewport is essentially one data structure with different names.
    This data holds two coordinates: northeas and southwest.
    '''

    def __init__(self, northeast, southwest):
        self.northeast = Location(northeast)
        self.southwest = Location(southwest)

    def __repr__(self):
        return 'northeast: {0}, southwest: {1}'.format(self.northeast,
                                                       self.southwest)

    def __eq__(self, other):
        i = (self.northeast == other.northeast)
        j = (self.southwest == other.southwest)

        if (i and j):
            return True
        else:
            return False


class Gobject(object):
    def __init__(self, data):
        '''
        Args:
            data: google geoservice API response in form of JSON string or object
        
        Raises:
            TODO
        '''
        geo = None

        # check data format
        if (type(data) == type({})):
            geo = data
        elif (type(data) == type('')):
            geo = json.loads(data)
        else:
            raise UnsupportedDataTypeError(
                'Provided data type {0} is unsupported'.format(type(data)))

        # check response status
        if (geo['status'] != Status.OK.name):
            for s in Status:
                if (geo['status'] == s.name):
                    raise Status.exception_pool[s.name]()
