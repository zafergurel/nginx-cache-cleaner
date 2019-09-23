#!/usr/bin/env bash
if find $1 -maxdepth 0 -empty | read v; then echo 1; else echo 0 ; fi