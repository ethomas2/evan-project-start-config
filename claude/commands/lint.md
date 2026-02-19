# Lint

- First check to make sure all changes are currently committed. No dirty changes. If there are dirty changes commit them with the message `cursor: stash before linting`.
- Activate the virtual environment with `source venv/bin/activate`,  then run pylint on the codebase to check for linting errors.
- Fix all linting errors and continue running pylint in a loop until there are no more errors. Keep iterating until pylint passes completely with no issues.
