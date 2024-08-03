#!/bin/bash

# Directory to monitor
DIRECTORY="$PWD"
HASHSTRING_STORAGE="$PWD/DigestString.txt"
HASH_STORAGE="$PWD/Digest.txt"
PROBABILITY_STORAGE="$PWD/Distribution.txt"
INCONSISTENCY_STORAGE="$PWD/Inconsistency.txt"
TOOL="$PWD/Tool.py"

# Function to calculate the hash of a file
calculate_hash() {
    python3 "$TOOL" "$1" "$2" "$3" "$4" "$5"
}

# Function to calculate the current probability distribution
calculate_probability() {
    python3 "$TOOL" "$1" "$2" "$3" "$4"
}

# Monitor the directory for new files
inotifywait -m -e create --format '%w%f' "$DIRECTORY" | while read FILE
do
    echo "New file detected: $FILE"
    sleep 5
    HASH=$(calculate_hash "CreatingDigest" "$FILE" "$HASHSTRING_STORAGE" "$HASH_STORAGE" 2)
    sleep 5
    PROBABILITY=$(calculate_probability "CalculatingProbability" "$HASH_STORAGE" "$PROBABILITY_STORAGE" "$INCONSISTENCY_STORAGE")
done
