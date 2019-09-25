#!/usr/bin/env bash
pattern=$1
index_file=$2
# delete files in the cache directory
grep -P "$pattern" "$index_file" | awk '{print $1}' | xargs rm

# remove index entries from the index file
grep -P "$pattern" "$index_file" -n | awk -F ":" '{print $1}' | xargs -I @@ sh -c "sed -i '"@@"c\*****' "$index_file
