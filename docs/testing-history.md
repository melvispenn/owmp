# Testing History

This file records important verification activities. Executable tests remain in the project test directories.

| Date | Area | Test or verification | Purpose | Result |
|---|---|---|---|---|
| 2026-09-25 | Tailwind CLI | npm run css:build | Verify the official Tailwind CLI generates Django's static CSS output | Passed |
| 2026-09-25 | Tailwind assets | tests/frontend/test_tailwind_assets.py | Verify input configuration, template integration, and CLI output | Passed: 3 tests |

| 2026-11-16 | Project test environment | pytest with default test settings | Run the unit test suite without requiring a local PostgreSQL server | Passed: 37 tests, with existing staticfiles warning |
