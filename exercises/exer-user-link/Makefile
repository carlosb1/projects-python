.PHONY: test

clean:
	rm -rf build dist searchfile.egg-info
test:
	pip install . && python setup.py install && pip install -e . && pytest -s -v

all:
	pip install . && python setup.py install && pip install -e . && user-link

docker:
	docker build . -t user-link && docker run -p 5000:5000 user-link
