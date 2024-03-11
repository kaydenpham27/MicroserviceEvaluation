#!/usr/bin/env python3

import sys
import re
import os
import hashlib
import datetime
from collections import defaultdict 

def SHA256(data): 
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode('utf-8'))
    #print(data.encode('utf-8'))
    hash_result = sha256_hash.hexdigest()
    return hash_result

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
        if (f[n][m] == f[n - 1][m]):
            n -= 1
        elif (f[n][m] == f[n][m - 1]):
            m -= 1
        else:
            lcs.append(D1[n - 1]); n -= 1; m -= 1
    lcs.reverse()
    return lcs

def Difference(input, trace, D, LCS, output):
    with open(output, 'a') as output_file: output_file.write(f'From {input}: \n')
    pos = 0
    for i in range(len(D)):
        if (pos < len(LCS) and D[i] == LCS[pos]):
            pos += 1
        else :
            with open(output, 'a') as output_file: output_file.write(f"{trace[i][0]}({trace[i][1]}) = {trace[i][2]} \n")
    with open(output, 'a') as output_file: output_file.write(f"\n")

def Comparing(input1, input2, output):
    with open(output, 'a') as output_file:
        output_file.write(f'Comparing {input1} and {input2} \n')

    # Open the strace output file for reading
    with open(input1, 'r') as file: raw_trace1 = file.read()
    with open(input2, 'r') as file: raw_trace2 = file.read()

    # Extract system call information using pattern
    pattern = re.compile(r'(\w+)(?:\((.*?)\))?\s*=\s*(-?\d+|\?)')
    trace1 = re.findall(pattern, raw_trace1)
    trace2 = re.findall(pattern, raw_trace2)

    # Create unique digest from each line in a trace
    # line[0] syscall name
    # line[1] parameters
    # line[2] return value
    D1 = []; D2 = []
    mode = 2
    for line in trace1: D1.append(GetHash((line[0] + line[1] + line[2] if mode == 1 else line[0])))
    for line in trace2: D2.append(GetHash((line[0] + line[1] + line[2] if mode == 1 else line[0])))
        
    # Find the Longest Common Subsequence between D1 and D2 (LCS)
    LCS = FindingLCS(D1, D2)
    
    # Print the differences between two traces
    Difference(input1, trace1, D1, LCS, output)
    Difference(input2, trace2, D2, LCS, output)

def CreatingDigest(input_file, output_file1, output_file2, mode):
    # Extract information using pattern
    with open(input_file, 'r') as file: raw_trace = file.read()
    pattern = re.compile(r'(\d+:\d+:\d+)\s+(\w+)(?:\((.*?)\))?\s*=\s*(-?\d+|\?)')
    matches = re.findall(pattern, raw_trace)

    # Hash 
    hashString = ""
    for match in matches:
        date, syscall, params, ret = match
        #print(syscall)
        if(syscall != 'futex' and syscall != 'epoll_wait' and syscall != 'ioctl'):
            hashString = hashString + ((syscall + params + ret) if mode == 1 else syscall)
    #print(hashString)
    #print(SHA256(hashString))
    with open(output_file1, 'a') as output_file:
        output_file.write(f'{input_file}: {hashString} \n') 
    with open(output_file2, 'a') as output_file:
        output_file.write(f'{input_file}: {SHA256(hashString)} \n')

def CalculatingProbability(input, output, output1):
    with open(f'{input}', 'r') as file: data = file.read()

    # Extract digest using pattern 
    pattern = re.compile(r'(.*?): (\w+)')
    hashList = re.findall(pattern, data)

    # Find number of happening times for each event in the sample space
    eventNum = defaultdict(int); sampleSize = len(hashList); eventCandidate = defaultdict(str)
    
    for hash in hashList:
        fileNum, hashValue = hash; eventNum[hashValue] += 1
        eventCandidate[hashValue] = fileNum
        #print(fileNum, hashValue)
    
    Baseline = eventCandidate[max(eventNum, key = eventNum.get)]

    # Calculating probability for an event to happen in the sample space
    timestamp = datetime.datetime.now()
    with open(f'{output}', 'a') as output_file:
            output_file.write(f"Probability Distribution At {timestamp}: \n")
    with open(f'{output1}', 'a') as output_file:
            output_file.write(f"------------------------------------------------------------------ \n")
            output_file.write(f"Inconsistency Detected At {timestamp}: \n")
    
    for event, num in eventNum.items():
        # if (eventCandidate[event] != Baseline):
            # Need to add more 
            #Comparing(Baseline, eventCandidate[event], output1)
        Prob = num / sampleSize * 100
        with open(f'{output}', 'a') as output_file: 
            output_file.write(f"Digest: {event}, Probability: {Prob} \n")

if __name__ == "__main__":
    function_name = sys.argv[1]
    if function_name == "CreatingDigest":
        filename = sys.argv[2]
        hashstring_storage = sys.argv[3]
        hash_storage = sys.argv[4]
        mode = int(sys.argv[5])
        CreatingDigest(filename, hashstring_storage, hash_storage, mode)
    elif function_name == "CalculatingProbability":
        hash_storage = sys.argv[2]
        probability_distribution_storage = sys.argv[3]
        inconsistency_storage = sys.argv[4]
        CalculatingProbability(hash_storage, probability_distribution_storage, inconsistency_storage)













