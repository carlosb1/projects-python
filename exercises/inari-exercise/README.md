# inari-exercise

*Name*: Carlos Báez 
*Spend time:* 3 afternoons (relaxed, with breaks to work in other tasks)

This code works with +python3.6 and I advice to use some virtual environment (conda, miniconda, virtualenv...).

## Code structure 

    ├── install.sh                          -> Scripts to intall dependencies with requirements
    ├── requirements.txt                    -> Requirements file for dependencies   
    ├── resources
    │   └── exercise.pdf                    -> Exercise description
    ├── run.sh                              -> Script to execute game
    ├── src                                 -> Source code 
    │   ├── adapters.py                     -> Module for adapters
    │   ├── controller.py                   -> Controller module manage
    │   ├── entrypoints.py                  -> Module for entrypoints
    │   ├── main.py                         -> Code to play game
    │   ├── models.py                       -> Module to save the Business model
    │   ├── tests                           -> Set of tests
    │   │   ├── adapters_tests.py           -> Unitary tests for adapters
    │   │   ├── entrypoints_tests.py        -> Unitary tests for entrypoints
    │   │   ├── integrations_tests.py       -> Integration (and in this case, also they are acceptance tests)
    │   │   └── usecases_tests.py           -> Unitary tests for usecases
    │   └── usecases.py                     -> Module for usecases 
    ├── test.sh                             -> Script to execute test and check coverage
    └── travis.yml                          -> Script to apply continuous delivery


## Description

The idea of this implementation follows the [clean architecture][clean] in order to follow [SOLID][solid] principles. It permits achieve some good features in the code (split responsabilities, immutabilites, fast testing, etc...)

In the first steps, I didn't use any specification of the business [domain][domain] (saved in `models.py`). I was adding new features to permit understand better the business and in the last steps of the implementation I added a Game(`models.py`) as an entity.

Furthermore, I used type checking feature for python 3.x  to specify the contract among modules. In the clean architecture, I have some modules where these contracts are necessary:

- *adapters* are used as connection of different services (databases, queues, etc) in our case I only need call a random generator of numbers
- *entrypoints* are used to implement different entrypoints to the code (webservices, cli, RPC services)
- *use cases* are the core of the business, they describe how the business works and every use case defines one different. It is very important to check which workflow has the business.
- *controller*  In this case, It has the only responsability to move the received data ([DTO objects][DTO]) from different entrypoints to use cases and get the responses.
- *models*  are entities to define the business domain.

 This implementation provides different features:

- Single responsabilities
- Inverse dependency when I create objects (I can check the factory to preview it)
- Work with contracts
- Difference between value objects and classes
- Possibility to implement different asynchronous patterns with immutable objects.

![clean_architecture](https://blog.cleancoder.com/uncle-bob/images/2012-08-13-the-clean-architecture/CleanArchitecture.jpg)

## Tests

For tests, I follow the pyramid test architecture:

![pyramid](https://www.360logica.com/blog/wp-content/uploads/2014/07/A-sneak-peek-into-test-framework-test-pyramid-testing-pyramid.png)


Furthermore, I decided to use integration and acceptance tests in the same way. This is a small problem, I don't need to split them.

    Name                          Stmts   Miss  Cover
    -------------------------------------------------
    __init__.py                       0      0   100%
    adapters.py                      16      1    94%
    controller.py                    34     12    65%
    entrypoints.py                   53      3    94%
    main.py                          12     12     0%
    models.py                        42      4    90%
    tests/__init__.py                 0      0   100%
    tests/adapters_tests.py          15      0   100%
    tests/entrypoints_tests.py       40      0   100%
    tests/integrations_tests.py      99      0   100%
    tests/usecases_tests.py          63      0   100%
    usecases.py                      39      0   100%
    -------------------------------------------------
    TOTAL                           413     32    92%

In general, the not tested code has an explanation:

* adapters and entrypoints don't get 100% because I can not test the implemented interfaces / contracts that they work as contracts
* `main.py`  and `controller.py` are not tested the factory pattern and to source code to execute the end app, they are outside of the end-to-end testbed
For these reasons, I can consider I have a 100% coverage discarding these two cases. Anyway, If I want to be strict and search more extreme ways all the complete pipeline.

## Improvements

- With this structure, It can be possible to work with different languages if I move messages in a different class.
- It is a very basic example, I must use a good random seed in order to get good random values.

[clean]: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html "clean"
[solid]: https://en.wikipedia.org/wiki/SOLID "solid"
[domain]: https://en.wikipedia.org/wiki/Business_domain "domain"
[DTO]: https://en.wikipedia.org/wiki/Data_transfer_object "DTO objects"
