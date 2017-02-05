import pytest

import json

from gobject import gobject as geo
from gobject import exception


class TestLocation:
    lat = 37.0108489
    lng = -122.0307963
    loc = geo.Location({'lat': lat, 'lng': lng})

    def test_object(self):
        assert self.loc.lat == self.lat and self.loc.lng == self.lng

    def test_representation(self):
        assert self.loc.__repr__() == '<lat: 37.0108489 ; lng: -122.0307963>'

    def test_equality(self):
        assert self.loc == self.loc

    def test_inequality(self):
        other_loc = geo.Location({'lat': 37.010848, 'lng': -122.030796})
        assert self.loc != other_loc

    def test_dict(self):
        assert self.loc.__dict__() == {'lat': self.lat, 'lng': self.lng}


class TestAddressComponent:
    long_name = 'Santa Cruz de Tenerife'
    short_name = 'Santa Cruz de Tenerife'
    types = ['locality', 'political']
    addr = geo.AddressComponent(long_name, short_name, types)

    def test_object(self):
        assert (self.addr.long_name == self.long_name and
                self.addr.short_name == self.short_name and
                self.addr.types == self.types)

    def test_representation(self):
        expected = ('<long name: Santa Cruz de Tenerife,'
                    ' short name: Santa Cruz de Tenerife,'
                    ' types: [\'locality\', \'political\']>')
        assert self.addr.__repr__() == expected

    def test_equality(self):
        assert self.addr == self.addr

    def test_inequality(self):
        other_addr = geo.AddressComponent('long_name', 'short_name', [1, 2])
        assert self.addr != other_addr

    def test_dict(self):
        assert self.addr.__dict__() == {
            'long_name': self.long_name,
            'short_name': self.short_name,
            'types': self.types
        }


class TestGeoPair:
    ne = {'lat': 37.010848, 'lng': -122.030796}
    sw = {'lat': 32.234532, 'lng': -123.123442}
    geopair = geo.GeoPair(ne, sw)

    def test_object_equality(self):
        assert (self.geopair.northeast.lat == self.ne['lat'] and
                self.geopair.northeast.lng == self.ne['lng'] and
                self.geopair.southwest.lat == self.sw['lat'] and
                self.geopair.southwest.lng == self.sw['lng'])

    def test_representation(self):
        expected = ('<northeast: <lat: 37.010848 ; lng: -122.030796>,'
                    ' southwest: <lat: 32.234532 ; lng: -123.123442>>')

    def test_equality(self):
        assert self.geopair == (geo.GeoPair(self.ne, self.sw))

    def test_dict(self):
        assert self.geopair.__dict__() == {
            'northeast': self.ne,
            'southwest': self.sw
        }


class TestGobject:
    data = None

    with open('test/mock_response.json', 'r') as f:
        data = f.read()

    gobject = None

    def test_wrong_initialization(self):
        with pytest.raises(exception.UnsupportedDataTypeError):
            gobject = geo.Gobject(123)

    def test_zero_results_exception(self):
        with pytest.raises(exception.ZeroResultsError):
            geo.Gobject({'status': 'ZERO_RESULTS'})

    def test_over_query_limit_exception(self):
        with pytest.raises(exception.OverQueryLimitError):
            geo.Gobject({'status': 'OVER_QUERY_LIMIT'})

    def test_request_denied_exception(self):
        with pytest.raises(exception.RequestDeniedError):
            geo.Gobject({'status': 'REQUEST_DENIED'})

    def test_invalid_request_exception(self):
        with pytest.raises(exception.InvalidRequestError):
            geo.Gobject({'status': 'INVALID_REQUEST'})

    def test_unknown_error_exception(self):
        with pytest.raises(exception.UnknownError):
            geo.Gobject({'status': 'UNKNOWN_ERROR'})

    def test_inverse(self):
        '''Bijective function test.

        It checks wether data can be mapped back or not. If test is green
        then the whole object works as needed, bijection exists, data is safe.
        '''
        gobject = geo.Gobject(self.data)
        json_data = json.loads(self.data)
        assert gobject.serialize() == json_data
