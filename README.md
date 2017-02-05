# Gobject
Google Geocode API wrapper supercharged with Python Data Model,
which makes Gobject behave like a first class citizen. 


## Example

_Assume we are working in Python REPL environement_

#### General showcase

```
> # Get JSON response
> response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=Jakarta&key=YOUR_API_KEY')

> # load() return initialized Gobject instance
> obj = gobject.load(response.text)

> # Lets take northeast bounds
> obj.bounds.northeast
> # REPL will return northeast bound representation
<lat: -5.1843219 ; lng: 106.972825>

> obj.bounds.northeast.lat
-5.1843219

> len(obj.address_components)
2

> obj.address_components[0].long_name
'Special Capital Region of Jakarta'

> # Thanks to the data model we can use comparison operator
> obj.bounds.northeast == obj.bounds.northeast
True
> obj.bounds.northeast == obj.bounds.southwest
False

> # We can edit each and every data
> obj.place_id = 'new place id'
> obj.place_id
'new place id'

> # More over, Gobject can be serialized back. Function serialize() is the inverse
> # function of load(). Thus, there exists bijection, which means that the data is safe.
> # Convert JSON response string into a dictionary
> original_response = json.loads(response.text)
> original_response == obj.serialize()
True
```

#### Errors

Gobject handles all (5 kinds) errors which may occur in 'status' field of JSON
response from Google Geocode API.

```
> # If something went wrong, exception with explanation will occur
> data = {'results': [], 'status': 'INVALID_REQUEST'}
...
gobject.exception.InvalidRequestError: Query (address, components, lat, lng) is missing

> # Status class is a modified Enum container which helps to manage exceptions.
> # It is not trivial and covered in details in its docstring.
> for s in exception.Status:
...   print(s)
Status.OK
Status.ZERO_RESULTS
Status.OVER_QUERY_LIMIT
Status.REQUEST_DENIED
Status.INVALID_REQUEST
Status.UNKNOWN_ERROR

> # Friendly reminder: Read docstring in REPL can be done with pprint:
> #     pprint(exception.Status.__doc__)

```

## Tests

Coverage is > 90%. Run `py.test --cov`.