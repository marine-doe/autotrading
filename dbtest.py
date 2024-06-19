from pymongo import MongoClient
import yaml

with open('config.yaml', encoding='UTF-8') as f:
    _cfg = yaml.load(f, Loader=yaml.FullLoader)
MONGODB_URI = _cfg['MONGODB_URI']

try:
    client = MongoClient(MONGODB_URI)
    collection = client['assets']['stock']
    documents = collection.find()

    symbol_list = {  # 매수 희망 종목 리스트
        "005930": "삼성전자",
        "000660": "SK하이닉스",
        "005380": "현대차",
    }

    for sym in symbol_list.keys():
        new_document = {
            "code": sym,
            "name": symbol_list[sym],
            "value": 0
        }
        existing_document = collection.find_one({"code": new_document["code"]})

        if not existing_document:
            collection.insert_one(new_document)

    cash = collection.find_one({"code": "-1"})["value"]
    stock_value = 0
    for doc in documents:
        if not doc["code"] == "-1":
            stock_value += doc["value"]

    print(cash)
    print(stock_value)
except Exception as e:
    print(e)
