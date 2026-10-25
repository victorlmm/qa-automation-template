# QA Automation Template · Python + pytest + Playwright

![Tests](https://github.com/victorlmm/qa-automation-template/actions/workflows/tests.yml/badge.svg)

A reusable starting point for **UI and API test automation**. It ships with the pieces every test project ends up needing (environment configuration, logging, base classes, fixtures, reporting, linting, Docker and CI), so a new project starts with writing tests instead of plumbing.

Click **Use this template** on GitHub to start a new project from it.

## What's included

| Area | What you get |
|---|---|
| **Environments** | `dev`, `qa`, `staging`, `prod` config files. Pick one with `--env=staging` or `TEST_ENV=staging`. |
| **Secrets** | Loaded from `.env` locally and GitHub Secrets in CI. Never stored in config files. |
| **UI base** | `BasePage` with navigation, logged interactions (passwords masked), dialog handling and URL assertions. |
| **API base** | `BaseApiClient` with base URL, bearer token, timeouts, retries on transient errors (429/502/503/504) and request logging. |
| **Contracts** | Response validation with `pydantic` models. |
| **Test data** | Faker-based generators with unique values, safe for parallel runs. |
| **Failure evidence** | Screenshot, video and Playwright trace saved **only for failed tests**. |
| **Reporting** | Self-contained HTML report (`reports/report.html`) and a log file (`reports/logs/test-run.log`). |
| **Stability** | Parallel runs (`pytest-xdist`), retries (`pytest-rerunfailures`), configurable blocking of ads/analytics hosts. |
| **Code quality** | Ruff for linting and formatting, enforced with pre-commit and in CI. |
| **Docker** | Run the suite the same way on any machine. |
| **CI** | GitHub Actions: lint → smoke tests on every push/PR, full regression on weekdays, manual runs with environment and suite selection. |

## Project structure

```
├── config/
│   ├── environments/      # dev.toml, qa.toml, staging.toml, prod.toml
│   └── settings.py        # loads the selected environment + .env overrides
├── core/                  # reusable framework code, rarely changes
│   ├── api/base_client.py
│   ├── ui/base_page.py
│   └── logger.py
├── pages/                 # your Page Objects (examples included)
├── api_clients/           # your service clients and schemas (examples included)
├── utils/data_factory.py  # test data generation
├── tests/
│   ├── api/
│   └── ui/
├── conftest.py            # global fixtures: settings, browser config, API settings
├── Dockerfile
└── .github/workflows/tests.yml
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
playwright install chromium
pre-commit install                 # optional: lint on every commit
cp .env.example .env

pytest -m smoke                    # fast critical-path checks
pytest --env=staging -m regression # full suite against staging
pytest -m api -n auto              # API tests in parallel
pytest -m ui --headed              # watch the browser
```

Open `reports/report.html` after a run. For a failed UI test, open its trace with:

```bash
playwright show-trace reports/artifacts/<test-folder>/trace.zip
```

### With Docker

```bash
docker build -t qa-tests .
docker run --rm -e TEST_ENV=qa -v "$PWD/reports:/app/reports" qa-tests -m smoke
```

## Adapting it to your project

1. **Point the environments to your app.** Edit the URLs in `config/environments/*.toml`.
2. **Add secrets** (tokens, test users) to `.env` locally and to **Settings → Secrets and variables → Actions** in GitHub, with the same names as in `.env.example`.
3. **Replace the examples.** Write your own page objects in `pages/`, service clients in `api_clients/`, and tests in `tests/`. Delete the example files.
4. **Keep `core/` generic.** Anything project-specific belongs outside it.

### Writing a page object

```python
from core.ui import BasePage

class CheckoutPage(BasePage):
    path = "/checkout"

    def __init__(self, page):
        super().__init__(page)
        self.pay_button = page.get_by_role("button", name="Pay now")

    def pay(self):
        self.click(self.pay_button)
```

### Writing a service client

```python
from core.api import BaseApiClient

class OrdersClient(BaseApiClient):
    def get_order(self, order_id: str):
        return self.get(f"orders/{order_id}")
```

```python
@pytest.fixture(scope="session")
def orders_client(api_settings):
    return OrdersClient(**api_settings)   # environment URL, token, timeout and retries applied
```

## Conventions

- Locators live in page objects, never in tests. Prefer roles, `data-*` attributes or ids.
- Use Playwright's `expect()` for UI assertions; never `time.sleep`.
- Service clients only call endpoints; assertions belong in tests.
- Every test gets a layer marker (`ui`, `api`) and a suite marker (`smoke`, `regression`).
- Tests are independent and safe to run in parallel.
- Production runs are read-only: smoke tests that create no data.

## Author

**Victor Morera** · Senior QA Engineer · [LinkedIn](https://www.linkedin.com/in/victorluismm)
