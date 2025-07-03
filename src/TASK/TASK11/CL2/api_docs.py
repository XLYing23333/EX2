import json

ordering_api_docs = {
    "base_url": "http://127.0.0.1:1143/",
    "endpoints": {
        "/menu": {
            "method": "GET",
            "description": "获取当前餐厅菜单（包含菜品列表与定制选项）。",
            "parameters": None,
            "response": {
                "description": "返回包含所有可点菜品、配料及其库存数量的JSON对象。",
                "content_type": "application/json"
            }
        },
        "/special-offers": {
            "method": "GET",
            "description": "获取当前餐厅的促销与优惠活动。",
            "parameters": None,
            "response": {
                "description": "返回当前所有优惠和折扣信息的JSON对象。",
                "content_type": "application/json"
            }
        },
        "/customer-reviews": {
            "method": "GET",
            "description": "获取餐厅顾客的评价。",
            "parameters": None,
            "response": {
                "description": "返回包含顾客评价、评分和评论的JSON对象。",
                "content_type": "application/json"
            }
        },
        "/customizations": {
            "method": "GET",
            "description": "获取餐厅支持的餐品定制选项。",
            "parameters": None,
            "response": {
                "description": "返回所有可选定制（如加料、少盐、无糖等）的JSON对象。",
                "content_type": "application/json"
            }
        }
    }
}

ordering_api_docs = json.dumps(ordering_api_docs, indent=2)
