import psutil

def get_cpu_usage():
    """
    Returns the CPU usage percentage.
    """
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    """
    Returns the memory usage percentage.
    """
    mem_info = psutil.virtual_memory()
    return {
        "total": mem_info.total,
        "used": mem_info.used,
        "percentage": mem_info.percent
    }

def get_disk_usage(path='/'):
    """
    Returns the disk usage for a given path. Defaults to root.
    """
    disk_info = psutil.disk_usage(path)
    return {
        "total": disk_info.total,
        "used": disk_info.used,
        "percentage": disk_info.percent
    }

def get_network_activity():
    """
    Returns the total bytes sent and received since boot.
    """
    net_io = psutil.net_io_counters()
    return {
        "bytes_sent": net_io.bytes_sent,
        "bytes_recv": net_io.bytes_recv
    }

def get_active_processes(limit=5):
    """
    Returns the top `limit` processes based on CPU usage.
    """
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        processes.append(proc.info)
    
    # Sort processes based on CPU usage and get the top 'limit' processes
    top_processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:limit]
    
    return top_processes

# Optionally, you can add more functions to check other parameters or specific services.

if __name__ == "__main__":
    # If running this script directly, print out the metrics:
    print("CPU Usage:", get_cpu_usage())
    print("Memory Usage:", get_memory_usage())
    print("Disk Usage:", get_disk_usage())
    print("Network Activity:", get_network_activity())
    print("Top 5 Processes by CPU Usage:", get_active_processes())
