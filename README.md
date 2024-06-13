# CondorErrorTracker.py usage details

The file CondorErrorTracker.py is a python script that tracks jobs as they transition through states in /var/log/condor/ShadowLog  

*Must be run in a directory with access to ShadowLog, or manually changed to run on a local copy*
 
Input:  
none  

Output text:  
Error rate and total job count   

Output files:  
ErrorClassification.txt - counts number of detected errors at each state for each job  
ErrorLog.txt - raw text of jobs with detected errors  
