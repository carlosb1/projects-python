.PHONY: test

test:
		pip install . && python setup.py install && pip install -e . && pytest -s -v
