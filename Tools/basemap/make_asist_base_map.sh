#!/usr/bin/env bash

if [[ -n "$asist_testbed" ]]; then
    echo "Using testbed home as $asist_testbed"
    echo
else
    echo "Need env var asist_testbed set to testbed directory"
    echo $asist_testbed
    exit 1
fi

if [[ -n "$1" ]]; then
    echo "MC Mission Map $1"
    echo
else
    echo "Need Map Name"
    echo "Usage: $0 Map_Name"
    exit 1
fi

map_name=$1
program=$(basename $0)
pdir=$(dirname $0)

ulimit -n 4096
(cd $pdir/ASIST-MC-toolbox ; ./testbed_to_json.py $map_name)
RESULT=$?
#echo $RESULT
if [[ $RESULT != 0 ]]; then
  exit 1
fi
jsn_file="$pdir/ASIST-MC-toolbox/$map_name/$map_name.json"

echo "Processing extracted blocks"
java -jar $pdir/IMCW/Import-MC-World/bin/imcw.jar -i $jsn_file -o "$map_name.json" -l import
ls -lsat "$map_name.json"
echo "Done"
#java -jar $pdir/IMCW/Import-MC-World/bin/imcw.jar -i $jsn_file -o "$map_name.tmp.json" import
#python3 -m json.tool "$map_name.tmp.json" "$map_name.json"
#rm "$map_name.tmp.json"
