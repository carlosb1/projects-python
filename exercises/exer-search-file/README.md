# exer-search-file


### For virtual env.
It can be choosen any one, it depends on your preferences I prefer `pipenv`, but it should be a python 3.x, it is tested with 3.8  but it should work
with any 3.x version.

```
	pipenv shell
```


### For installation

```
	python setup.py install
```

### Run

```
	search-file
```

it searchs by default inside `resources/files` the files to be loaded

then it runs a prompt, you can type

```
>>> hello world
```

It should return which files contain the words.

### For testing

```

pytest -s -v

```


### Bullet points about design decisions

* It is designed with a clean architecture with use cases. It split any use case in one class, to permit single responsabilities
* It applies SOLID principles with inverse dependencies, abstractions, single responsabilities
* It tries to abstract in functions the functionalities
* It is not safe-thread, but we can try to do improvements in the DB to avoid this
* It is not async., it saves information in a in-memory db, but we keep blocked, it can be modified, applying async operations and apply
some concurrency pattern
* The domain classes are to simple that we decided that it was not necessary to create extra classes as dataclass
* Variable and functios try to apply a commond vocabulary that are from the context.
