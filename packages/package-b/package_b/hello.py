from package_a.hello import say_hello as say_hello_a


def greet() -> str:
    return say_hello_a() + " from package-b!"


def say_hello() -> str:
    return "Hello, World B!"
