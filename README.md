# CondorErrorTracker.py usage details

The file CondorErrorTracker.py is a python script that tracks jobs as they transition through states in /var/log/condor/ShadowLog  
 
Input file:  
/var/log/condor/ShadowLog or local copy of ShadowLog        
 

Output files:              
ErrorClassification.txt - counts number of detected errors at each state for each job  
ErrorLog.txt - raw text of jobs with detected errors  
