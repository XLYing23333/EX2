def open_app(app: str) -> str:
    mapping = {
        '记事本': 'notepad.exe',
        'notepad': 'notepad.exe',
        '计算器': 'calc.exe',
        'calculator': 'calc.exe',
        '画图': 'mspaint.exe',
        'paint': 'mspaint.exe',
        '浏览器': 'start msedge',
        'edge': 'start msedge'
    }
    exe = mapping.get(app.strip().lower())
    if not exe:
        return f"不支持打开: {app}"
    import subprocess
    try:
        use_shell = exe.startswith('start')
        subprocess.Popen(exe if not use_shell else exe.split(), shell=use_shell)
        return f"已尝试打开 {app}"
    except Exception as e:
        return f"打开失败: {str(e)}"
