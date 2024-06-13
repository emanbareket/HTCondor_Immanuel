# CondorErrorTracker.py usage details

The file CondorErrorTracker.py is a python script that tracks jobs as they transition through states in /var/log/condor/ShadowLog

Input file: /var/log/condor/ShadowLog 
\n*can be changed manually to run on a local copy of ShadowLog


Output files: \n
ErrorClassification.txt - counts number of detected errors at each state for each job \n
ErrorLog.txt - raw text of jobs with detected errors
