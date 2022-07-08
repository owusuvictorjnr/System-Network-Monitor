"""
This software monitors the network usage of you machine.
It monitors the total nework usage, network usage per network
interface, and network usage per system process.
"""

import psutil 
import time



"""
Total Network Usage
"""


UPDATE_DELAY = 1 # in seconds

def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes: .2f}{unit}B"
        
        bytes /= 1024
        
        
        
        
        
"""
Next, we will use psutil.net_io_counter() function 
that returns the network input and output statistic.
"""

#get the network I/O stats from psutil
io = psutil.net_io_counters()

#extract the total bytes sent and received
bytes_sent, bytes_recv = io.bytes_sent, io.bytes_recv

"""
Now, let's enter the loop that gets the same stats but 
after a delay so we can calcualte the download  and upload speed.
"""

while True:
    #sleep for `UPDATE_DELAY` seconds
    time.sleep(UPDATE_DELAY)
    
    #get the stats again
    io_2 = psutil.net_io_counters()
    
    #new - old stats gets us the speed
    us, ds = io_2.bytes_sent - bytes_sent, io_2.bytes_recv - bytes_recv
    
    #print the total download/upload along with current speeds
    print(f"Upload: {get_size(io_2.bytes_sent)}     "
          f", Download: {get_size(io_2.bytes_recv)}     "
          f", Upload Speed: {get_size(us / UPDATE_DELAY)}/s     "
          f", Download Speed: {get_size(ds / UPDATE_DELAY)}/s       ", end="\r")
    
    #update the bytes_sent and bytes_recv for next iteration
    bytes_sent, bytes_recv = io_2.bytes_sent, io_2.bytes_recv
    
    
    
"""
We simply subtracted the old netwotk stats from the new stats to get the speed, 
we will also include the total downloaded and uploaded stats. Since we want the 
printing to be updated in one line and not printed in several lines, we pass the 
return character '\r' to the 'end'  parameter in the 'print()' function to return 
to the beginning of the same line after printing.
"""

