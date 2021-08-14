#!/bin/bash

shopt -s globstar

export EDITOR=nvim

script_path=$(realpath "${BASH_SOURCE[0]}")
script_dir=$(dirname "$script_path")
source_dir="$(dirname "$script_dir")/src"

PYTHONPATH=$source_dir
cd "$source_dir" || return
for d in **/; do
  if [[ $(basename "$d") != "__pycache__" ]]; then
    PYTHONPATH="${PYTHONPATH}:$(realpath "$d")"
  fi
done
export PYTHONPATH

export python_virtualenv="${HOME}/python_envs/udemy_flask/bin/activate"
