
# Linked data equivalent in software code

This document provides a brief overview of how linked data could be
applied to annotate software code in a same way that JSON-LD provides
semantics in relation to JSON data. It is using a simplified example for
convenience of illustration. This very simple case could be solved with
an easier approach, but the principles should be helpful for more
complex use cases.

Consider the following JSON string, that contains information about a
wind speed value and a wind direction value.

```json
{
    "wind_speed": 10.0,
    "wind_from_direction": 0.0
}
```

It could for example be the response from an API request.

The API documentation might include a JSON Schema, as shown below, which
includes details about the structure of the data. The semantics
(meaning) of the data is documented in the descriptions, which are not
machine readable. The machine readable part, the required fields and
their types, is entirely concerned with structure and not with
semantics.

```json
{
    "properties": {
        "wind_speed": {
            "type": "number",
            "title": "Wind Speed",
            "description": "The wind speed scalar magnitude in metre per second"
        },
        "wind_from_direction": {
            "type": "number",
            "title": "Wind From Direction",
            "description": "The direction that the wind is coming from in degrees, where the origin is north"
        }
    },
    "required": [
        "wind_speed",
        "wind_from_direction"
    ]
}
```

To make the semantics of the data machine-readable, the API may use
JSON-LD, including a context header that binds each key (`"wind_speed"`
and `"wind_direction"`) to an ontology or taxonomy type through a URI.
The URIs shown in the example below are just fictional. It should be
assumed that they include relevant details about the measurement
quantity and unit of measure, as well as the format of the data (decimal
numbers).

```json
{
    "@context": {
        "wind_speed": "https://wind-measurement-ontology.foo/terms/wind_speed",
        "wind_from_direction": "https://wind-measurement-ontology.foo/terms/wind_from_direction"
    },
    "wind_speed": 10.0,
    "wind_from_direction": 0.0
}
```

Whereas the semantics of data described by a JSON Schema must be mapped
to the system using it beforehand, a JSON-LD document might be possible
to interpret "on-the-fly," provided there is a reasoner that can handle
the ontologies used.

Analogous to the simple JSON string, consider the following function in
the Python programming language.

```python
import math


def get_wind_vector(
    wind_speed,
    wind_from_direction,
):
    return (
        wind_speed * math.sin(math.radians(wind_from_direction)),
        -wind_speed * math.cos(math.radians(wind_from_direction)),
    )

```

To describe the structure of this function, it would be common to add
type annotations and a documentation string as shown below.

```python
import math


def get_wind_vector(
    wind_speed: float,
    wind_from_direction: float,
) -> tuple[float, float]:
    """Calculate the wind vector from wind speed and direction.
    
    The x-component of the wind vector is towards east and the
    y-component is towards north.

    :param wind_speed: the wind speed scalar magnitude in metre per
        second
    :param wind_from_direction: the direction that the wind is coming
        from in degrees, where the origin is north
    """
    return (
        wind_speed * math.sin(math.radians(wind_from_direction)),
        -wind_speed * math.cos(math.radians(wind_from_direction)),
    )
```

The type annotations provides details about the structure of the data,
similar to the type information in JSON Schema. It allows a type checker
to ensure compatible types between interacting components.

The documentation string content is similar to the description content
in the JSON Schema. It is useful for developers working with the code
base, but not machine readable.

To move to the equivalent of JSON-LD, one would need to use type
annotations that link to the ontology types, which could be achieved
by a solution along the lines of the below example. The documentation
string as in the above example could still be kept for convenience, but
is removed assuming that those details would instead all be retrieved
from the ontology types linked with the URIs.

The example assumes that some library would be developed to support
semantic annotations. The structures and names used here are just for
illustration.

It should be possible to use a semantic type checker to assert
compatibility between components, just like a static type checker like
`mypy` can be used to check for structural compatibility. That would of
course involve some complexities in the implementation.

The semantic annotations as envisioned here would not have any impact at
runtime (just like the type annotations, they would be ignored at
runtime) or compile time (for a compiled language). They would serve as
enabler of static semantic compatibility checking, enabler of automated
integration and source of rich documentation.

A natural approach would likely be to convert the annotations to JSON-LD
and then use the existing technology stack that supports that format to
perform validation (e.g. with SHACL) and reasoning.

```python
import math
from typing import Annotated

from some_semantic_annotation_library import TypeContext


WindSpeed = Annotated[
    float,
    TypeContext(uri="https://wind-measurement-ontology.foo/terms/wind_speed"),
]

WindFromDirection = Annotated[
    float,
    TypeContext(uri="https://wind-measurement-ontology.foo/terms/wind_from_direction"),
]

WindVector = Annotated[
    tuple[float, float],
    TypeContext(uri="https://wind-measurement-ontology.foo/terms/wind_vector"),
]


def get_wind_vector(
    wind_speed: WindSpeed,
    wind_from_direction: WindFromDirection,
) -> WindVector:
    return (
        wind_speed * math.sin(math.radians(wind_from_direction)),
        -wind_speed * math.cos(math.radians(wind_from_direction)),
    )

```
