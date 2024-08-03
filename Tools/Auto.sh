#!/bin/bash

# Directory to monitor
DIRECTORY="$PWD"
HASHSTRING_STORAGE="$PWD/DigestString.txt"
HASHUNIQUE_STORAGE="$PWD/DigestUnique.txt"
HASH_STORAGE="$PWD/Digest.txt"
BASELINE="$PWD/Baseline.txt"
PROBABILITY_STORAGE="$PWD/Distribution.txt"
INCONSISTENCY_STORAGE="$PWD/Inconsistency.txt"
TOOL="$PWD/Tool.py"

# Function to calculate the hash of a file
calculate_hash() {
    python3 "$TOOL" "$1" "$2" "$3" "$4" "$5" "$6"
}

# Function to calculate the current probability distribution
calculate_probability() {
    python3 "$TOOL" "$1" "$2" "$3" "$4"
}

# Function to detect inconsistencies between newly created trace and baseline trace
detecting_abnormal_behavior() {
    python3 "$TOOL" "$1" "$2" "$3" "$4" "$5"
}

# Ensure necessary files exist
create_if_not_exists() {
    if [ ! -f "$1" ]; then
        touch "$1"
        echo "Created file: $1"
    fi
}

create_if_not_exists "$HASHSTRING_STORAGE"
create_if_not_exists "$HASHUNIQUE_STORAGE"
create_if_not_exists "$HASH_STORAGE"
create_if_not_exists "$BASELINE"
create_if_not_exists "$PROBABILITY_STORAGE"
create_if_not_exists "$INCONSISTENCY_STORAGE"

# Monitor the directory for new files
inotifywait -m -e create --format '%w%f' "$DIRECTORY" | while read FILE
do
    echo "New file detected: $FILE"
    sleep 5
    # Create Digest for newly created trace
    HASH=$(calculate_hash "CreateDigest" "$FILE" "$HASHSTRING_STORAGE" "$HASH_STORAGE" "$HASHUNIQUE_STORAGE" 2)
    sleep 5
    # Detects inconsistencies between newly created trace and baseline trace
    INCONSISTENCY=$(detecting_abnormal_behavior "DetectInconsistency" "$FILE" "$BASELINE" "$INCONSISTENCY_STORAGE" 2)
    sleep 5
    # Updates the frequency distribution
    PROBABILITY=$(calculate_probability "UpdateFrequency" "$BASELINE" "$HASH_STORAGE" "$PROBABILITY_STORAGE")
    sleep 5
done
