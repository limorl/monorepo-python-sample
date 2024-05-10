# Configuration Provider

Configuration provider is initialized with a config file which containes configuration sections named after the type of configuration.
For example, a configuration file as follows:
```json
{
    "AppConfiguration": {
        "numOfExclamations": 1
    },
    "LDConfiguration": "abcdefg-aaa-sssdf-seefd-sssa",
    "DummyConfiguration1": {
        "int100": 100,
        "int200": 200,
        "section100": {
            "str100": "100",
            "str200": "200"
        }
     },
    "DummyConfiguration2": {
        "int1": 1,
        "int2": 2,
        "section1": {
            "int1": 1,
            "str1": "1"
        },
        "section10": {
            "int10": 10,
            "str10": "10"
        }
    }
}
```

`app_configuration_provider.get_configuration(AppConfiguration)` it will return an oject of type `AppConfiguration`.