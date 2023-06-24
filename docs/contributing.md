# Contribution Guidelines

Thanks for considering to contribute to this project! Some guidelines:

- Go through the issue list and if needed create a relevant issue to discuss the change design. On disagreements, maintainer(s) will have the final word.
- You can expect a response from a maintainer within 7 days. If you haven’t heard anything by then, feel free to ping the thread.
- This package tries to be as simple as possible for the user (hide any complexity from the user). Options are only added when there is clear value to the majority of users.
- When issues or pull requests are not going to be resolved or merged, they should be closed as soon as possible. This is kinder than deciding this after a long period. Our issue tracker should reflect work to be done.

## Unit Tests

Make sure to install an editable version before running tests:

```bash
pip install -r tests/test_requirements.txt
pip install -e .
pytest --cov=mkdocs_print_site_plugin --cov-report term-missing tests/
```

If it makes sense, writing tests for your PRs is always appreciated and will help get them merged.

In addition, this project uses [pyflakes](https://pypi.org/project/pyflakes/) for static code checking:

```bash
pip install pyflakes
pyflakes tests/ mkdocs_print_site_plugin/
```

## Manual testing

To quickly serve a website with your latest changes to the plugin use the sites in our tests suite. For example:

```bash
pip install -r tests/test_requirements.txt
pip install -e .
mkdocs serve -f tests/fixtures/projects/basic/mkdocs.yml
```

Tip: If you use google chrome, you can also view the print version of a page inside the browser [by setting the renderer](https://www.smashingmagazine.com/2018/05/print-stylesheets-in-2018/).

## Code Style

Make sure your code *roughly* follows [PEP-8](https://www.python.org/dev/peps/pep-0008/) and keeps things consistent with the rest of the code. I recommended using [black](https://github.com/psf/black) to automatically format your code.

We use google-style docstrings.

## Documentation

Is in `docs/`. To [deploy the docs](https://www.mkdocs.org/user-guide/deploying-your-docs/), run:

```bash
mkdocs gh-deploy
```

Note: there is no automated github action for this currently.
