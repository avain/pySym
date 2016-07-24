import logging
from pyObjectManager.List import List
from pyObjectManager.Int import Int
from pyObjectManager.Real import Real
from pyObjectManager.BitVec import BitVec
from pyObjectManager.Char import Char
from pyObjectManager.String import String
import pyState
from copy import copy

logger = logging.getLogger("pyState:SimFunction:List:append")


def handle(state,call,var,ctx=None):
    """
    Append var to list
    """
    ctx = ctx if ctx is not None else state.ctx
    
    # Resolve what we're going to be appending
    varList = state.resolveObject(var,ctx=ctx)

    # If we're waiting on a symbolic call, return
    retObjs = [x for x in varList if type(x) is pyState.ReturnObject]
    if len(retObjs) > 0:
        return retObjs

    ret = []

    for var in varList:
        s = var.state.copy()
        
        s.path.pop(0)

        # Resolve Root
        root = s.resolveObject(call.func.value,ctx=ctx)

        assert len(root) == 1
        root = root.pop()

        assert type(root) is List

        # Append it
        root.append(copy(var))
        
        # Add this to our returns
        retObj = pyState.ReturnObject(1)
        retObj.state = s

        ret.append(retObj)

    return ret



