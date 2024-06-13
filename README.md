# SideEffect Library

The `SideEffect` library provides a convenient way to manage state changes with optional synchronous or asynchronous side effects. This can be particularly useful in scenarios where you want to perform an action whenever a state changes, such as updating a user interface, logging, notifications, or other side effects.

## Installation

You can install `SideEffect` using pip:

```bash
pip install sideeffect
```

## Usage

### `SideEffect` Class

The `SideEffect` class allows you to manage a state with an optional side effect that can be executed either synchronously or asynchronously when the state is changed. Additionally, you can specify if the side effect is dependent on the state or not.

#### Example

```python
from sideeffect import SideEffect

def drink_coffee():
    print("Coffee consumed ☕️")

coffee_level = SideEffect(default="Full", side_effect=drink_coffee)

# Oh no, the coffee level is dropping!
coffee_level.setState("Half")
```

### `side_effect` Function

The `side_effect` function is a convenience function that creates a `SideEffect` instance and returns accessor functions for getting and setting the state.

#### Example

```python
from sideeffect import side_effect

def drink_coffee():
    print("Coffee consumed ☕️")

coffee_level, set_coffee_level = side_effect(default="Full", side_effect=drink_coffee)

# Oh no, the coffee level is dropping!
set_coffee_level("Half")
```

## API

1. ### `SideEffect` Class

    `__init__(self, default=0, side_effect=lambda: None, *, asynchronous=True, dependent=False) -> None`

    Initializes the `SideEffect` instance.

    - `default` (Any): The initial state (default is 0).
    - `side_effect` (Callable[[], None]): A callable to be executed as a side effect (default is a no-op lambda).
    - `asynchronous` (bool): If True, the side effect is executed asynchronously (default is True).
    - `dependent` (bool): If True, the side effect is dependent on the state (default is False).

    `state(self) -> Any`

    Returns the current state.

    `setState(self, value, *, asynchronous: Union[bool, None]=None) -> None`

    Sets the state to the given value and executes the side effect.

    - `value` (Any): The new state value.
    - `asynchronous` (Union[bool, None]): If provided, overrides the instance's asynchronous setting for this call.
    - Raises `TypeError` if the `asynchronous` parameter is not a boolean.

1. ### `side_effect` Function

    `side_effect(default=0, side_effect=lambda: None, *, asynchronous=True, dependent=False) -> Tuple[Callable[[], Any], Callable[[Any, Optional[bool]], None]]`

    A convenience function to create a `SideEffect` instance and return accessor functions.

    - `default` (Any): The initial state (default is 0).
    - `side_effect` (Callable[[], None]): A callable to be executed as a side effect (default is a no-op lambda).
    - `asynchronous` (bool): If True, the side effect is executed asynchronously (default is True).
    - `dependent` (bool): If True, the side effect is dependent on the state (default is False).

    Returns a tuple containing:
    - A lambda to get the current state.
    - A lambda to set the state and execute the side effect.

## New Features in v1.0.3

- Added a new `dependent` parameter to the `SideEffect` class and `side_effect` function. This parameter allows you to specify whether the side effect is dependent on the state or not. If the side effect is dependent, the previous side effect will be completed before executing the new one.
- Improved thread handling for asynchronous side effects, ensuring that the previous side effect is completed before starting a new one if the side effect is dependent on the state.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on [GitHub](https://github.com/sharunashwanth/SideEffect).

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
