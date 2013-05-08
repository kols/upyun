.PHONY: docs dist publish test

docs:
	make -C docs html

dist:
	python setup.py sdist

publish: dist
	python setup.py upload

test:
	py.test -v
