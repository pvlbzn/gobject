[![Test Coverage](https://codeclimate.com/github/pvlbzn/gobject/badges/coverage.svg)](https://codeclimate.com/github/pvlbzn/gobject/coverage)


# Gobject
Google Geocode API wrapper supercharged with Python Data Model,
which makes Gobject behave like a first class citizen. 


## Install

```
pip install gobject
```

## Example

_Assume we are working in Python REPL environement_

Import modules: requests to make a request, json as a utility, gobject. Note that `gobject` dependency free library.
It does not care about a source of JSON containing response from Google Geocode API.

```
import gobject, requests, json
```

Get JSON response from Google API

```
resp = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=Jakarta&key=YOUR_API_KEY')
resp
> <Response [200]>
```

We got the response from API, now lets initialize `gobject`. It can be done in two ways, first one is preffered.

```
gobj = gobject.load(resp.text)

# Or another way using the class Gobject
gobj_alt = gobject.Gobject(resp.text)
```

Beeing a Pythonic, `gobject` leverages Python Data Model to be first-class citizen in your code.

```
gobj == gobj_alt
> True
```

Important feature: `gobject.load` has an inverse function `gobject.serialize`. There exists a _bijection_ relation.
Wrap the data into an object, serialize it and compare to original data.

```
(gobject.load(resp.text)).serialize() == json.loads(resp.text)
> True
```

`gobject` API follows Google Geocode API, just read Geocode docs and you will find it in Gobject too

```
gobj.bounds
> <northeast: <lat: -5.1843219 ; lng: 106.972825>, southwest: <lat: -6.3708331 ; lng: 106.3831259>>

gobj.bounds.northeast
> <lat: -5.1843219 ; lng: 106.972825>

gobj.bounds.northeast == gobj.bounds.southwest
> False

gobj.bounds.northeast = gobj.bounds.southwest
gobj.bounds.northeast == gobj.bounds.southwest
> True

len(gobj.address_components)
> 2
```

#### Errors

Gobject handles all (5 kinds) errors which may occur in 'status' field of a JSON
response from Google Geocode API.

Lets make a request with non-existent place, such as _Cappleble_.

```
resp = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=Cappleble&key=API_KEY')
resp
> <Response [200]>
```

And load its data into the `gobject`

```
wobj = gobject.load(resp.text)
> Traceback (most recent call last):
> ...
> gobject.exception.ZeroResultsError: The geocode was successful but returned no results.
This may occur if the geocoder was passed a non-existent address.
```

Exception message says exactly what we did, the cause of it is a non-existent place.

`gobject` supports all exceptions from Google API with their explanation messages.


## Code Quality

Code quality is measured by codeclimate, you can find badge on a first line.

To test the code run:

```
py.test
```
