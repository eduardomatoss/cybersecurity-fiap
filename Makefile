local/lint:
	flake8 app/

local/black:
	python -m black app/

local/check-packages:
	pipenv check --system -e PIPENV_PYUP_API_KEY=""

local/bandit:
	bandit -r app *.py

local/install:
	pipenv install --dev --skip-lock

local/shell:
	pipenv shell

local/run:
	python run.py

local/test:
	python -m pytest -c tests/pytest.ini \
	--pyargs ./tests -v --junitxml=results.xml \
	--cov-fail-under 100 --cov-report xml \
	--cov-report term \
	--cov-report html --cov ./app
