deb:
	python setup.py --command-packages=stdeb.command sdist_dsc --package ubuntu-cleaner bdist_deb

clean:
	@rm -rf deb_dist dist ubuntu_cleaner.egg-info
	@rm -f ubuntu-cleaner*.tar.gz

test:
	python -m unittest discover tests
