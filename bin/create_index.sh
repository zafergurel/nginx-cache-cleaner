#!/usr/bin/env bash
op=$1
folder=$2
output_file=$3
delta=${4:--30}

if [ $op == "append" ] 
then
    find $folder -maxdepth 1 -type f -mtime $delta | xargs -P 16 -I @@ bash -c 'head -n 3 @@ | awk '\''/KEY: (.+)/{print "'@@'", $2}'\'' ' >> $output_file
elif [ $op == "create" ]
then
    find $folder -maxdepth 1 -type f -mtime $delta | xargs -P 16 -I @@ bash -c 'head -n 3 @@ | awk '\''/KEY: (.+)/{print "'@@'", $2}'\'' ' > $output_file
fi

# touch file to update its timestamp
touch $output_file