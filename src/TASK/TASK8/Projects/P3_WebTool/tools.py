import requests

def scrape_website(url: str) -> str:
    """
    抓取指定URL的网页内容（text）。
    只返回纯文本内容。
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        html = resp.text

        # 简单去除script/style标签
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        # 删除所有<script>和<style>等无关内容
        for tag in soup(['script', 'style', 'noscript']):
            tag.decompose()
        text = soup.get_text(separator='\n')
        # 去除多余空白
        lines = [line.strip() for line in text.splitlines()]
        text = '\n'.join([line for line in lines if line])
        return text[:4000]  # 只返回前4K字，防止溢出
    except Exception as e:
        return f"网页抓取失败: {str(e)}"