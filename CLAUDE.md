# Persistent Instructions
- Always make plans extremely concise; favor concision over full grammar.
- At the end of each plan, list unresolved questions to answer.
- When writing functions put a high level overview of teh function in a docstring. Eg.
```python
def dry_run(cfg: config.Config) -> None:
    1. List local files and remote files.
    2. Print files to upload (local - remote).
    3. Print files to maybe delete (remote - local).
    4. Don't sync anything.
    """
    local_files = set(_list_local_files(cfg.local_src_path))
    remote_files = _list_remote_files(cfg)

    to_upload = sorted(local_files - remote_files)
    to_maybe_delete = sorted(remote_files - local_files)

    if to_upload:
        print("Files to upload:")
        for f in to_upload:
            print(f"  + {f}")
    else:
        print("No files to upload.")

    print()

    if to_maybe_delete:
        print("Files on Whatbox that don't exist locally (consider deleting):")
        for f in to_maybe_delete:
            print(f"  - {f}")
    else:
        print("No extra files on Whatbox.")

    print()
    print("Running in --dry-run mode. Use --execute to sync changes")

```

# Backend Architecture
- note directory structure (backend/{app,db/config,models,schemas}.py) which should include respectively
    - app.py :: all fastapi stuff
    - db.py :: all interaction with the db. Every function accepts a sqlalchemy
              session and args which are python primitives or pydantic objects.
             Every function returns python primitives or pydantic objects. No orm models leak outside
    - config.py :: Definition of all config. Config is a pydantic object of
                   relevant env variables. E.g. config.COnfig.db_connection_string. Config
                   object is instantiated once in main.py as cfg = config.Config.from_env()
                   (classmethod)
    - models.py :: definition of sqlalchemy models
    - schemas.py :: definition of all db pydnatic objects and all fastapi request/response objects

# Executing plans
1. Always make plans extremely concise; favor concision over full grammar.
2. At the end of each plan, list unresolved questions to answer.
3. When Executing plans, FIRST make python code that has "stubs" written out. I.e.
has all the functions that you need but only has the function names and types.
The "implementation" is pseudocoded in docstrings
4. After making stubs ask the user to review. Fill in the stubs with real python code
5. After approval replace stubs with real code. LEAVE THE DOCSTRINGS
