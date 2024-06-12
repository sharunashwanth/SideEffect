import threading
from typing import Any, Callable, Optional, Tuple, Union

def typecheck(obj: Any, datatype: Union[type, str], *, error_msg: str="Object {obj} is not assignable to type '{datatype}'") -> None:
    """
    Checks if the given object matches the specified datatype.
    
    Parameters:
    - obj: The object to be checked.
    - datatype: The expected type of the object. If "function", checks if the object is callable.
    - error_msg: Custom error message for the TypeError (default is a formatted string).
    
    Raises:
    - TypeError: If the object does not match the expected datatype.
    """

    if datatype == "function":
        if not callable(obj):
            raise TypeError(
                error_msg.format(obj=obj, datatype="function")
            )
        return
    
    if not isinstance(obj, datatype):
        raise TypeError(
            error_msg.format(obj=obj, datatype=datatype)
        )

class SideEffect():
    """
    A class to manage a state with an optional side effect that can be executed either synchronously or asynchronously when the state is changed assuming that the asynchrous operation is independent of the state.
    
    Attributes:
    - _state: The current state.
    - _side_effect: A callable to be executed as a side effect.
    - _asynchronous: A boolean indicating whether the side effect should be executed asynchronously.
    
    Methods:
    - __init__(self, default=0, side_effect=lambda: None, *, asynchronous=True): Initializes the SideEffect instance.
    - state(self): Property to get the current state.
    - setState(self, value, *, asynchronous: bool=None): Sets the state and executes the side effect.
    """
    
    def __init__(self, default: Any=0, side_effect: Callable[[], None]=lambda: None, *, asynchronous: bool=True) -> None:
        """
        Initializes the SideEffect instance.
        
        Parameters:
        - default: The initial state (default is 0).
        - side_effect: A callable to be executed as a side effect (default is a no-op lambda).
        - asynchronous: If True, the side effect is executed asynchronously (default is True).
        """
        
        self._state = default

        # Checking the types for the inputs
        typecheck(side_effect, "function")
        typecheck(asynchronous, bool)
        
        self._side_effect = side_effect
        self._asynchronous = asynchronous

    @property
    def state(self) -> Any:
        """ Returns the current state. """
        return self._state

    def setState(self, value: Any, *, asynchronous: Union[bool, None]=None) -> None:
        """
        Sets the state to the given value and executes the side effect.
        
        Parameters:
        - value: The new state value.
        - asynchronous: If provided, overrides the instance's asynchronous setting for this call.
        
        Raises:
        - TypeError: If the asynchronous parameter is not a boolean.
        """
        
        # Checking the types for the inputs
        if asynchronous != None:
            typecheck(asynchronous, bool)
        
        asynchronous = self._asynchronous

        self._state = value

        if asynchronous:
            threading.Thread(target=self._side_effect).start()
        else:
            self._side_effect()


def side_effect(default: Any=0, side_effect: Callable[[], None]=lambda: None, *, asynchronous: bool=True) -> Tuple[Callable[[], Any], Callable[[Any, Optional[bool]], Any]]:
    """
    A convenience function to create a SideEffect instance and return accessor functions.
    
    Parameters:
    - default: The initial state (default is 0).
    - side_effect: A callable to be executed as a side effect (default is a no-op lambda).
    - asynchronous: If True, the side effect is executed asynchronously (default is True).
    
    Returns:
    - A tuple containing:
      - A lambda to get the current state.
      - A lambda to set the state and execute the side effect.
    """

    _state = SideEffect(default, side_effect, asynchronous=asynchronous)

    return (
        lambda : _state.state,
        lambda value, *, asynchronous=None: _state.setState(value, asynchronous=asynchronous)
    )
