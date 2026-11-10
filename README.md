# exbyte-brand

Exbyte console branding as an installable package. One animated startup splash, zero dependencies.

## Install

```bash
pip install "git+https://github.com/exbyte-dev/exbyte-brand.git@v0.1.0"
```

With uv:

```bash
uv add "git+https://github.com/exbyte-dev/exbyte-brand.git" --tag v0.1.0
```

In `requirements.txt`:

```
exbyte-brand @ git+https://github.com/exbyte-dev/exbyte-brand.git@v0.1.0
```

Installing from Git needs `git` on the machine. On slim Docker images, add it before the install step:

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
```

## Usage

```python
from exbyte_brand import play_splash

play_splash()
```

Per project overrides:

```python
play_splash(
    tagline="Order Bot v2",     # "" hides the tagline
    label="connecting",         # text next to the spinner
    clear=False,                # keep existing terminal output
    spinner=0,                  # skip the spinner
)
```

When stdout is not a terminal (pipes, systemd, Docker logs) or `NO_COLOR` is set, it prints a plain text banner with no escape codes and no delays.

## Preview

```bash
python -m exbyte_brand
python -m exbyte_brand --tagline "Order Bot v2" --label connecting
```

## Releasing a change

1. Edit the code and bump `__version__` in `src/exbyte_brand/__init__.py`.
2. Commit, then tag and push:

```bash
git tag v0.1.1
git push && git push --tags
```

3. In each project that should pick it up, change the pinned tag.

Projects pinned to an older tag keep the old branding until you bump them.
