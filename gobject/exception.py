'''exception.py

Container for API errors. Google API errors:
    - ZeroResultsError
    - OverQueryLimitError
    - RequestDeniedError
    - InvalidRequestError
    - UnknownError

They have supporting class Status. Status is the 1st level container
of Google geo API JSON response, it counterparts to result container.

Note: docstring is needed, despite that explanation mostly duplicated
      in msg class variable because of various helpers in code editors,
      sometimes they show docstring on hover.
'''


class ZeroResultsError(Exception):
    '''ZERO_RESULTS exception.
    
    Indicates that the geocode was successful but returned no results.
    This may occur if the geocoder was passed a non-existent address.
    '''
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
