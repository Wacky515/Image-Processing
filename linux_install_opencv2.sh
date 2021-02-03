#!/usr/bin/env bash
# @(#) Pip OpenCV
# Created:     201*/**/** **:**:**
# Last Change: 2021/02/02 14:11:39.

set -euo pipefail
export LC_ALL=C

## 関数
[ -f ~/.bash_function ] && source ~/.bash_function

readonly         APPS="OpenCV"
readonly  ACTION_LOWC="pip"
readonly  ACTION_PROP="Pip"
readonly PROCESS_LOWC=${ACTION_LOWC}" "${APPS}
readonly PROCESS_PROP=${ACTION_PROP}" "${APPS}

gm_echo ">> Start ${PROCESS_LOWC}"

sudo apt install -y python-numpy
sudo apt install -y python-opencv

result_echo $? "${PROCESS_LOWC}"
