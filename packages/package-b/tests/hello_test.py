from package_b.hello import say_hello, greet  # Adjust the import for package-b

def test_greet():
    assert greet() == "Hello, World A! from package-b!"

def test_say_hello():
    assert say_hello() == "Hello, World B!"
