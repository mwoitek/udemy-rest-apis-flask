#!/bin/bash

script_path=$(realpath "$0")
script_dir=$(dirname "$script_path")
source "${script_dir}/environment.sh"

if [[ -z "$1" ]]; then
  $EDITOR
else
  file_path=$(realpath "$1")
  $EDITOR "$file_path"
fi
