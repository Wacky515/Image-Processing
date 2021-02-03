#!/usr/bin/env bash
# @(#) Clone dependencies
# Created:     201*/**/** **:**:**
# Last Change: 2021/02/02 14:09:55.

set -euo pipefail
export LC_ALL=C

## 関数
[ -f ~/.bash_function ] && source ~/.bash_function

readonly         APPS="dependencies"
readonly  ACTION_LOWC="clone"
readonly  ACTION_PROP="Clone"
readonly PROCESS_LOWC=${ACTION_LOWC}" "${APPS}
readonly PROCESS_PROP=${ACTION_PROP}" "${APPS}

gm_echo ">> Start ${PROCESS_LOWC}"

if [ -e ~/Sound/.git/ ]; then
    echo ">> Git clone Sound"
    git clone https://github.com/Wacky515/Sound.git
else
    echo ">> Already clone Sound"
fi

if [ -e ~/Serial/.git/ ]; then
    echo ">> Git clone Serial"
    git clone https://github.com/Wacky515/Serial.git
else
    echo ">> Already clone Serial"
fi

if [ -e ~/SaveData/.git/ ]; then
    echo ">> Git clone SaveData"
    git clone https://github.com/Wacky515/SaveData.git
else
    echo ">> Already clone SaveData"
fi

result_echo $? "${PROCESS_LOWC}"
