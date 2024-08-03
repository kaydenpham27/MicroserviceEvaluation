#!/bin/bash

for i in {1..400}; do
	curl http://127.0.0.1:5000/emp
	#curl -X POST http://127.0.0.1:5000/create -H "Content-Type: application/json" -H "Accept: application/json" -d '{"name":"TestUser $i", "email":"test@domain.com", "phone":"123456789", "address": "QUT"}'
	#curl -X DELETE "http://127.0.0.1:5000/delete/$i"
	#curl -X DELETE http://127.0.0.1:5000/delete/103
	sleep 2
done

#python_script="hashing.py"

#for input in $(cat "inputsize16.txt" | tr -s '[:space:]' '\n'); do
    #echo "Running with input: $input"
    #curl -X POST http://127.0.0.1:5000/create -H "Content-Type: application/json" -H "Accept: application/json" -d '{"name":"$input", "email":"test@domain.com", "phone":"123456789", "address": "QUT"}'    
    # You can add additional processing here if needed
#done
