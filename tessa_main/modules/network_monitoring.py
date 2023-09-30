import os
from scapy.all import sniff, ARP

def get_connected_devices(ip_range='192.168.1.0/24'):
    """
    Detect devices in the local network using ARP ping.
    """
    devices = []
    ans, _ = ARP().ping(ip_range)
    
    for _, rcv in ans:
        devices.append({
            'ip': rcv.psrc,
            'mac': rcv.hwsrc
        })
    
    return devices

def monitor_traffic(interface='eth0', packet_count=10):
    """
    Monitor network traffic on a given interface.
    """
    packets = sniff(iface=interface, count=packet_count)
    
    traffic = []
    for packet in packets:
        packet_info = {
            "source": packet.sprintf('%IP.src%'),
            "destination": packet.sprintf('%IP.dst%')
        }
        traffic.append(packet_info)

    return traffic

if __name__ == "__main__":
    # Print connected devices and monitored traffic.
    print("Connected Devices:", get_connected_devices())
    print("Monitored Traffic:", monitor_traffic(packet_count=5))