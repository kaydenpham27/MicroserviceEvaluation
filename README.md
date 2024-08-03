# FUSE Microservice Evaluation
- This is the source code (developed by me) for FUSE Microservice Evaluation method mentioned in this [paper](https://link.springer.com/chapter/10.1007/978-3-031-48421-6_17).
- Feel free to use it for research purpose.

# Table of Contents
## Installation Instructions ##
### Prerequisites ###
- Linux Strace Built-in Tool
- Python Packages
### Installation Steps ### 
1. Linux Environment/Strace
  - Enables Windows Subsystem for Linux
  - Install A Linux distribution (e.g., Ubuntu) 
  - Set up Linux Environment by following on-screen instructions
  - Install strace ([Detailed Linux Strace Document](https://man7.org/linux/man-pages/man1/strace.1.html)):
    ```sh
    sudo apt install strace
    ```
2. Python Packages:
   ```sh
   sudo apt install python3
   ```
3. Inotify WSL:
   ```sh
   sudo apt install inotify-tools
   ```
4. Tool Setup:
   ```sh
   git clone https://github.com/kaydenpham27/MicroserviceEvaluation/
   sudo chmod a+x Auto.sh fuzz.sh Tool.py
   ```
## Usage
In the example below, I use a simple RestAPI (main.py) as the evaluating microservice, feel free to change it with your actual testing software. 
Besides, one might need multiple Linux screens running simultaneously for different purposes, including running the evaluating software, tracing the software information, running FUSE and issuing requests to the software. I recommend using Linux Screen, a terminal multiplexer that allows you to manage multiple terminal sessions within a single window, however, opens multiple windows would also work. 
### Example
1. Run the evaluating software/application (screen 1):
   ```sh
   python main.py
   ```
2. Grep the running application's ProcessID:
   ```sh
   ps aux | grep main.py 
   ```
3. Attach Strace to the running application's ProcessID (PID) (screen 2):
   ```sh
   sudo strace -f -ff -o strace_output.txt -s 4096 -t -v -p PID
   ```
4. Starts the inotify watches (screen 3):
   ```sh
   sudo .\Auto.sh
   ```
5. (Optional) Running fuzzer to issue requests automatically for software evaluating (screen 4):
   ```sh
   sudo .\fuzz.sh
   ```
### Results
- After each request, strace produces a strace_output.txt file representing the combination of system calls used by Kernel to handle the most recent request:
  ![Trace Example](https://github.com/kaydenpham27/MicroserviceEvaluation/blob/main/Images/Trace_Example.png)
- Digest.txt is updated with the digest value (hash value) of the latest created trace (strace_output.txt file):
  ![Digest Example](https://github.com/kaydenpham27/MicroserviceEvaluation/blob/main/Images/Digest_Example.png)
- DigestString.txt is updated with the hashing string of system call (optionally their parameters and return values) of the latest created trace:
- Distribution.txt is updated with the new frequency distribution of unique digests in the sample space:
- Inconsistency.txt is updated with inconsistencies between the newly created trace and the baseline trace:
