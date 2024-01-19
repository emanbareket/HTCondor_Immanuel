# HTCondor_Immanuel

The file LogParser.py is a python script that scans through the GlobalEventLog and filters jobs based on whether states were repeated or if any unexpected transitions occurred. It also counts and prints the percentage of these errors. There is currently no input, and the two output files "GEL_Unexpected_Transitions" and "GEL_Repeated_States" are appended to everytime the script is run. The code still needs some cleaning and more features will be added including the ShadowLog state transitions allowing for it to run on that as well.
