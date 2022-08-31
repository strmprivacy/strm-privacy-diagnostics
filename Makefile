release: dist ## package and upload a release
	twine upload dist/*

release-test: dist
	twine upload --repository testpypi dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install
