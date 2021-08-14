#!/bin/bash

script_path=$(realpath "$0")
script_dir=$(dirname "$script_path")
source "${script_dir}/environment.sh"

source "$python_virtualenv"

root_dir=$(dirname "$script_dir")
cd "$root_dir" || return

python_script_path="${root_dir}/src/app.py"
python3 "$python_script_path"
