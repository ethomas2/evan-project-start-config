set -euxo pipefail
SRC=/Users/evanthomas/github.com/ethomas2/evan-project-start-config
DST=${1:-$(pwd)}
cp -ri "$SRC"/* "$DST"/

(
  cd "$DST"
  rm init.sh || true
  mv -i cursor .cursor || true
  mv -i claude .claude || true
  mv -i gitignore .gitignore || true
  mv -i envrc .envrc || true
  direnv allow
)

(
  cd $DST/backend/
  touch requirements.txt
  ~/.pyenv/versions/3.13.0/bin/python -m venv venv
  source venv/bin/activate
  pip install -r dev-requirements.txt
)

(
  cd "$DST"

  ln -s backend/venv
  ln -s backend/pylintrc
  ln -s backend/pyproject.toml

  git init
  git add .
  git commit -m "Initial commit"
)
