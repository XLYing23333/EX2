from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=10, description="用户名")  # ...必填字段(required=True)，长度限制
    age: Optional[int] = Field(None, ge=0, description="年龄")  # 可选字段，必须 ≥0
    hobbies: list[str] = Field([], description="爱好")  # 默认空列表
    
# 合法数据
user = User(id=1, name="Alice", age=25)
print(user)  # id=1 name='Alice' age=25 hobbies=[]

# 非法数据（触发验证错误）
try:
    User(id="not_an_int", name="A", age=-1)
except Exception as e:
    print(e)  # 输出详细错误信息
    
# 转字典
user_dict = user.model_dump()  # {'id': 1, 'name': 'Alice', 'age': 25, 'hobbies': []}
# 转JSON
user_json = user.model_dump_json(indent=2)  
print(user_json)