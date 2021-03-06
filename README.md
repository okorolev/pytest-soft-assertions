[![Build Status](https://api.travis-ci.org/okorolev/pytest-soft-assertions.svg?branch=master)](https://travis-ci.org/okorolev/pytest-soft-assertions)
[![image](https://img.shields.io/pypi/v/pytest-soft-assertions.svg)](https://pypi.org/project/pytest-soft-assertions/)
### About
This project is experimental. First version written in 25.11.2018.

### Usage
```bash
py.test --soft-asserts
```

### Output
```bash
py.test examples/test_all_asserts.py --soft-asserts
```

```
E           AssertionError:
E           +-------------------------+-----------------+------------------+---------------+
E           |       expression        |    condition    |  current value   |   expected    |
E           +=========================+=================+==================+===============+
E           | assert value == 1       | ==              | -1               | 1             |
E           +-------------------------+-----------------+------------------+---------------+
E           | assert 1 == 2           | ==              | 1                | 2             |
E           +-------------------------+-----------------+------------------+---------------+
E           | assert 'Kek' is None    | is              | Kek              | None          |
E           +-------------------------+-----------------+------------------+---------------+
E           | assert object is None   | is              | <class 'object'> | None          |
E           +-------------------------+-----------------+------------------+---------------+
E           | assert None is not None | is not          | None             | is not None   |
E           +-------------------------+-----------------+------------------+---------------+
E           | assert 1 is None        | is              | 1                | None          |
E           +-------------------------+-----------------+------------------+---------------+
E           | assert 1 in [2, 2]      | in              | 1                | in [2, 2]     |
E           +-------------------------+-----------------+------------------+---------------+
E           | assert 1 not in [1, 2]  | not in          | 1                | not in [1, 2] |
E           +-------------------------+-----------------+------------------+---------------+
E           | assert 4 in orders      | in              | 4                | in [1, 2, 3]  |
E           +-------------------------+-----------------+------------------+---------------+
E           | assert None or False    | or              | None             | <Not None>    |
E           +-------------------------+-----------------+------------------+---------------+
E           | assert not True         | not             | True             | <Not None>    |
E           +-------------------------+-----------------+------------------+---------------+
E           | assert {}               | <Not condition> | {}               | <Not None>    |
E           +-------------------------+-----------------+------------------+---------------+
E           | assert None             | <Not condition> | None             | <Not None>    |
E           +-------------------------+-----------------+------------------+---------------+
E           | assert 1 > 1            | >               | 1                | > 1           |
E           +-------------------------+-----------------+------------------+---------------+
E           | assert 1 < 1            | <               | 1                | < 1           |
E           +-------------------------+-----------------+------------------+---------------+
E           | assert 1 >= 2           | >=              | 1                | >= 2          |
E           +-------------------------+-----------------+------------------+---------------+
E           | assert 2 <= 1           | <=              | 2                | <= 1          |
E           +-------------------------+-----------------+------------------+---------------+
E           | assert 1 != 1           | !=              | 1                | != 1          |
E           +-------------------------+-----------------+------------------+---------------+
```