# CondorErrorTracker.py usage details

The file CondorErrorTracker.py is a python script that tracks jobs as they transition through states in /var/log/condor/ShadowLog

Input file: *can be changed manually to run on a local copy of the ShadowLog*
/var/log/condor/ShadowLog


Output files:
ErrorClassification.txt - counts number of detected errors at each state for each job
ErrorLog.txt - raw text of jobs with detected errors
