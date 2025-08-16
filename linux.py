import subprocess
import os
import platform
import re
import time

def run_command(command, shell=True, check=False, **kwargs):
    """
    运行一个 shell 命令并返回其标准输出。
    如果命令失败，则打印错误消息并返回 None。
    """
    try:
        # 使用 subprocess.run 运行命令，捕获输出
        result = subprocess.run(
            command,
            shell=shell,
            check=check,  # 如果 check=True，非零退出码会引发 CalledProcessError
            text=True,    # 将 stdout 和 stderr 解码为文本
            capture_output=True, # 捕获标准输出和标准错误
            encoding='utf-8', # 明确指定编码以避免解码错误
            errors='replace', # 替换无法解码的字符
            **kwargs
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"错误: 命令 '{' '.join(command) if isinstance(command, list) else command}' 执行失败，返回码 {e.returncode}:")
        print(f"标准输出:\n{e.stdout}")
        print(f"标准错误:\n{e.stderr}")
        return None
    except FileNotFoundError:
        print(f"错误: 命令 '{command.split()[0] if isinstance(command, str) else command[0]}' 未找到。请确保它已安装并位于 PATH 中。")
        return None
    except Exception as e:
        print(f"运行命令时发生意外错误 '{command}': {e}")
        return None

def get_system_info():
    """
    获取并打印基本的系统信息。
    """
    print("\n--- 系统信息 ---")
    print("-" * 15)

    os_release_output = run_command("cat /etc/os-release")
    if os_release_output:
        os_info = {}
        for line in os_release_output.splitlines():
            if '=' in line:
                key, value = line.split('=', 1)
                os_info[key.strip()] = value.strip().strip('"')
        print(f"操作系统名称: {os_info.get('PRETTY_NAME', '未知')}")
        print(f"操作系统ID: {os_info.get('ID', '未知')}")
        print(f"版本ID: {os_info.get('VERSION_ID', '未知')}")
        print(f"构建ID: {os_info.get('BUILD_ID', '未知')}")

    hostname_output = run_command("hostname")
    if hostname_output:
        print(f"主机名: {hostname_output}")

    kernel_output = run_command("uname -a")
    if kernel_output:
        print(f"内核信息: {kernel_output}")

    arch_output = run_command("uname -m")
    if arch_output:
        print(f"架构: {arch_output}")

    uptime_output = run_command("uptime")
    if uptime_output:
        # 解析 uptime 输出以获取更详细的信息
        match = re.search(r'up (.*?),.*?load average: (.*)', uptime_output)
        if match:
            uptime_str = match.group(1)
            load_avg = match.group(2)
            print(f"系统运行时间: {uptime_str}")
            print(f"负载平均值 (1, 5, 15 分钟): {load_avg}")
        else:
            print(f"系统运行时间 (原始): {uptime_output}")

def get_cpu_info():
    """
    获取并打印 CPU 信息。
    """
    print("\n--- CPU 信息 ---")
    print("-" * 14)

    cpuinfo_output = run_command("cat /proc/cpuinfo")
    if cpuinfo_output:
        model_name = "未知"
        cpu_cores = 0
        logical_processors = 0
        unique_physical_ids = set()

        for line in cpuinfo_output.splitlines():
            if "model name" in line:
                if model_name == "未知": # 只记录第一个型号名称
                    model_name = line.split(":")[1].strip()
            elif "cpu cores" in line:
                cpu_cores = int(line.split(":")[1].strip())
            elif "processor" in line:
                logical_processors += 1
            elif "physical id" in line:
                unique_physical_ids.add(line.split(":")[1].strip())

        print(f"CPU 型号: {model_name}")
        print(f"物理 CPU 数量: {len(unique_physical_ids)}")
        print(f"每个物理 CPU 的核心数: {cpu_cores}")
        print(f"逻辑处理器总数: {logical_processors}")
    else:
        print("无法获取 CPU 信息。")

def get_memory_info():
    """
    获取并打印内存信息。
    """
    print("\n--- 内存信息 ---")
    print("-" * 14)

    meminfo_output = run_command("cat /proc/meminfo")
    if meminfo_output:
        mem_total = 0
        mem_free = 0
        buffers = 0
        cached = 0
        swap_total = 0
        swap_free = 0

        for line in meminfo_output.splitlines():
            if "MemTotal:" in line:
                mem_total = int(line.split()[1]) # KB
            elif "MemFree:" in line:
                mem_free = int(line.split()[1]) # KB
            elif "Buffers:" in line:
                buffers = int(line.split()[1]) # KB
            elif "Cached:" in line:
                cached = int(line.split()[1]) # KB
            elif "SwapTotal:" in line:
                swap_total = int(line.split()[1]) # KB
            elif "SwapFree:" in line:
                swap_free = int(line.split()[1]) # KB

        mem_used = mem_total - mem_free - buffers - cached # 近似已用内存

        print(f"总内存: {mem_total / 1024**2:.2f} GB")
        print(f"可用内存: {mem_free / 1024**2:.2f} GB")
        print(f"已用内存 (近似): {mem_used / 1024**2:.2f} GB")
        print(f"缓冲区: {buffers / 1024**2:.2f} GB")
        print(f"缓存: {cached / 1024**2:.2f} GB")
        print(f"总交换空间: {swap_total / 1024**2:.2f} GB")
        print(f"可用交换空间: {swap_free / 1024**2:.2f} GB")
    else:
        print("无法获取内存信息。")

def get_disk_info():
    """
    获取并打印磁盘使用情况。
    """
    print("\n--- 磁盘信息 ---")
    print("-" * 14)

    df_output = run_command("df -h")
    if df_output:
        lines = df_output.splitlines()
        if len(lines) > 1:
            print(lines[0]) # 打印标题行
            for line in lines[1:]:
                print(line)
        else:
            print("没有找到磁盘分区信息。")
    else:
        print("无法获取磁盘信息。")

def get_network_info():
    """
    获取并打印网络接口信息和统计数据。
    """
    print("\n--- 网络信息 ---")
    print("-" * 14)

    ip_output = run_command("ip -s a")
    if ip_output:
        interfaces = {}
        current_iface = None
        for line in ip_output.splitlines():
            # 匹配接口行 (e.g., '1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000')
            if re.match(r'^\d+:', line):
                parts = line.split(':', 2)
                iface_id = parts[0].strip()
                iface_name = parts[1].strip()
                current_iface = iface_name
                interfaces[current_iface] = {'addresses': [], 'rx_bytes': 0, 'tx_bytes': 0, 'rx_errors': 0, 'tx_errors': 0}
            elif current_iface and 'inet ' in line:
                # 匹配 IPv4 地址
                addr = line.strip().split(' ')[1]
                interfaces[current_iface]['addresses'].append(f"IPv4: {addr}")
            elif current_iface and 'inet6 ' in line:
                # 匹配 IPv6 地址
                addr = line.strip().split(' ')[1]
                interfaces[current_iface]['addresses'].append(f"IPv6: {addr}")
            elif current_iface and 'RX: bytes' in line:
                # 匹配 RX 字节和错误 (ip -s a output format)
                stats_line = next(ip_output.splitlines()[ip_output.splitlines().index(line)+1:], None)
                if stats_line:
                    stats = stats_line.strip().split()
                    if len(stats) >= 10: # bytes, packets, errors, dropped, overrun, mcast
                        interfaces[current_iface]['rx_bytes'] = int(stats[0])
                        interfaces[current_iface]['rx_errors'] = int(stats[2])
            elif current_iface and 'TX: bytes' in line:
                # 匹配 TX 字节和错误
                stats_line = next(ip_output.splitlines()[ip_output.splitlines().index(line)+1:], None)
                if stats_line:
                    stats = stats_line.strip().split()
                    if len(stats) >= 10:
                        interfaces[current_iface]['tx_bytes'] = int(stats[0])
                        interfaces[current_iface]['tx_errors'] = int(stats[2])

        for iface, data in interfaces.items():
            print(f"\n接口: {iface}")
            if data['addresses']:
                for addr in data['addresses']:
                    print(f"  地址: {addr}")
            else:
                print("  无 IP 地址")
            print(f"  接收字节: {data['rx_bytes']} ({data['rx_bytes'] / 1024**2:.2f} MB)")
            print(f"  发送字节: {data['tx_bytes']} ({data['tx_bytes'] / 1024**2:.2f} MB)")
            print(f"  接收错误: {data['rx_errors']}")
            print(f"  发送错误: {data['tx_errors']}")
    else:
        print("无法获取网络信息。")

def get_process_info():
    """
    获取并打印运行中的进程信息，按 CPU 和内存使用率排序。
    """
    print("\n--- 运行进程 ---")
    print("-" * 14)

    # ps aux --sort=-%cpu,-%mem 可以按 CPU 和内存使用率降序排序
    # -e 选项可以显示所有进程，包括没有控制终端的进程
    # -o 选项可以定制输出列，但为了简单，我们使用 aux 默认输出
    ps_output = run_command("ps aux --sort=-%cpu,-%mem | head -n 20") # 获取前20个进程
    if ps_output:
        print("USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND")
        lines = ps_output.splitlines()
        # 打印除标题行外的所有行
        for line in lines[1:]:
            print(line)
    else:
        print("无法获取进程信息。")

def get_logged_in_users():
    """
    获取并打印当前登录用户。
    """
    print("\n--- 登录用户 ---")
    print("-" * 14)

    who_output = run_command("who")
    if who_output:
        print(who_output)
    else:
        print("无法获取登录用户信息。")

def get_system_logs():
    """
    获取并打印最近的系统日志条目 (dmesg 或 journalctl)。
    """
    print("\n--- 系统日志 (最近15条) ---")
    print("-" * 23)

    # 尝试使用 journalctl (适用于 systemd 系统)
    journal_output = run_command("journalctl -n 15 --no-pager")
    if journal_output:
        print("--- 使用 journalctl ---")
        print(journal_output)
    else:
        # 如果 journalctl 失败，尝试 dmesg
        dmesg_output = run_command("dmesg | tail -n 15")
        if dmesg_output:
            print("--- 使用 dmesg ---")
            print(dmesg_output)
        else:
            print("无法获取系统日志 (journalctl 和 dmesg 都失败了)。")

def main():
    """
    主函数，调用所有信息获取函数。
    """
    print("🚀 正在收集 Linux 系统信息... 🚀")
    get_system_info()
    get_cpu_info()
    get_memory_info()
    get_disk_info()
    get_network_info()
    get_process_info()
    get_logged_in_users()
    get_system_logs()
    print("\n✨ 信息收集完成！✨")

if __name__ == "__main__":
    main()
