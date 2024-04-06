from package_a.hello import say_hello  # Adjust the import for package-b

def test_say_hello():
    assert say_hello() == "Hello, World A!"
