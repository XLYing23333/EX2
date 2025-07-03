# tools/calculator.py
def calculator(expression: str) -> str:

    import ast
    import operator as op
    _getop = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Pow: op.pow,
        ast.USub: op.neg
    }
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            f = _getop.get(type(node.op))
            if f is None: raise TypeError("不支持的操作符")
            return f(_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            f = _getop.get(type(node.op))
            if f is None: raise TypeError("不支持的操作符")
            return f(_eval(node.operand))
        else:
            raise TypeError("表达式有误")
    try:
        node = ast.parse(expression, mode="eval").body
        return str(_eval(node))
    except Exception as e:
        return f"表达式错误: {str(e)}"
