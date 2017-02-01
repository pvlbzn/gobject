from enum import Enum


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


class Bound(object):
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
        geo = None

        # Check the data type
        if (type(data) == type({})):
            geo = data
        elif (type(data) == type('')):
            geo = json.loads(data)
        else:
            # Data type is not valid
            raise UnsupportedDataTypeError(
                'Provided data type {0} is unsupported'.format(type(data)))

        # Check response status
        if (geo['status'] is not 'OK'):
            try:
                err_msg = geo['error_message']
                status = geo['status']
            except KeyError:
                # Shouldn't be the case, but.. Only option to happen so is 
                # the change in Google geo API.
                raise RequestError('request error')
            finally:
                raise RequestError('status: {0}, error message: {1}'.format(
                    err_msg, status))

        self.address_components = None
        self.formatted_address = None
        self.geometry = None
        self.place_id = None
        self.types = None
