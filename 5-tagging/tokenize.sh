#!/bin/bash

target="ustawy"
let count=0
for f in "$target"/*
do
	# if [[ $count != 1 ]]; then
    	curl -XPOST localhost:9200 --data-binary "@$f" > "tokeny/$(basename $f)"
    	let count=count+1
		# exit
	# fi 	
	
done
echo ""
echo "Count: $count"
