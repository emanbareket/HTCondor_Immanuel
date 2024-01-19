import re

ShadowLog = open("/var/log/condor/ShadowLog", "r")
GlobalEventLog = open("/var/log/condor/GlobalEventLog", "r")
GEL_Repeated_States = open("GEL_Repeated_States", "a")
GEL_Unexpected_Transitions = open("GEL_Unexpected_Transitions", "a")
pattern = re.compile(r"\((\d+\.\d+)")
jobs = {}
states = ["Job submitted from host", 
          "Started transferring input files", 
          "Finished transferring input files",
          "Warning from starter",
          "Job executing on host",
          "Started transferring output files",
          "Finished transferring output files",
          "Job terminated"]
count = 0
for line in GlobalEventLog:
    id = pattern.search(line)
    if(id != None):
        id = id.group(0)
        if(id not in jobs):
            jobs[id] = []
        for state in states:
            if state in line:
                jobs[id].append(state)
        count+=1
repeated = 0
missing = 0
for job in jobs:
    if(jobs[job] and jobs[job][0] == states[0] and jobs[job][len(jobs[job])-1] == states[7] and jobs[job] != states):
        if(len(jobs[job]) < len(states)):
            GEL_Unexpected_Transitions.write(job[1:])
            GEL_Unexpected_Transitions.write("      States reached:")
            for i in range(len(states)):
                if(states[i] in jobs[job]):
                    GEL_Unexpected_Transitions.write(str(i))
                    GEL_Unexpected_Transitions.write(", ")
            GEL_Unexpected_Transitions.write("\n")
            missing += 1
        elif(len(jobs[job]) > len(states)):
            GEL_Repeated_States.write(job[1:])
            GEL_Repeated_States.write("       Repeated states: ")
            for j in range(len(states)):
                if(jobs[job].count(states[j]) > 1):
                    GEL_Repeated_States.write(str(j))
                    GEL_Repeated_States.write(", ")
            GEL_Repeated_States.write("\n")
            repeated += 1
print("Jobs with repeated states:", repeated, "Percent of total:", repeated / count)
print("Jobs with missing states:", missing, "Percent of total:", missing / count)
GEL_Repeated_States.close()   
GEL_Unexpected_Transitions.close() 
GlobalEventLog.close()        
ShadowLog.close()
