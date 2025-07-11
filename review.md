# Review Note

## veggie_w3.py

- Don't nested try-catch, try-catch should be concentrated on individual potential exception.

- **Filter out** unexpected result with early return

- Walrus operator

- Replace function comments with docstring

- Avoid returning both success / fail result.
  Handle the unexpected outcome with custom Exception.

- Early return with `continue` within loop.

- `traceback`: module for tracing exception.

- English-based naming.

## git ignore

- `__pycache__`
- [.streamlit/secrets.toml](https://docs.streamlit.io/develop/concepts/connections/secrets-management)

> [!WARNING]
> Add this file to your `.gitignore` so you don't commit your secrets!

## veggie_w4_schedule.py

- Avoid override `sys.stdout` / `sys.stderr`, it's a bit dangerous.
  - stdout / stderr on command line level:
    ```bash
    python veggie_w4_schedule.py >schedule.log 2>schedule.error
    ```
  - decorator + partial print function
  - python [logger library](https://docs.python.org/3/library/logging.html)
