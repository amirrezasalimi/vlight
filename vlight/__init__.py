from .validate import validate


# in the name of god


def v(schema=None, **kwargs):
    if schema is None:
        schema = {}
    return validate(schema, **kwargs)


def valid(schema=None, **kwargs):
    if schema is None:
        schema = {}
    return validate(schema, **kwargs)

