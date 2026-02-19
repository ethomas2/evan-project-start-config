# Fix TODOs

- First check to make sure all changes are currently committed. No dirty changes. If there are dirty changes commit them with the message `cursor: stash before fixing TODOs`.

- Run `rg -i 'TODO.*(cursor)' -g '*.py' --vimgrep` to find all TODOs in the codebase that I want you to fix.

- ONLY fix the TODOs annotated with (cursor). DO NOT fix or delete the TODOs annotated with (evan). I will fix those myself.

- After fixing each TODO commit your changes with a meaningful commit message. Always prefix the commit message with `cursor: `. E.g.
```
cursor: Fixed TODO in backend/utils.py to handle edge case in data processing
```
