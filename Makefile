unittests:
	@echo "Unittesting Model2Service..."
	@nosetests --nocapture --nologcapture  --all-modules --verbose --exe m2s/tests --cover-package=m2s --with-coverage --cover-inclusive --cover-erase --cover-html --cover-html-dir=testing/coverage