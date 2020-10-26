# Testing

writing test is important.

cati has a custom testing system. all of tests are in `tests/` directory.

## running tests
to run tests, you have the following ways:

```bash
make test
# or
python3 tests/run.py
# or
./tests/run.py
```

`tests/run.py` script runs tests.

## create test

to create new test, you can run this command in terminal:

```bash
python3 tests/make_test.py test_something
```

the `tests/make_test.py` script makes a test. you should pass test name as argument to this script.

now, created test is in `tests/items/test_something.py`:

```python
""" Test test_something """

from TestCore import TestCore

class test_something(TestCore):
    """ Test test_something """
    def run(self):
        """ Run test """
        # this is main function of test. do assertions here
        self.assert_true(True)

```

now you can do assertions in `run` function.

#### NOTE: tests will run in a isolated environemnt

Another TestCore function:
- `assert_equals(first, last)`: assert equals
- `env()`: returns testing environment directory path
- `refresh_env()`: when you installing/removing... packages in current environment, this action may make conflict for another tests, so, calling this function refreshes environment
- `run_command(command_name, [command_arguments])`: this function runs command and returns exit code of that
