#!/usr/bin/env sh
set -e

npm run build
source ./shell_scripts/auto_pipenv.sh
auto_pipenv_shell

if [ $# -eq 0 ] || [ "${1#-}" != "$1" ]; then
  set -- supervisord "$@"
fi

exec "$@"
