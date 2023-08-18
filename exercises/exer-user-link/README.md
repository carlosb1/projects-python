
For a correct installation, it should be necessary install one of your virtualenv environment. It exists a good set of options, if it is not possible run with `sudo` permissions

### For virtual env.
It can be choosen any one, it depends on your preferences I prefer `pipenv`, but it should be a python 3.x, it is tested with 3.8  but it should work
with any 3.x version.

```
	pipenv shell
```

## Installation

```
pip install -e .
```

## Test

```
make test
```

## Run via docker
```
make docker
```

## Run non via docker
```
make all
```

### Architecture bullet points

* It was applied an clean architecture
* `domain.py` includes entity classes
* `services` includes business use cases which is part of the domain.
* `adapters` following the clean architecrue, it includes adapters like: repositories, file managers.
* `utils` some extra necessary function
* Coverage should be 100%, it was not evaluated
* It applies the pyramid test, where the end-to-end tests should be in `test_app.py`
* The auth and authorization is customized and developer from scratch
* Applied SOLID principles
* It was tried to apply abstraction by functions.
* Our token implementation has a bug, it needs a seed and correct hash function, it replies all the same token.
