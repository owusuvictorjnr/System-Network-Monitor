from os import uname
from pendulum import time
import psutil
import platform
from datetime import datetime
import GPUtil
from tabulate import tabulate
import time 
from sympy import factor



# me = f"Vitech Solutions"

# print(me, "\n\n\n")
# time.sleep(5)


# a function that converts a large number of bytes into a scaled format 
# (e.g in kilo, mega, Giga, etc.)
def get__size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g: 1253656 => '1.20MB'
    """
    factor = 1024
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes: .2f}{unit}B"
        bytes /= factor
        
        
        
#System Information
#We'll use `platform` module here

print("="*40, "System Information", "="*40)

uname = platform.uname()

print(f"System: {uname.system}")

print(f"Node Name: {uname.node}")

print(f"Release: {uname.release}")

print(f"Version: {uname.version}")

print(f"Machine: {uname.machine}")  
      
print(f"Processor: {uname.processor}")


#Getting the date and time the computer was booted
print("="*40, "Boot Time", "="*40)

boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
print(f"Boot Time: {bt.year}/{bt.month}/{bt.day}  {bt.hour}:{bt.minute}:{bt.second}")



#CPU Information

#Let's get some CPU information, such as the total number 
# of cores, usage, etc

print("="*40, "CPU Information", "="*40)

#Number of cores
print("Physical cores:", psutil.cpu_count(logical=False))
print("Total cores", psutil.cpu_count(logical=True))

#CPU Frequencies
cpufreq = psutil.cpu_freq()
print(f"Max Frequency: {cpufreq.max: .2f}Mhz")
print(f"Min Frequency: {cpufreq.min: .2f}Mhz")
print(f"Current Frequency: {cpufreq.current: .2f}Mhz")

#CPU Usage
print("CPU Usage Per Core")

for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"Core {i}: {percentage}%")
print(f"Total CPU Usage: {psutil.cpu_percent()}%")




#Memory Usage
#Memory Information
print("="*40, "Memory Information", "="*40)


#Get the memory details
svmem = psutil.virtual_memory()

print(f"Total: {get__size(svmem.total)}")
print(f"Available: {get__size(svmem.available)}")
print(f"Used: {get__size(svmem.used)}")
print(f"Percentage: {get__size(svmem.percent)}")

print("="*20, "SWAP", "="*20)

#get the swap memory details(if exists)
swap = psutil.swap_memory()

print(f"Total: {get__size(swap.total)}")
print(f"Free: {get__size(swap.free)}")
print(f"Used: {get__size(swap.used)}")
print(f"Percentage: {get__size(swap.percent)}")




# Disk Usage
print("="*40, "Disk Information", "="*40)

print("Partitions and Usage:")

#Get all disk partitions 
partitions = psutil.disk_partitions()
for partition in partitions:
    print(f"=== Devices: {partition.device} ===")
    print(f"    Mountpoint: {partition.mountpoint}")
    print(f"    File system type: {partition.fstype }")
    
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
        
    except PermissionError:
        #This can be catched due to the disk that is not ready
        continue
    
    print(f"    Total Size: {get__size(partition_usage.total)}")
    print(f"    Used: {get__size(partition_usage.used)}")
    print(f"    Free: {get__size(partition_usage.free)}")
    print(f"    Percentage: {get__size(partition_usage.percent)}")
    
    
    
#Get IO stats since boot
disk_io = psutil.disk_io_counters()
print(f"Total read: {get__size(disk_io.read_bytes)}")
print(f"Total write: {get__size(disk_io.write_bytes)}\n")



# Network Information

print("="*40, "Network Information", "="*40)

#Get all network interfaces (virtual and Physical)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f"=== Interface: {interface_name}===")
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f"    IP Address: {address.address}")
            print(f"    Netmask: {address.netmask}")
            print(f"    Broadcast IP: {address.broadcast}")
            
        elif str (address.family) == 'AddressFamily.AF_PACKET':
            print(f"    MAC Address: {address.address}")
            print(f"    Netmask: {address.netmask}")
            print(f"    Broadcast MAC: {address.broadcast}")
            
            
                        
#Get IO stats since boot
net_io = psutil.net_io_counters()
print(f"Total Byte Sent: {get__size(net_io.bytes_sent)}")
print(f"Total Byte Received: {get__size(net_io.bytes_recv)}")




# GPU Information
print("="*40, "GPU Details", "="*40)


gpus = GPUtil.getGPUs()
list_gpus = []

for gpu in gpus:
    #Get the GPU id 
    gpu_id = gpu.id
    
    #Name of GPU 
    gpu_name = gpu.name
    
    #Get % percentage of GPU usage of that GPU
    gpu_load = f"{gpu.load*100}%"
    
    #Get free memory in MB format
    gpu_free_memory = f"{gpu.memoryFree}MB"
    
    #get used memory
    gpu_used_memory = f"{gpu.memoryUsed}MB"
    
    # get total memory
    gpu_total_memory = f"{gpu.memoryTotal}MB"
    
    # get GPU temperature in Celsius
    gpu_temperature = f"{gpu.temperature} °C"
    gpu_uuid = gpu.uuid
    list_gpus.append((
        gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
        gpu_total_memory, gpu_temperature, gpu_uuid
    ))
    
    
print(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory",
                                   "temperature", "uuid")), "\n\n\n")





print(f"credit to Abdou Rockikz ")