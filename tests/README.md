The tests work in the following way:

- Firstly, test_mocks.py is tested using pytest-codecarbon's `--carbon` option to generate a test example csv.
- Then, test_codecarbon.py is tested *without* the `--carbon` option to ensure the mock tests returned what we were looking for.
