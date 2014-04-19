from .util import collect, remove, dshape
from .coretypes import *

# https://github.com/ContinuumIO/datashape/blob/master/docs/source/types.rst

dimension_types = (Fixed, Var, Ellipsis)

isunit = lambda x: isinstance(x, Unit)

def isdimension(ds):
    """ Is a component a dimension?

    >>> isdimension(Fixed(10))
    True
    >>> isdimension(Var())
    True
    >>> isdimension(int32)
    False
    """
    return isinstance(ds, dimension_types)


def ishomogenous(ds):
    """ Does datashape contain only one dtype?

    >>> ishomogenous(int32)
    True
    >>> ishomogenous(var * (3 * string))
    True
    >>> ishomogenous(var * Record([('name', string), ('amount', int32)]))
    False
    """
    return len(set(remove(isdimension, collect(isunit, ds)))) == 1


def dimensions(ds):
    """ Number of dimensions of datashape

    Interprets records as dimensional

    >>> dimensions(int32)
    0
    >>> dimensions(10 * int32)
    1
    >>> dimensions(var * (10 * int32))
    2
    >>> dimensions(var * Record([('name', string), ('amount', int32)]))
    2
    """
    if not isinstance(ds, DataShape):
        ds = dshape(ds)
    if isdimension(ds[0]):
        return 1 + dimensions(ds.subarray(1))
    if isinstance(ds[0], Record):
        return 1 + max(map(dimensions, ds[0].fields.values()))
    if len(ds) == 1 and isunit(ds[0]):
        return 0
    raise NotImplementedError('Can not compute dimensions for %s' % ds)
