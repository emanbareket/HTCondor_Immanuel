# CondorErrorTracker.py usage details

The file CondorErrorTracker.py is a python script that tracks jobs as they transition through states in the HTCondor system by parsing the ShadowLog file in /var/log/condor. It is based on a logical state machine reverse engineered by examining logs, and is therefore not an exact representation of the HTCondor system, but an overall good model. The script uses regular expression patterns in the ShadowLog to determine what state transition the job is going through and whether it should be considered an error or not. Since error messages can vary drastically, there may be some errors that are overlooked or wrongly classified, but the vast majority of errors will be detected, categorized, and documented by this script.  

*Must be run in a directory with access to /var/log/condor/ShadowLog, or manually changed to run on a local copy*

 
Input:  
none  

Output text:  
Error rate and total job count   

Output files:  
ErrorClassification.txt - counts number of detected errors at each state for each job  
ErrorLog.txt - raw text of jobs with detected errors  
