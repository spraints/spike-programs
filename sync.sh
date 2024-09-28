#!/bin/bash
#/ Usage: ./sync.sh [-m MESSAGE]

set -e
set -o nounset

set -x
mind-meld spike fetch --git refs/heads/spike "$@"
git push origin spike
