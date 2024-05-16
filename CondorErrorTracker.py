import re

# ShadowLog: Input data
# ErrorLog: Logs associated with 'bad' or 'irregular' jobs
# ErrorClassification: Index of 'bad' job id's and their error description
ShadowLog = open("/var/log/condor/ShadowLog", "r")
ErrorLog = open("ErrorLog.txt", "a")
ErrorIndex = open("ErrorClassification.txt", "a")

# Dictionary mapping jobs seen to states reached while runnning the script
jobs = {}

# List of 'bad' jobs
bad_jobs = []
# Dictionary mapping current state to possible 'good' next states
transitions = { 
    0 : [1, 2, 4], 
    1 : [2],
    2 : [4, 5],
    3 : [0, 1, 2],
    4 : [5],
    5 : [6],
    6 : [5]
}

states = {
    0 : "Idle in queue",
    1 : "File upload",
    2 : "Running",
    3 : "Hold",
    4 : "File Download",
    5 : "Terminated",
    6 : "Shadow exit"
}
# Dictionary mapping ShadowLog text to current state
state_patterns = [
    r"Initializing a VANILLA shadow", 
    r"Request to run .*ACCEPTED$", 
    r"Request to run .*DELAYED$",
    r"Request to run .*REFUSED$",
    r"^((?!peer stats).)*File Transfer Upload",
    r"File transfer completed successfully",
    r"File Transfer Download",
    r"Job disconnected",
    r"job is being evicted",
    r"going into Hold",
    r"graceful removal of job",
    r"File transfer failed",
    r"^terminated: exited with status",
    r"EXITING WITH STATUS" 
]

pattern_index = {0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 2, 6: 4, 7: 0, 8: 0, 9: 3, 10: 4, 11: 1, 12: 5, 13: 6}

# Regex for job id 
id_pattern = r"\((\d+\.\d+)\)"

for line in ShadowLog: # Read every line from ShadowLog determine which job it describes
    id = re.search(id_pattern, line) 
    if not id : continue 
    id = id.group(0)[1:-1]
    if id not in jobs:
        jobs[id] = {"log" : [], "state" : 0, "errors" : []} 
    for i, pattern in enumerate(state_patterns): # Determine which state/transition we are in
        message = re.search(pattern, line)
        if not message : continue
        if jobs[id]["state"] == -1 and i != 0: # Delete all jobs that didn't start in the current ShadowLog
           del jobs[id] 
           break 
        current_state = pattern_index[i] 
        jobs[id]["log"].append(line) 
        error = False
        if current_state == 2 and jobs[id]["state"] == 4: current_state = 5 
        if current_state not in transitions[jobs[id]["state"]]: error = True
        if current_state == 3:
            if i == 9: error = False
            if "PERIODIC_HOLD" in line: error = False
        if current_state == 0 and i == 2: error = False
        if current_state == 0 and i == 1: error = False
        if i == 11 and "status=0" in line: error = False
        if error:
            jobs[id]["errors"].append(states[jobs[id]["state"]] + " -> " + states[current_state])
        jobs[id]["state"] = current_state
        break
count = 0
for job in jobs:
    if jobs[job]["errors"] == []:
        continue
    else:
        count += 1
        for line in jobs[job]["log"]:
            ErrorLog.write(line)
            #ErrorLog.write('\n')
        ErrorIndex.write("bad transitions for job: " + job + "\n")
        for error in jobs[job]["errors"]:
            ErrorIndex.write(error + "\n")
        ErrorIndex.write("______________________________________________\n")
print("Error rate: " + str(count/len(jobs)) + "% out of " + str(len(jobs)) + " jobs")


