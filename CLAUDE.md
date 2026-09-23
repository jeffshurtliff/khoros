# CLAUDE.md

## Status
`khoros` is a Python SDK for Khoros Communities. The project is **archived and no longer maintained**; v6.0.0 is the
final release. Keep any change minimal and scoped; do not refactor or restructure.

## Layout
- `khoros/`: the package (`core.py` holds the `Khoros` object; `api.py`, `structures/`, `objects/`, `utils/`)
- `khoros/utils/tests/`: pytest suite
- `docs/`: Sphinx docs (built on Read the Docs from `requirements.txt`)

## Commands
- `poetry install` (or `pip install -r requirements.txt && pip install -e .`); requires Python 3.10+
- `pytest`: live-API tests skip themselves because no helper file/credentials exist
- `sphinx-build docs docs/_build`

## Notes
- The version must match in `pyproject.toml` and `khoros/utils/version.py` (`setup.py` reads the latter).
- Dependencies are declared in `pyproject.toml`, `requirements.txt` and `setup.py`; keep all three in sync.
