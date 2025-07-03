# tools.py
from typing import Optional

# 生成诗歌
def generate_poem(topic: str, style: Optional[str] = None) -> str:
    """
    生成一首诗歌（如七言诗），topic为主题，style为风格（可选，默认为现代诗）。
    """
    prompt = f"请以“{topic}”为主题，写一首七言诗。"
    if style:
        prompt += f" 风格为：{style}。"
    return prompt  # 交给LLM生成

# 文本润色
def rephrase_text(text: str, style: Optional[str] = None) -> str:
    """
    润色文本，可以指定风格。
    """
    prompt = f"请对以下文本进行润色"
    if style:
        prompt += f"，风格为{style}"
    prompt += f"：{text}"
    return prompt  # 交给LLM生成

# 文档保存
def doc_save(text: str, filename: str = "output.txt") -> str:
    """
    保存文本到指定文件。
    """
    with open(filename, "w", encoding='utf-8') as f:
        f.write(text)
    return f"内容已保存到{filename}"