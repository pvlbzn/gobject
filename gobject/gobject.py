from enum import Enum


class Gobject(object):
    '''Python object representation of the Google geo API response.'''

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

    class Geometry(object):
        class Location(object):
            '''Third level object: Location.

            Location wraps lat:lng. It provides custom representation
            and equality check. Last one will be particularly useful
            during the class composition.
            '''

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


class ZeroResultsError(Exception):
    '''ZERO_RESULTS exception.
    
    Indicates that the geocode was successful but returned no results.
    This may occur if the geocoder was passed a non-existent address.
    '''
    # duplicate is needed because of features of some code editors such
    # as show docstring on hower.
    msg = ('The geocode was successful but returned no results.'
           ' This may occur if the geocoder was passed'
           ' a non-existent address.')


class OverQueryLimitError(Exception):
    '''OVER_QUERY_LIMIT exception.

    Indicates that you are over your quota.
    '''
    msg = 'Over quota.'


class RequestDeniedError(Exception):
    '''REQUEST_DENIED exception.

    Indicates that your request was denied.
    '''
    msg = 'Request denied'


class InvalidRequestError(Exception):
    '''INVALID_REQUEST exception.

    Generally indicates that the query (address, components or lat:lng)
    is missing.
    '''
    msg = 'Query (address, components, lat, lng) is missing'


class UnknownError(Exception):
    '''UNKNOWN_ERROR exception.

    Indicates that the request could not be processed due to a server error.
    The request may succeed if you try again.
    '''
    msg = 'Server error. Try again.'


class UnsupportedDataTypeError(Exception):
    '''Unsupported data error exception.
    
    Raised when data type / structure is not suitable for the procedure.
    '''
    msg = 'Unsupported data structure'


class Status(Enum):
    OK = 1
    ZERO_RESULTS = 2
    OVER_QUERY_LIMIT = 3
    REQUEST_DENIED = 4
    INVALID_REQUEST = 5
    UNKNOWN_ERROR = 6

    def __init__(self, status):
        self.exception_pool = [
            ZeroResultsError, OverQueryLimitError, RequestDeniedError,
            InvalidRequestError, UnknownError
        ]