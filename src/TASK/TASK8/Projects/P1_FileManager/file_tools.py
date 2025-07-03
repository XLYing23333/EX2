import os

# 编程语言关键字&扩展名映射表
LANG_SIGNS = [
    # (关键词集合, 语言名, 扩展名)
    ({"def", "import", "print", "None"}, "Python", ".py"),
    ({"#include", "int main", "printf"}, "C", ".c"),
    ({"public static void main", "System.out.println"}, "Java", ".java"),
    ({"console.log", "function", "let"}, "JavaScript", ".js"),
    ({"<html>", "<body>", "<head>"}, "HTML", ".html"),
    ({"#!/bin/bash", "echo"}, "Bash", ".sh"),
    ({"SELECT", "FROM", "WHERE"}, "SQL", ".sql"),
    ({"fn", "let", "mut"}, "Rust", ".rs"),
    ({"package main", "func main"}, "Go", ".go"),
    ({"using System", "namespace"}, "C#", ".cs"),
    ({"class", "public", "void"}, "Java/C++", ".java"), # 简化处理
    # ...可以继续扩展
]

def guess_language_and_ext(filepath):
    """根据文件内容猜测代码语言、返回扩展名"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(2048)  # 读前2K字符
    except Exception as e:
        return None, None
    for signs, lang, ext in LANG_SIGNS:
        if any(sign in content for sign in signs):
            return lang, ext
    return None, None

def code_name_format_tool(dir_path: str) -> str:
    """
    遍历dir_path下所有无扩展名文件，根据内容自动补齐扩展名
    """
    results = []
    try: dir_path = dir_path.replace('\n', ' ')
    except: pass
    try: dir_path = dir_path.replace('"', '')
    except: pass
    try: dir_path = dir_path.replace("'", '')
    except: pass
    dir_path = dir_path.split(' ')[0]
    dir_path = os.path.join(os.path.dirname(__file__), dir_path)
    print(f"[{os.listdir(dir_path)}]")
    for fname in os.listdir(dir_path):
        fpath = os.path.join(dir_path, fname)
        if os.path.isfile(fpath) and '.' not in fname:
            lang, ext = guess_language_and_ext(fpath)
            if lang and ext:
                new_fpath = fpath + ext
                os.rename(fpath, new_fpath)
                results.append(f"{fname} → {fname+ext} ({lang})")
            else:
                results.append(f"{fname} (无法识别语言，未修改)")
    if not results:
        return "没有发现需要处理的文件。"
    return "\n".join(results)
