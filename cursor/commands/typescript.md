# TypeScript

- First check to make sure all changes are currently uncommitted changes. If there are uncommitted changes commit them with the message `cursor: stash before fixing typescript`. IT IS OK TO HAVE UNTRACKED FILES, just no uncommitted changes of tracked files
- `cd frontend/` and run `tsc --noEmit` to check for type errors.
- Fix all type errors and continue running tsc in a loop until there are no more errors. Keep iterating until tsc passes completely with no issues.

