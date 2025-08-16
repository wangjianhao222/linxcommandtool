Linux System Information Tool
Overview
The Linux System Information Tool (linux.py) is a comprehensive Python script designed to collect and display detailed system information for Linux-based operating systems. Leveraging Python's subprocess module and standard libraries, the tool executes various Linux commands to gather data on system configuration, hardware resources, network status, running processes, logged-in users, and system logs. It is an essential utility for system administrators, developers, and enthusiasts who need a consolidated view of system metrics without manually running multiple commands.
This script is platform-specific to Linux environments and provides a structured, human-readable output suitable for diagnostics, monitoring, or documentation purposes. It includes robust error handling, supports UTF-8 encoding for compatibility, and processes command outputs to extract meaningful insights.
Features
Core Functionality

System Information:
Retrieves OS details (name, ID, version, build) from /etc/os-release.
Displays hostname, kernel version, system architecture, uptime, and load averages.


CPU Information:
Extracts CPU model, physical CPU count, core count per CPU, and total logical processors from /proc/cpuinfo.


Memory Information:
Reports total, free, used, buffered, and cached memory, as well as swap space details, from /proc/meminfo.
Converts memory values from KB to GB for readability.


Disk Information:
Displays disk usage statistics using df -h, including filesystem details and mount points.


Network Information:
Collects network interface data, including IPv4/IPv6 addresses, received/transmitted bytes, and error counts using ip -s a.
Converts byte counts to MB for clarity.


Process Information:
Lists the top 20 processes sorted by CPU and memory usage using ps aux --sort=-%cpu,-%mem.
Displays detailed process attributes like user, PID, CPU/memory usage, and command.


Logged-in Users:
Shows currently logged-in users with session details using the who command.


System Logs:
Retrieves the latest 15 log entries, preferring journalctl for systemd-based systems, with a fallback to dmesg if journalctl is unavailable.



Technical Highlights

Command Execution:
Utilizes a reusable run_command function to execute shell commands with comprehensive error handling.
Supports both string and list-based commands, with options for shell execution and output capture.


Error Handling:
Captures and displays detailed error messages for failed commands, including return codes, stdout, and stderr.
Handles FileNotFoundError for missing commands and general exceptions for unexpected errors.


Output Parsing:
Employs regular expressions (re module) to parse complex outputs, such as uptime and network statistics.
Processes multi-line command outputs to extract specific fields (e.g., CPU model, memory values).


Platform Compatibility:
Designed for Linux systems, leveraging standard commands like cat, uname, df, ip, ps, who, journalctl, and dmesg.
Uses UTF-8 encoding with error replacement to handle non-standard characters.



Requirements

Python Version: Python 3.6 or higher (uses subprocess.run with text and capture_output options).
Operating System: Linux-based system (e.g., Ubuntu, CentOS, Debian, etc.).
Dependencies: Standard Python libraries (subprocess, os, platform, re, time).
System Commands: Requires common Linux utilities (cat, uname, df, ip, ps, who, journalctl, dmesg) to be available in the system PATH.
Permissions: Some commands (e.g., dmesg) may require elevated privileges for full access.

Installation
Prerequisites

Ensure Python 3.x is installed:python3 --version

If not installed, download and install from python.org or use your package manager:sudo apt install python3  # Debian/Ubuntu
sudo yum install python3  # CentOS/RHEL


Verify that required Linux commands are available:which cat uname df ip ps who journalctl dmesg

Install missing tools using your package manager (e.g., apt, yum, dnf).

Setup

Obtain the Script:
Download or clone the linux.py script to your local system.

wget <script_url>/linux.py

or
git clone <repository_url>


Set Permissions (if needed):chmod +x linux.py


Run the Script:python3 linux.py



Usage
Running the Tool
Execute the script to collect and display system information:
python3 linux.py

The output is printed to the console, organized into sections with clear headers and formatted data.
Example Output
🚀 正在收集 Linux 系统信息... 🚀

--- 系统信息 ---
---------------
操作系统名称: Ubuntu 22.04.3 LTS
操作系统ID: ubuntu
版本ID: 22.04
构建ID: unknown
主机名: my-server
内核信息: Linux my-server 5.15.0-73-generic #80-Ubuntu SMP Mon May 15 15:18:26 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
架构: x86_64
系统运行时间: 2 days, 3:45
负载平均值 (1, 5, 15 分钟): 0.15, 0.22, 0.19

--- CPU 信息 ---
--------------
CPU 型号: Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz
物理 CPU 数量: 1
每个物理 CPU 的核心数: 8
逻辑处理器总数: 8

--- 内存信息 ---
--------------
总内存: 31.29 GB
可用内存: 12.45 GB
已用内存 (近似): 10.34 GB
缓冲区: 0.67 GB
缓存: 7.83 GB
总交换空间: 2.00 GB
可用交换空间: 1.95 GB

--- 磁盘信息 ---
--------------
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       237G   85G  141G  38% /
tmpfs           3.2G     0  3.2G   0% /dev/shm

--- 网络信息 ---
--------------
接口: eth0
  地址: IPv4: 192.168.1.100/24
  接收字节: 123456789 (117.73 MB)
  发送字节: 987654321 (941.90 MB)
  接收错误: 0
  发送错误: 0

--- 运行进程 ---
--------------
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
user      1234  5.2  3.1 123456 78901 ?        S    08:00   0:15 /usr/bin/python3
...

--- 登录用户 ---
--------------
user   tty1    2023-08-14 08:00
admin  pts/0   2023-08-14 09:15 (192.168.1.10)

--- 系统日志 (最近15条) ---
------------------------
--- 使用 journalctl ---
Aug 14 09:15:01 my-server systemd[1]: Starting User Manager...
...

✨ 信息收集完成！✨

Command Details

System Information: Parses /etc/os-release for OS metadata and uses uname, hostname, and uptime for additional details.
CPU Information: Extracts fields from /proc/cpuinfo to provide a detailed CPU profile.
Memory Information: Calculates used memory by subtracting free, buffered, and cached memory from the total.
Disk Information: Uses df -h for human-readable disk usage output.
Network Information: Parses ip -s a output to extract interface details and traffic statistics.
Process Information: Limits to top 20 processes to avoid overwhelming output.
Logged-in Users: Directly displays who output for simplicity.
System Logs: Prioritizes journalctl for modern systems, falling back to dmesg for compatibility.

Advanced Usage
Customizing Output

Modify the main function to selectively call information-gathering functions (e.g., only get_cpu_info() and get_memory_info()).
Adjust the number of processes displayed by changing the head -n 20 parameter in get_process_info().
Customize log retrieval by modifying the journalctl -n 15 or dmesg | tail -n 15 commands in get_system_logs().

Error Handling

If a command fails, the script prints detailed error information, including the command, return code, stdout, and stderr.
For missing commands (e.g., journalctl not found), the script gracefully skips to alternative methods or reports the issue.

Integration

Scripting: Integrate into larger monitoring scripts by importing specific functions (e.g., get_cpu_info()).
Automation: Schedule the script with cron for periodic system reports:crontab -e
0 * * * * python3 /path/to/linux.py >> /path/to/system_report.log


Output Redirection: Save output to a file for logging:python3 linux.py > system_info.txt



Troubleshooting
Common Issues

Command Not Found:
Verify that required commands are installed (apt install iproute2 procps for ip and ps).
Ensure commands are in the system PATH.


Permission Denied:
Run the script with sudo if accessing restricted files (e.g., /proc/cpuinfo, dmesg):sudo python3 linux.py




Empty or Incomplete Output:
Check if the system supports the queried commands (e.g., journalctl requires systemd).
Ensure the system is fully booted and services are running.


Encoding Errors:
The script uses UTF-8 with errors='replace' to handle non-standard characters, but rare encoding issues may require manual inspection of command outputs.



Debugging

Enable check=True in run_command for specific commands to raise exceptions on failure for detailed debugging.
Add print statements within parsing loops to inspect raw command outputs.
Test individual functions (e.g., get_network_info()) to isolate issues.

Future Enhancements

GUI Integration: Add a Tkinter or Flask-based interface for interactive use (similar to the ADB Toolbox).
JSON Output: Support structured JSON output for integration with monitoring tools.
Real-Time Monitoring: Implement continuous updates for metrics like CPU load or network traffic.
Cross-Distribution Compatibility: Enhance parsing for non-standard /etc/os-release formats or alternative commands.
Extended Hardware Info: Include GPU, temperature, or fan speed data using tools like lscpu or sensors.
Custom Filters: Allow users to filter processes by user, PID, or resource usage.

Contributing
Contributions are welcome to enhance functionality or fix bugs:

Fork the repository.
Create a feature branch:git checkout -b feature/new-feature


Commit changes:git commit -m "Add new feature"


Push to the branch:git push origin feature/new-feature


Open a pull request with a detailed description of changes.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

Built with Python standard libraries (subprocess, os, platform, re, time).
Inspired by the need for a unified system information tool for Linux administrators.
Leverages Linux utilities provided by distributions like Ubuntu, CentOS, and Debian.
