from os import uname
import psutil
import platform
from datetime import datetime

from sympy import factor



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