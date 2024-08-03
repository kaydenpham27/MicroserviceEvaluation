#!/usr/bin/env python3

import sys
import re
import os
import shutil
import hashlib
import datetime
from collections import defaultdict 

# Getting SHA256 Hash
def SHA256(data): 
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode('utf-8'))
    hash_result = sha256_hash.hexdigest()
    return hash_result

# Fining Longest Common Subsequence between two sequences 
def FindingLCS(D1, D2):
    # Using dynamic programming to implement LCS
    n = len(D1); m = len(D2); f = [[0 for _ in range(m + 2)] for __ in range(n + 2)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            f[i][j] = max(f[i][j - 1], f[i - 1][j])
            if(D1[i - 1] == D2[j - 1]):
                f[i][j] = max(f[i][j], f[i - 1][j - 1] + 1)
    
    # Tracing LCS
    lcs = []
    while(n > 0 and m > 0):
        if (D1[n - 1] == D2[m - 1]):
            lcs.append(D1[n - 1]); n -= 1; m -= 1
        elif (f[n - 1][m] > f[n][m - 1]):
            n -= 1
        else:
            m -= 1
    lcs.reverse()
    return lcs

# Tracing differences based on LCS
def Difference(input, trace, D, LCS, output):
    with open(output, 'a') as output_file: output_file.write(f'From {input}: \n')
    pos = 0
    for i in range(len(D)):
        if (pos < len(LCS) and D[i] == LCS[pos]):
            pos += 1
        else :
            with open(output, 'a') as output_file: output_file.write(f"{trace[i][0]}({trace[i][1]}) = {trace[i][2]} \n")
    with open(output, 'a') as output_file: output_file.write(f"\n")

def DetectInconsistency(new_trace, baseline, inconsistencyStorage, mode):
    # If there is no baseline yet, we skip this part
    if (os.path.isfile(baseline) == False):
        return
    
    with open(inconsistencyStorage, 'a') as output_file:
        output_file.write(f'Comparing {new_trace} and {baseline}\n')

    # Open the strace output file for reading
    with open(new_trace, 'r') as file: raw_trace1 = file.read()
    with open(baseline, 'r') as file: raw_trace2 = file.read()

    # Extract system call information using pattern
    pattern = re.compile(r'(\w+)(?:\((.*?)\))?\s*=\s*(-?\d+|\?)')
    trace1 = re.findall(pattern, raw_trace1)
    trace2 = re.findall(pattern, raw_trace2)

    # Create unique digest from each line in a trace
    # line[0] syscall name
    # line[1] parameters
    # line[2] return value
    D1 = []; D2 = []
    for line in trace1: D1.append(SHA256((line[0] + line[1] + line[2] if mode == 1 else line[0])))
    for line in trace2: D2.append(SHA256((line[0] + line[1] + line[2] if mode == 1 else line[0])))
        
    # Find the Longest Common Subsequence between D1 and D2 (LCS)
    LCS = FindingLCS(D1, D2)
    
    # Print the differences between two traces
    Difference(new_trace, trace1, D1, LCS, inconsistency_storage)
    Difference(baseline, trace2, D2, LCS, inconsistency_storage)

def CreateDigest(new_trace, hashStringStorage, hashStorage, hashUniqueStorage, mode):
    # Extract information using pattern
    with open(new_trace, 'r') as file: raw_trace = file.read()
    pattern = re.compile(r'(\d+:\d+:\d+)\s+(\w+)(?:\((.*?)\))?\s*=\s*(-?\d+|\?)')
    matches = re.findall(pattern, raw_trace)

    # Hash 
    hashString = ""
    for match in matches:
        date, syscall, params, ret = match
        if(syscall != 'futex' and syscall != 'epoll_wait' and syscall != 'ioctl'):
            hashString = hashString + ((syscall + params + ret) if mode == 1 else syscall)
    digest = SHA256(hashString)
    with open(hashStringStorage, 'a') as output_file:
        output_file.write(f'{new_trace}: {hashString} \n') 
    with open(hashStorage, 'a') as output_file:
        output_file.write(f'{new_trace}: {digest} \n')
    
    # Add Digest To Unique Digest Storage
    included = False
    if (os.path.isfile(hashUniqueStorage)):
        with open(hashUniqueStorage, 'r') as file: hashUniqueList = file.read()
        pattern = re.compile(r'(.*?): (\w+)')
        hashUniqueList = re.findall(pattern, hashUniqueList)
        for [T, D] in hashUniqueList:
            if digest == D:
                included = True
                break
    if included == False:
        with open(hashUniqueStorage, 'a') as output_file:
            output_file.write(f'{new_trace}: {digest}')

def UpdateFrequency(oldBaseline, hashStorage, frequencyStorage):
    with open(f'{hashStorage}', 'r') as file: data = file.read()
    
    # Extract digest using pattern 
    pattern = re.compile(r'(.*?): (\w+)')
    hashList = re.findall(pattern, data)

    # Find the number of occurrences for each digest in the sample space
    eventNum = defaultdict(int); sampleSize = len(hashList); eventCandidate = defaultdict(str)
    
    for hash in hashList:
        fileNum, hashValue = hash; eventNum[hashValue] += 1
        eventCandidate[hashValue] = fileNum
    
    # Update new baseline
    newBaseline = eventCandidate[max(eventNum, key = eventNum.get)]
    if (newBaseline != oldBaseline):
        with open(newBaseline, 'r') as src, open(oldBaseline, 'w') as dst:
            dst.write(src.read())

    # Calculating probability for an event to happen in the sample space
    timestamp = datetime.datetime.now()
    with open(f'{frequencyStorage}', 'a') as output_file: 
        output_file.write(f"Probability Distribution At {timestamp}: \n")   
    for event, num in eventNum.items():
        Prob = num / sampleSize * 100
        with open(f'{frequencyStorage}', 'a') as output_file: 
            output_file.write(f"Digest: {event}, Probability: {Prob} \n")

if __name__ == "__main__":
    function_name = sys.argv[1]
    if function_name == "CreateDigest":
        filename = sys.argv[2]
        hashstring_storage = sys.argv[3]
        hash_storage = sys.argv[4]
        hashunique_storage = sys.argv[5]
        mode = int(sys.argv[6])
        CreateDigest(filename, hashstring_storage, hash_storage, hashunique_storage, mode)
    elif function_name == 'DetectInconsistency':
        filename = sys.argv[2]
        baseline = sys.argv[3]
        inconsistency_storage = sys.argv[4]
        mode = int(sys.argv[5])
        DetectInconsistency(filename, baseline, inconsistency_storage, mode)
    elif function_name == "UpdateFrequency":
        baseline = sys.argv[2]
        hash_storage = sys.argv[3]
        frequency_storage = sys.argv[4]
        UpdateFrequency(baseline, hash_storage, frequency_storage)
