# Pyright


- First check to make sure all changes are currently uncommitted changes. If there are uncommitted changes commit them with the message `cursor: stash before fixing pyright`. IT IS OK TO HAVE UNTRACKED FILES, just no uncommitted changes of tracked files
- Activate the virtual environment with `source venv/bin/activate` then run `pyright backend/ experiments/` to check for type errors.
- Fix all type errors and continue running pyright in a loop until there are no more errors. Keep iterating until pyright passes completely with no issues.
