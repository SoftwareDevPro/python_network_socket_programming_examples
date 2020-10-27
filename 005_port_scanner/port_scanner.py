
import sys, socket, threading
from queue import Queue
from enum import Enum

class ScanType(Enum):
    """The type of port scan to perform"""
    SCAN_WELL_KNOWN       = 1
    """ Well Known Ports Scan Mode """
    SCAN_NON_PRIVATE      = 2
    """ Non-Private Ports Scan Mode """
    SCAN_SECURE_APP_PORTS = 3
    """ Secure Application Ports Scan Mode """
    SCAN_CUSTOM           = 4
    """ User-defined Ports Scan Mode """

WELL_KNOWN_PORTS = range(1, 1024)
""" Well Known IANA Ports (1-1024) """
ALL_NONPRIVATE_PORTS = range(1, 49152)
""" Well Known + User/Registered IANA Ports (1-49152) """
SECURE_APP_PORTS =[20, 21, 22, 23, 25, 53, 80, 110, 443]
""" Secure Application Ports (e.g. 22=ssh) """

target = "localhost"
""" the target to scan """
queue = Queue()
""" FIFO of port(s) to scan """
open_ports = []
""" Holds the list of open ports """

def portscan(port):
    """Scans the given port, determining if it can be connected to."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False

def get_ports(mode):
    """Returns the ports to scan per the given scan mode."""
    if mode == ScanType.SCAN_WELL_KNOWN:
        for port in WELL_KNOWN_PORTS:
            queue.put(port)
    elif mode == ScanType.SCAN_NON_PRIVATE:
        for port in ALL_NONPRIVATE_PORTS:
            queue.put(port)
    elif mode == ScanType.SCAN_SECURE_APP_PORTS:
        ports = SECURE_APP_PORTS
        for port in ports:
            queue.put(port)
    elif mode == ScanType.SCAN_CUSTOM:
        ports = input("Enter ports to scan (separate by spaces):")
        ports = ports.split()
        ports = list(map(int, ports))
        for port in ports:
            queue.put(port)

def worker():
    """ Works through the queue, invoking the port scan. """
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print(f"Port {port} is open!")
            open_ports.append(port)
        else:
            print(f"Port {port} is closed!")

def run_scanner(threads, mode):
    """ Performs the port scan with the number of threads for the scan mode. """

    get_ports(mode)

    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print(f"Open ports are: {open_ports}")

if __name__ == '__main__':
    run_scanner(500, ScanType(int(sys.argv[1])))
