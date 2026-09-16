# ecoci-demo

Demo application used to evaluate the **EcoCI** carbon-aware CI/CD control plane.

This repository is deliberately layered so that a pull request can be
documentation-only, UI-only, database-only or security-relevant. That is what
gives EcoCI's test selection something meaningful to decide about.

| Layer | Module | Tests | EcoCI scope |
| --- | --- | --- | --- |
| Backend | `src/shop/pricing.py` | `tests/test_pricing.py` | `backend` |
| Database | `src/shop/repository.py` | `tests/test_repository.py` | `database` |
| Security | `src/shop/auth.py` | `tests/test_auth.py` | `security` (never skipped) |
| UI | `src/shop/web/templates.py` | `tests/test_templates.py` | `ui` |
| Docs | `docs/` | none | `documentation` |

## Run the tests

```bash
python -m pip install -e . pytest
python -m pytest -q
```

## Run them the way EcoCI does

With the EcoCI package installed, the pytest plugin records real per-test
durations and an energy estimate:

```bash
python -m pytest -p ecoci.pytest_plugin --ecoci-report ecoci_report.json -q
```

To execute only a chosen subset (this is what the scheduler's decision does):

```bash
printf 'tests/test_pricing.py::test_order_total_with_tax\n' > selected.txt
python -m pytest -p ecoci.pytest_plugin --ecoci-select selected.txt -q
```

## CI

`.github/workflows/ecoci.yml` asks the EcoCI control plane what to run, executes
that subset, measures it, reports the measurements back and comments the decision
on the pull request.

Set the repository variable `ECOCI_URL` to your control plane (for local
development, an `ngrok`/Cloudflare tunnel to `http://127.0.0.1:8000`). Without it
the workflow simply runs the full suite, so CI never breaks because the scheduler
is unreachable.

## Energy accounting honesty

Energy reported here is a **TDP x utilisation estimate**, not a hardware counter
reading, and every record is tagged `energy_source="tdp"`. Hardware energy via
Intel RAPL is Phase 5 of the project and requires Linux.

Carbon intensity comes from the [NESO Carbon Intensity API](https://carbonintensity.org.uk)
(free, no API key, CC BY 4.0).
