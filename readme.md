# douban-web-client

A simple Python client for Douban, based on the web interface.

## Installation

You can install this package directly from GitHub using either `uv` or `pip`.

### 1. Command-line Installation

#### Using `uv`
```sh
uv pip install 'git+ssh://git@github.com/DodgePock/douban_web_client.git'
```

#### Using `pip`
```sh
pip install 'git+ssh://git@github.com/DodgePock/douban_web_client.git'
```

### 2. Configuration-based Installation

Add the following line to your `pyproject.toml` under `[project.dependencies]` or your `requirements.txt`:

#### In `pyproject.toml`

add this line to dependencies

```toml
"douban-web-client @ git+ssh://git@github.com/DodgePock/douban_web_client.git"
```

#### In `requirements.txt`

add this line to text

```
git+ssh://git@github.com/DodgePock/douban_web_client.git
```

Then install with:

- `uv pip install -r requirements.txt`
- or `pip install -r requirements.txt`

## Requirements

- Python >= 3.8

## License

MIT