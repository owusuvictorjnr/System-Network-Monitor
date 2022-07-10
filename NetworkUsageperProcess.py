"""
In this tuttorial, I will be introducing you to a new framework or library called Scapy.
Scapy is a powerful packet manipulation tool that provides us the ability to 
sniff outgoing and incoming packets in our machine. If you want to learn more about it,
use the docs of it.


This time, I will use the psutil library to get the current network connections and 
extract the source and destination ports and the process ID (PID) that is responsible 
for the connection.

We then match this information while sniffing for packets using Scapy and put the 
traffic stats in the corresponding PID.
"""

from py import process
from scapy.all import *
import psutil
from collections import defaultdict
import os
from threading import Thread
import pandas as pd



#Get the all network adapter's MAC addresses
all_macs = {iface.mac for iface in ifaces.values()}

#A dictionary to map connection to its corresponding Process ID (PID)
connection2pid = {}

#A dictiondary that to map each process ID (PID) to total Upload (0) and Download (1)
#traffic
pid2traffic = defaultdict(lambda: [0, 0])

#The global Pandas DataFrame that's used to track previous traffic stats
global_df = None

#Global boolean for status of the program 
is_program_running = True


def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes: .2f}{unit}B"
        bytes /= 1024
        
"""

*all_macs* is a Python set that contains the MAC addresses of all network interfaces in our machine.
*connection2pid* is a Python dictionary that maps each connection (represented 
as the source and destination ports on the TCP/UDP layer).
*pid2traffic* is another dictionary that maps each process ID (PID) to a list 
of two values representing the upload and download traffic.
*global_df* is a Pandas dataframe that is used to store the previous 
traffic data (so we can calculate the usage).
*is_program_running* is simply a boolean that is when set to False, 
the program will stop and exit.

"""

"""
The use of Scapy and its models sniff()
"""

def process_packet(packet):
    global pid2traffic
    
    try:
        #Get the packet source and destination IP address and ports
        packet_connection = (packet.sport, packet.dport)
        
    except (AttributeError, IndexError):
        
        #Sometimes the packet does not have TCP/UDP layers, we just these packets
        pass
    
    else:
        #get the PID responsible for this connection from our `connection2pid` global dictionary
        packet_id = connection2pid.get(packet_connection)
        
        if packet_id:
            if packet.src in all_macs:
                #The source MAC address of the packet is our MAC address
                #So it's an outgoing packet, meaning it's upload.
                pid2traffic [packet_id][0] += len(packet)
                
            else:
                #incoming packet, download
                pid2traffic[packet_id][1] += len(packet)
                
                
                

"""
The `process_packet()` callback accepts a packet as an argument. If there are 
TCP or UDP layers in the packet, it extracts the source and destination ports 
and tries to use the connection2pid dictionary to get the PID responsible for 
this connection. If it does find it, and if the source MAC address is one of 
the machine's MAC addresses, then it adds the packet size to the upload traffic. 
Otherwise, it adds it to the download traffic.
"""

"""
function responsible for getting the connections
"""

def get_connections():
    """
    A function that keeps listening for connections on this machine 
    and adds them to `connection2pid` global variable
    """
    
    global connection2pid
    
    while is_program_running:
        #using psutil, we can grab each connection's sources and destination ports
        #and their process ID
        for c in psutil.net_connections():
            if c.laddr and c.raddr and c.pid:
                #if local address, remote address and PID are in the connection
                #add them to our global dictionary 
                connection2pid[(c.laddr.port, c.raddr.port)] = c.pid
                connection2pid[(c.raddr.port, c.laddr.port)] = c.pid
                
        #Sleep for a second(in can be adjusted to whatever you want)
        time.sleep(1)

"""
The above function is the one accountable for filling the connection2pid global 
variable that is used in the process_packet() function
"""

# function that calculates the network usage and prints our collected data

def print_pid2traffic():
    global global_df
    
    #initialize the list of processes
    processes = []
    
    for pid, traffic in pid2traffic.items():
        #`pid` is an integer that represents the process ID
        #`traffic` is a list of two values: total Upload and Download size in bytes
        try:
            
            #Get the process object from psutil
            p = psutil.Process(pid)
            
        except psutil.NoSuchProcess:
            #If process is not found, simply continue to the next PID for now
            continue
        
        
        
        #Get the name of the process, eg. chrome.exe etc
        name = p.name()
        
        #Get the time the process was spawned
        try:
            create_time = datetime.fromtimestamp(p.create_time())
            
        except OSError:
            #system processes, using boot time instead
            create_time = datetime.fromtimestamp(psutil.boot_time())
            
        #Construct our dictionary that stores process info
        process = {
            "pid": pid, "name": name, "create_time": create_time, "Upload": traffic[0],
            "Dowmload": traffic[1],
        }
        
        
        try:
            #Calculate the upload and download speeds by siply subtracting the old stats 
            #from the new stats
            process["Upload Speed"] = traffic[0] - global_df.at[pid, "Upload"]
            process["Download Speed"] = traffic[1] - global_df.at[pid, "Download"]
            
        except (KeyError, AttributeError):
            #If it's the first time running this function, then the speed is the current traffic
            #You can think of it as if old traffic is 0
            process["Upload Speed"] = traffic[0]
            process["Download Speed"] = traffic[1]
            
            
        #Append the process to our processes list
        processes.append(process)
        
        

#Construct our Pandas DataFrames
df = pd.DataFrame(processes) 

try:
    #set the PID as the index of the dataframe
    df = df.set_index("pid")
    
    #sort by column
    df.sort_values("Download",inplace=True, ascending=False)
except KeyError as e:
    
    #When dataframe is empty
    pass



#Make another copy of the dataframe just for fancy printing 
printing_df = df.copy()


try:
    #Apply the function get_size to scale the stats like '234.5KB tec
    printing_df["Download"] = printing_df["Download"].apply(get_size)
    printing_df["Upload"] = printing_df["Upload"].apply(get_size)
    printing_df["Download Speed"] = printing_df["Download Speed"].apply(get_size).apply(lambda s: f"{s}/s")
    printing_df["Upload Speed"] = printing_df["Upload Speed"].apply(get_size).apply(lambda s: f"{s}/s")

except KeyError:
    #when dataframe is empty again 
    pass

#Clear the screen based on your OS
os.system("cls") if "nt" in os.name else os.system("clear")

#Print our dataframe 
print(printing_df.to_string())

#update the global df to the dataframe
global_df = df



"""
The above function iterates over the pid2traffic dictionary, and tries to get the 
process object using psutil so it can get the name and creation time of the process 
using the name() and create_time() methods, respectively.

After we create our process dictionary that has most of the information we need about 
the process including the total usage, we use global_df to get the previous total usage 
and then calculate the current upload and download speed using that. After that, we 
append this process to our processes list and convert it as a pandas dataframe to print 
it.

Before we print the dataframe, we can do some modifications such as sorting by 
"Download" usage, and also apply the get_size() utility function to print the 
bytes in a nice scalable format.
"""

#A function that calls the above function every second
def print_stats():
    """
    A simple function that keeps printing the stats
    """
    while is_program_running:
        time.sleep(1)
        print_pid2traffic()
        
        

"""
So now, we have two functions that keeps running in separate threads, 
one is the above print_stats() and the second is the get_connections()
"""

# Let's make the main code:
if __name__ == "__main__":
    #Start the priting thread
    priting_thread = Thread(target=print_stats)
    priting_thread.start()
    
    #Start the get_connection() function to update the curremt connection 
    #of this machine
    connection_thread = Thread(target=get_connections)
    connection_thread.start()
    
    
    #Start sniffing
    print("Started sniffing")
    sniff(prn=process_packet, store=False)
    
    #Setting the global variable to False to exit the program
    is_program_running = False