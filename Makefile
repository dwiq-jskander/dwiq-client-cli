include .env
log-level?=DEBUG

TEST_UNIT:= $(if $(test-file),$(test-file),tests/unit)
TEST_INTEGRATION:= $(if $(test-file),$(test-file),tests/integration)

PWD = $(shell pwd)
CMD:=LOGGING_LEVEL=$(log-level) LOGGING_TYPE=stream poetry run
COV_FAIL:=--cov-fail-under=30

PROJECT :=dwiq-client-cli
PYTHON_VERSION :=3.9

# this is required to activate conda within a Makefile (Supports system installed or user installed conda)
CONDA_SETUP := \
    if command -v conda &> /dev/null; then \
        __conda_setup="$$(conda 'shell.zsh' 'hook' 2> /dev/null)"; \
        if [ $$? -eq 0 ]; then \
            eval "$$__conda_setup"; \
        else \
            . "$$(conda info --base)/etc/profile.d/conda.sh"; \
        fi; \
    elif [ -f "$$HOME/miniconda3/etc/profile.d/conda.sh" ]; then \
        . "$$HOME/miniconda3/etc/profile.d/conda.sh"; \
    else \
        echo "Conda not found. Please install Conda and set up the environment."; \
        exit 1; \
    fi

# initial setup of the python environment
init:
	@$(CONDA_SETUP); conda init
	@$(CONDA_SETUP); conda create --name $(PROJECT) python=$(PYTHON_VERSION) --force

# pip install is needed because of a mac mismatch whl issue
install:
	pip install setuptools wheel 'Cython<3'
	pip install --no-build-isolation fastavro==1.7.4
	pip install 'SQLAlchemy<2.0.0'
	poetry install

clear-poetry-cache:
	poetry cache clear pypi --all
	poetry update

# Run lint and formatting with checks only
lint:
	$(CMD) flake8 .
	$(CMD) isort --profile=black .
	$(CMD) black . --check

# Run lint and formatting with an update of the files
lint-update:
	$(CMD) flake8 .
	$(CMD) isort --profile=black .
	$(CMD) black .

# Run unit tsts
test:
	$(CMD) pytest $(TEST_UNIT)
# $(COV_FAIL) --cov

# Run integration tests
test-integration:
	$(CMD) pytest $(TEST_INTEGRATION)

# Run test coverage
test-cov:
	$(CMD) pytest tests/unit --cov --cov-report=html:docs/coverage $(COV_FAIL)
	open docs/coverage/index.html || true

bq-current:
	BQ_DATASET=$(BQ_DATASET) GOOGLE_CLOUD_PROJECT=$(GOOGLE_CLOUD_PROJECT) alembic current

bq-downgrade:
	BQ_DATASET=$(BQ_DATASET) GOOGLE_CLOUD_PROJECT=$(GOOGLE_CLOUD_PROJECT) alembic downgrade -1

bq-upgrade:
	BQ_DATASET=$(BQ_DATASET) GOOGLE_CLOUD_PROJECT=$(GOOGLE_CLOUD_PROJECT) alembic upgrade head