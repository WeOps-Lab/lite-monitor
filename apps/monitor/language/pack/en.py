MONITOR_OBJECT_TYPE = {
    "Device": "Device",
}

MONITOR_OBJECT = {
    "Switch": "Switch",
}

MONITOR_OBJECT_PLUGIN = {
    "Switch": {

    }
}

MONITOR_OBJECT_METRIC_GROUP = {
    "Switch": {

    }
}

MONITOR_OBJECT_METRIC = {
    "Switch": {
        "sysUpTime": {
            "name": "System Uptime",
            "desc": "This metric indicates the uptime of the device since the last restart, measured in days. By monitoring the uptime, network administrators can understand the stability and reliability of the device and identify potential reboot or failure issues."
        },
        "ifAdminStatus": {
            "name": "Interface Admin Status",
            "desc": "This metric indicates the administrative status of the network switch interface. It serves to indicate whether the interface is enabled (up) or disabled (down) by an administrator, along with other states such as testing or not present. This information is vital for network management and troubleshooting."
        },
        "ifOperStatus": {
            "name": "Interface Oper Status",
            "desc": "This metric reflects the actual operational status of the network switch interface, indicating whether the interface is operational. Unlike the administrative status, the operational status shows whether the interface can successfully receive and send traffic, which is crucial for monitoring network health."
        },
        "ifHighSpeed": {
            "name": "Interface Bandwidth",
            "desc": "This metric indicates the maximum data transmission speed supported by the network interface, usually measured in KB per second. Understanding the maximum speed of the interface helps administrators optimize traffic and utilize network resources effectively."
        },
        "ifInErrors": {
            "name": "Incoming Errors Rate (per second)",
            "desc": "This metric calculates the average rate of incoming error packets over the past 5 minutes, measured in packets per second. Monitoring incoming errors allows administrators to detect potential issues, such as physical connection faults or configuration errors, in a timely manner."
        },
        "ifOutErrors": {
            "name": "Outgoing Errors Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing error packets over the past 5 minutes, measured in packets per second. Monitoring outgoing errors is essential for identifying transmission issues and ensuring data integrity."
        },
        "ifInDiscards": {
            "name": "Incoming Discards Rate (per second)",
            "desc": "This metric represents the average rate of incoming discarded packets over the past 5 minutes, measured in packets per second. Packet discards may indicate network congestion or resource shortages, and monitoring this metric can help administrators optimize network performance."
        },
        "ifOutDiscards": {
            "name": "Outgoing Discards Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing discarded packets over the past 5 minutes, measured in packets per second. Monitoring outgoing discards can help identify network transmission issues and misconfigurations."
        },
        "ifInUcastPkts": {
            "name": "Incoming Unicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming unicast packets over the past 5 minutes, measured in packets per second. Monitoring unicast packets is crucial for assessing interface utilization and traffic load."
        },
        "ifOutUcastPkts": {
            "name": "Outgoing Unicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing unicast packets over the past 5 minutes, measured in packets per second. By monitoring the number of unicast packets, administrators can assess the transmission performance of the interface and the usage of traffic."
        },
        "ifInBroadcastPkts": {
            "name": "Incoming Broadcast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming broadcast packets over the past 5 minutes, measured in packets per second. Monitoring broadcast traffic can help administrators identify potential bottlenecks and efficiency issues in the network."
        },
        "ifOutBroadcastPkts": {
            "name": "Outgoing Broadcast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing broadcast packets over the past 5 minutes, measured in packets per second. Understanding broadcast traffic is important for controlling network traffic and preventing network congestion."
        },
        "ifInMulticastPkts": {
            "name": "Incoming Multicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming multicast packets over the past 5 minutes, measured in packets per second. Monitoring multicast packets is crucial for performance assessment of specific applications, such as multimedia streaming."
        },
        "ifOutMulticastPkts": {
            "name": "Outgoing Multicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing multicast packets over the past 5 minutes, measured in packets per second. Understanding multicast traffic helps administrators optimize bandwidth usage and improve network efficiency."
        },
        "ifInOctets": {
            "name": "Interface Incoming Traffic Rate (per second)",
            "desc": "This metric indicates the average rate of bytes received over the past 5 minutes, converted to megabytes (MB). Monitoring byte traffic helps evaluate the load on the interface and bandwidth usage."
        },
        "ifOutOctets": {
            "name": "Interface Outgoing Traffic Rate (per second)",
            "desc": "This metric calculates the average rate of bytes sent over the past 5 minutes, measured in megabytes (MB). Monitoring outgoing traffic is crucial for ensuring data transmission quality and optimizing network performance."
        },
        "iftotalInOctets": {
            "name": "Device Total Incoming Traffic (per second)",
            "desc": "This metric indicates the average rate of total bytes received by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the incoming byte counts from multiple interfaces, this metric helps administrators obtain an overview of the device's incoming traffic, supporting overall traffic monitoring and capacity planning."
        },
        "iftotalOutOctets": {
            "name": "Device Total Outgoing Traffic (per second)",
            "desc": "This metric represents the average rate of total bytes sent by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the outgoing byte counts from multiple interfaces, this metric allows administrators to comprehensively assess the sending performance of the entire system, enabling more effective traffic management and optimization."
        }
    }
}

LANGUAGE_DICT = {
    "MONITOR_OBJECT_TYPE": MONITOR_OBJECT_TYPE,
    "MONITOR_OBJECT": MONITOR_OBJECT,
    "MONITOR_OBJECT_PLUGIN": MONITOR_OBJECT_PLUGIN,
    "MONITOR_OBJECT_METRIC_GROUP": MONITOR_OBJECT_METRIC_GROUP,
    "MONITOR_OBJECT_METRIC": MONITOR_OBJECT_METRIC,
}
