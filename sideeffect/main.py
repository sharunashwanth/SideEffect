import threading
from typing import Any, Callable, Optional, Tuple, Union

def typecheck(obj: Any, datatype: Union[type, str], *, error_msg: str = "Object {obj} is not assignable to type '{datatype}'") -> None:
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
    A class to manage a state with an optional side effect that can be executed either synchronously or asynchronously when the state is changed.
    
    Attributes:
    - _state: The current state.
    - _side_effect: A callable to be executed as a side effect.
    - _asynchronous: A boolean indicating whether the side effect should be executed asynchronously.
    - _dependent: A boolean indicating whether the side effect is dependent on the state.
    - _side_effect_on_action: A boolean flag indicating if the side effect is currently in action.
    - _side_effect_thread: The thread executing the side effect, if asynchronous.
    
    Methods:
    - __init__(self, default=0, side_effect=lambda: None, *, asynchronous=True, dependent=False): Initializes the SideEffect instance.
    - state(self): Property to get the current state.
    - setState(self, value, *, asynchronous: bool=None): Sets the state and executes the side effect.
    """
    def __init__(self, default: Any = 0, side_effect: Callable[[], None] = lambda: None, *, asynchronous: bool = True, dependent: bool = False) -> None:
        """
        Initializes the SideEffect instance.
        
        Parameters:
        - default: The initial state (default is 0).
        - side_effect: A callable to be executed as a side effect (default is a no-op lambda).
        - asynchronous: If True, the side effect is executed asynchronously (default is True).
        - dependent: If True, the side effect is dependent on the state (default is False).
        """
        self._state = default

        # Checking the types for the inputs
        typecheck(side_effect, "function")
        typecheck(asynchronous, bool)
        typecheck(dependent, bool)
        
        self._side_effect = side_effect
        self._asynchronous = asynchronous
        self._dependent = dependent

        self._side_effect_on_action = False
        self._side_effect_thread: Optional[threading.Thread] = None

    @property
    def state(self) -> Any:
        """
        Returns the current state.
        """
        return self._state

    def setState(self, value: Any, *, asynchronous: Optional[bool] = None) -> None:
        """
        Sets the state to the given value and executes the side effect.
        
        Parameters:
        - value: The new state value.
        - asynchronous: If provided, overrides the instance's asynchronous setting for this call.
        
        Raises:
        - TypeError: If the asynchronous parameter is not a boolean.
        """
        # Checking the types for the inputs
        if asynchronous is not None:
            typecheck(asynchronous, bool)
        
        if asynchronous is None:
            asynchronous = self._asynchronous

        if self._side_effect_on_action and self._dependent:
            self._side_effect_thread.join()
            self._side_effect_on_action = False
            self._side_effect_thread = None

        if asynchronous:
            side_effect_thread = threading.Thread(target=self._side_effect)
            self._side_effect_thread = side_effect_thread
            self._side_effect_on_action = True

            self._state = value
            self._side_effect_thread.start()
        else:
            self._state = value
            self._side_effect()

def side_effect(default: Any = 0, side_effect: Callable[[], None] = lambda: None, *, asynchronous: bool = True, dependent: bool = False) -> Tuple[Callable[[], Any], Callable[[Any, Optional[bool]], None]]:
    """
    A convenience function to create a SideEffect instance and return accessor functions.
    
    Parameters:
    - default: The initial state (default is 0).
    - side_effect: A callable to be executed as a side effect (default is a no-op lambda).
    - asynchronous: If True, the side effect is executed asynchronously (default is True).
    - dependent: If True, the side effect is dependent on the state (default is False).
    
    Returns:
    - A tuple containing:
      - A lambda to get the current state.
      - A lambda to set the state and execute the side effect.
    """
    _state = SideEffect(default, side_effect, asynchronous=asynchronous, dependent=dependent)

    return (
        lambda: _state.state,
        lambda value, *, asynchronous=None: _state.setState(value, asynchronous=asynchronous),
    )
