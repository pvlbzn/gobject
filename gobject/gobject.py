'''gobject.py'''

import json

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

    def __dict__(self):
        return {'lat': self.lat, 'lng': self.lng}


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

    def __dict__(self):
        return {
            'long_name': self.long_name,
            'short_name': self.short_name,
            'types': self.types
        }


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

    def __dict__(self):
        return {
            'northeast': self.northeast.__dict__(),
            'southwest': self.southwest.__dict__()
        }


class Gobject(object):
    def __init__(self, data=None):
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

        geo = geo['results'][0]

        self.address_components = self._parse_addr(geo['address_components'])
        self.formatted_address = geo['formatted_address']
        self.bounds = self._parse_geopair(geo['geometry']['bounds'])
        self.location = self._parse_location(geo['geometry']['location'])
        self.viewport = self._parse_geopair(geo['geometry']['viewport'])
        self.location_type = geo['geometry']['location_type']
        self.place_id = geo['place_id']
        self.types = geo['types']

    def _parse_addr(self, data):
        res = []

        for addr in data:
            res.append(
                AddressComponent(addr['long_name'], addr['short_name'], addr[
                    'types']))

        return res

    def _parse_geopair(self, data):
        return GeoPair(data['northeast'], data['southwest'])

    def _parse_location(self, data):
        return Location(data)

    def serialize(self):
        '''Inverse the data back to its initial JSON format.
        
        Serialize is an inverse function on object, it maps object back
        to initial data format. That makes Gobject instance behave like
        a bijecive function.
        '''
        pass

    def __repr__(self):
        # Get representation of each component.
        components = []
        for component in self.address_components:
            components.append(component.__repr__())

        addr = '<<address_components: {}>, '.format(components)
        fmt = '<formatted_address: {0}>, '.format(self.formatted_address)
        geo = '<geometry: <bounds: {0}>, '.format(self.bounds)
        loc = '<location:{0}>, '.format(self.location)
        loct = '<location_type: {0}>, '.format(self.location_type)
        view = '<viewport: {0}>>, '.format(self.viewport)
        pid = '<place_id: {0}>, '.format(self.place_id)
        types = '<types: {0}>>'.format(self.types)

        return addr + fmt + geo + loc + loct + view + pid + types

    def __dict__(self):
        components = []
        for component in self.address_components:
            components.append(component.__dict__())
