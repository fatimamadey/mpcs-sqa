# To-Do List Backend

## Install dependencies
```bash
pip install pytest pytest-cov
```

## Run tests
```bash
python3 -m pytest tests/ -v
```

## Run coverage report and generate HTML (tables will be in index.html)
``` bash
python3 -m pytest --cov=src --cov-branch --cov-report=term --cov-report=html tests/
```
---