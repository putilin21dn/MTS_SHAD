PYTHON = python3

.PHONY: run clean venv install

run:
	scrapy crawl -o out.csv films

clean:
	rm -rf __pycache__

test:
	$(PYTHON) -m unittest test.py

venv:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

install:
		pip3 install -r requirements.txt