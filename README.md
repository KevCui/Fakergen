# Fakergen

> Generate JSON/YAML/XML... mock data with a structured template using Faker under the hood.

## Table of Contents

- [Features](#features)
- [Dependency](#dependency)
- [Usage](#usage)
  - [How to create a Faker template?](#how-to-create-a-faker-template)
  - [How to create and use custom function?](#how-to-create-and-use-custom-function)
  - [How to repeat certain elements?](#how-to-repeat-certain-elements)
- [Credits](#credits)

## Features

- Human-readable syntax as template
- Fully support Faker providers
- Customizable extended functions
- Support any file formats: JSON, YAML, XML...
- CLI script, easy to be integrated into any CI process

## Dependency

```bash
~$ pip install Faker
```

## Usage

```
usage: fakergen.py [-h] [-s] template

positional arguments:
  template      Faker template file

optional arguments:
  -h, --help    show this help message and exit
  -s, --silent  Don't show error message
```

- Generate JSON data using default `./template.json`:

```bash
~$ cat ./template.json
[
  {
    "product_number": "{{bothify(text='????-########', letters='ABCDE')}}",
    "hostname": "{{hostname(2)}}",
    "attributes": [
      {
        "text": "static text",
        "ean": "{{ean13(leading_zero=False)}}",
        "random_number": {{pyint(min_value=1, max_value=999, step=1)}},
        "colors": "{{color_name()}} {{color_name()}}",
        "custom_greeting": "{{greeting()}}"
      }
    ]
  }
]

~$ ./fakergen.py template.json
[
  {
    "product_number": "CEAD-00367795",
    "hostname": "lt-75.collins.rivera-riley.com",
    "attributes": [
      {
        "text": "static text",
        "ean": "7263776026664",
        "random_number": 65,
        "colors": "OldLace Tomato",
        "custom_greeting": "Hi there"
      }
    ]
  }
]
```

### How to create a Faker template?

Faker template is basically a file with variables inside. As an example, `./template.json` shows briefly how a template looks like: Using `{{...}}` to surround Faker provider name or custom function name will indicate the function to be executed as a Faker provider or a python function.

A list of Faker providers can be found [here](https://faker.readthedocs.io/en/stable/providers.html).

### How to create and use custom function?

The preprepared `CustomProviders` class is located in `./customprovider.py`. Firstly, add a function inside this class. Then this custom function can be called from Faker template.

Checkout `greeting()` function as an example.

### How to repeat certain elements?

- One solution is to generate a new JSON template with repeated elements. Using [jq](https://stedolan.github.io/jq/download/) can simply do the job. For example, repeat `attributes`:

```bash
jq '.[].attributes += $el' --argjson el "$(jq '.[].attributes' template.json)" template.json > newtemplate.json
```

If more repeats are needed, `for` loop is helpful. For example, repeat `attributes` 5 times:

```bash
j="$(cat template.json)"; for ((i=0;i<5;i++)); do j="$(jq '.[].attributes += $el' --argjson el "$(jq '.[].attributes' template.json)" <<< "$j")"; done; echo "$j" > newtemplate.json
```

To generate YAML/XML template, similar to `jq`, [yq](https://github.com/kislyuk/yq) is recommended.

## Credits

Inspired by [JSON Generator](https://www.json-generator.com/)

---

<a href="https://www.buymeacoffee.com/kevcui" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-orange.png" alt="Buy Me A Coffee" height="60px" width="217px"></a>