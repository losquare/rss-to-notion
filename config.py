from notion.client import NotionClient

class global_var:

    # 请手动通过浏览器记录的 cookies 获取 token并填入
    client = NotionClient(token_v2="Your token_v2")
    # 请手动设置表格的 Url 
    tableUrl ="Your table Url"
    

# Gui预留接口 用于修改设置
def set_client(client):
    global_var.client = client
def get_client():
    return global_var.client
