# from distutils.command.upload import upload
# import imp
# from turtle import down
import psutil
import time
import os
import pandas as pd

# from TotalNetworkUsage import UPDATE_DELAY







UPDATE_DELAY = 1 # in seconds

def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes: .2f}{unit}B"
        bytes /= 1024
        
        
        
        
        
        
        
#get the network I/O stats from the psutil on each network interface
#by setting `pernic` to `True`
io = psutil.net_io_counters(pernic=True)

#Let's now enter the `while loop`
while True:
    #sleep for `UPDATE_DELAY` seconds
    time.sleep(UPDATE_DELAY)
    
    #get the network I/O stats again per interface
    io_2 = psutil.net_io_counters(pernic=True)
    
    #initialize the data to gather a list of dicts
    data = []
    
    for iface, iface_io in io.items():
        
        #new - old stats gets us speed 
        upload_speed, download_speed = io_2[iface].bytes_sent  - iface_io.bytes_sent, io_2[iface].bytes_recv - iface_io.bytes_recv
        data.append({
            "iface": iface, "Download": get_size(io_2[iface].bytes_recv),
            "Upload": get_size(io_2[iface].bytes_sent),
            "Upload Speed": f"{get_size(upload_speed / UPDATE_DELAY)}/s",
            "Download Speed": f"{get_size(download_speed / UPDATE_DELAY)}/s",
            
        })
        
        
        
        
    #update the I/O stats for the next iteration
    io = io_2
    
    #construct a Pandas DataFrame to print stats in a cool tabular style
    df = pd.DataFrame(data)
    
    #sort the values per column, (or any)
    df.sort_values("Download", inplace=True, ascending=False)
    
    #clear the screen based on your OS
    os.system("cls") if "nt" in os.name else os.system("clear")
    
    #print the stats
    print(df.to_string()) 
    
    """
    This time, the psutil.net_io_counters() returns a dictionary of each 
    interface and its corresponding network stats. Inside the while loop, we 
    iterate over this dictionary and do the same calculation as before.

    Since we have multiple lines, we're using pandas to print the stats in a
    tabular manner and use the cls command on Windows or clear on Linux or 
    macOS to clear the screen before printing the updated results.

    To print the whole pandas dataframe, we simply call the to_string() 
    method inside the print() function and it did the job
    """