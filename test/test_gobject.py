import pytest

from gobject import gobject as geo


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
        expected = ('<long name: Santa Cruz de Tenerife,',
                    ' short name: Santa Cruz de Tenerife,'
                    ' types: [\'locality\', \'political\']>')

    def test_equality(self):
        assert self.addr == self.addr

    def test_inequality(self):
        other_addr = geo.AddressComponent('long_name', 'short_name', [1, 2])
        assert self.addr != other_addr
