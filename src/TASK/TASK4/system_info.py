import psutil
import platform

def get_system_info(info_type: str = "all") -> str:
    """
    改写支持根据参数返回对应系统信息：

    info_type: cpu, memory, disk, network, all
    返回相应信息字符串
    """
    try:
        if info_type == "cpu":
            cpu_count_logical = psutil.cpu_count(logical=True)
            cpu_count_physical = psutil.cpu_count(logical=False)
            cpu_freq = psutil.cpu_freq()
            cpu_usage = psutil.cpu_percent(interval=1)
            return (
                f"CPU 物理核数: {cpu_count_physical}\n"
                f"CPU 逻辑核数: {cpu_count_logical}\n"
                f"当前CPU频率: {cpu_freq.current:.2f} MHz\n"
                f"CPU使用率: {cpu_usage}%"
            )
        elif info_type == "memory":
            mem = psutil.virtual_memory()
            return (
                f"内存总量: {mem.total / 1024 ** 3:.2f} GB\n"
                f"可用内存: {mem.available / 1024 ** 3:.2f} GB\n"
                f"已用内存: {mem.used / 1024 ** 3:.2f} GB\n"
                f"内存使用率: {mem.percent}%"
            )
        elif info_type == "disk":
            disk = psutil.disk_usage("C:\\")
            return (
                f"磁盘总容量: {disk.total / 1024 ** 3:.2f} GB\n"
                f"磁盘已用: {disk.used / 1024 ** 3:.2f} GB\n"
                f"磁盘可用: {disk.free / 1024 ** 3:.2f} GB\n"
                f"磁盘使用率: {disk.percent}%"
            )
        elif info_type == "network":
            net = psutil.net_io_counters()
            return (
                f"网络发送: {net.bytes_sent / 1024 ** 2:.2f} MB\n"
                f"网络接收: {net.bytes_recv / 1024 ** 2:.2f} MB"
            )
        else:  # all 或未知
            return get_system_info("cpu") + "\n\n" + \
                   get_system_info("memory") + "\n\n" + \
                   get_system_info("disk") + "\n\n" + \
                   get_system_info("network")

    except Exception as e:
        return f"获取系统信息失败: {e}"

