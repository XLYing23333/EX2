# tools/run_cmd.py
import subprocess

def run_cmd(cmd: str) -> str:
    try:
        completed = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        out = completed.stdout or ''
        err = completed.stderr or ''
        result = (out + '\n' + err).replace('\r\n', '\n').strip()
        return result if result else "命令执行成功，无输出。"
    except Exception as e:
        return f"命令执行失败: {str(e)}"
