#!/usr/bin/env bash
grep -P "$1" $2 | awk '{print $1}' | xargs rm