# Workflow: Watch Runner Agent

## Trigger
```
Watch project and run tests
```

## Execution Flow

### Phase 1: Setup
1. Verify Python environment and dependencies
2. Confirm watcher script exists: `.copilot/watch_tests.py`
3. Prepare test command for the project

### Phase 2: Watching
1. Monitor file changes in:
   - `mailer/`
   - `validators/`
   - `tests/`
2. Detect changes to `.py` files
3. Debounce rapid modifications to avoid duplicate runs

### Phase 3: Test Execution
1. Run `python -m pytest -q --tb=line`
2. Capture pass/fail status
3. Log error output if tests fail

### Phase 4: Reporting
1. Report current watcher status
2. Summarize last test run
3. Highlight failures and changed files
4. Keep the watcher running until stopped manually

## Output
```
docs/test-reports/watch-summary.md
```

## Success Criteria
- Watcher działa w tle i reaguje na zmiany
- Testy uruchamiają się automatycznie po zapisie pliku
- Wyniki są czytelne i szybkie do interpretacji
