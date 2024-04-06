from package_a.hello import say_hello as say_hello_a


def greet():
    return say_hello_a() + " from package-b!"


def say_hello():
    return "Hello, World B!"
