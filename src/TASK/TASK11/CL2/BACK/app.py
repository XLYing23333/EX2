from flask import Flask, jsonify
from data_store import menu, special_offers, customer_reviews, customizations

app = Flask(__name__)

@app.route('/menu', methods=['GET'])
def get_menu():
    """
    获取菜单数据

    返回：
        包含菜单（菜品、配料）数据的JSON，以及HTTP状态码。
    """
    return jsonify(menu), 200

@app.route('/special-offers', methods=['GET'])
def get_special_offers():
    """
    获取优惠活动数据

    返回：
        包含当前所有优惠活动信息的JSON，以及HTTP状态码。
    """
    return jsonify(special_offers), 200

@app.route('/customer-reviews', methods=['GET'])
def get_customer_reviews():
    """
    获取顾客评价数据

    返回：
        包含所有顾客评价、评分和评论的JSON，以及HTTP状态码。
    """
    return jsonify(customer_reviews), 200

@app.route('/customizations', methods=['GET'])
def get_customizations():
    """
    获取餐品定制选项数据

    返回：
        包含所有定制选项（如少盐、不加辣等）的JSON，以及HTTP状态码。
    """
    return jsonify(customizations), 200

if __name__ == '__main__':
    # 启动Flask服务，监听1143端口，debug模式方便开发调试
    app.run(debug=True, port=1143)