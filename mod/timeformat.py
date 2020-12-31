#!/usr/bin/env python3
# function to format time of seconds into a readable format
def format_time(seconds) -> str:
    minutes = seconds // 60 # integer division or whatever its called
    seconds = seconds % 60 # modulous obv
    hours = minutes // 60
    minutes = minutes % 60
    
    return(f'{int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds')
