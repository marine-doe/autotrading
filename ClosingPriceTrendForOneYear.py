import requests
import json
import datetime
import yaml
import pandas

with open('config.yaml', encoding='UTF-8') as f:
    _cfg = yaml.load(f, Loader=yaml.FullLoader)
APP_KEY = _cfg['APP_KEY']
APP_SECRET = _cfg['APP_SECRET']
ACCESS_TOKEN = ""
CANO = _cfg['CANO']
ACNT_PRDT_CD = _cfg['ACNT_PRDT_CD']
DISCORD_WEBHOOK_URL = _cfg['DISCORD_WEBHOOK_URL']
URL_BASE = _cfg['URL_BASE']


def get_daily_price(code):
    PATH = "uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type": "application/json",
               "authorization": f"Bearer {ACCESS_TOKEN}",
               "appKey": APP_KEY,
               "appSecret": APP_SECRET,
               "tr_id": "FHKST03010100"}
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=1)
    date_to = yesterday.strftime("%Y%m%d")
    date_from = (yesterday - datetime.timedelta(days=100)).strftime("%Y%m%d")
    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": code,
        "fid_input_date_1": date_from,
        "fid_input_date_2": date_to,
        "fid_org_adj_prc": "0",
        "fid_period_div_code": "D"
    }
    res = requests.get(URL, headers=headers, params=params)
    response_list = res.json()['output2']
    end_price_list = []
    for response in response_list:
        cur_end_price = int(response['stck_clpr'])
        end_price_list.insert(0, cur_end_price)
    date_to = (yesterday - datetime.timedelta(days=101)).strftime("%Y%m%d")
    date_from = (yesterday - datetime.timedelta(days=200)).strftime("%Y%m%d")
    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": code,
        "fid_input_date_1": date_from,
        "fid_input_date_2": date_to,
        "fid_org_adj_prc": "0",
        "fid_period_div_code": "D"
    }
    res = requests.get(URL, headers=headers, params=params)
    response_list = res.json()['output2']
    for response in response_list:
        cur_end_price = int(response['stck_clpr'])
        end_price_list.insert(0, cur_end_price)
    date_to = (yesterday - datetime.timedelta(days=201)).strftime("%Y%m%d")
    date_from = (yesterday - datetime.timedelta(days=300)).strftime("%Y%m%d")
    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": code,
        "fid_input_date_1": date_from,
        "fid_input_date_2": date_to,
        "fid_org_adj_prc": "0",
        "fid_period_div_code": "D"
    }
    res = requests.get(URL, headers=headers, params=params)
    response_list = res.json()['output2']
    for response in response_list:
        cur_end_price = int(response['stck_clpr'])
        end_price_list.insert(0, cur_end_price)
    date_to = (yesterday - datetime.timedelta(days=301)).strftime("%Y%m%d")
    date_from = (yesterday - datetime.timedelta(days=365)).strftime("%Y%m%d")
    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": code,
        "fid_input_date_1": date_from,
        "fid_input_date_2": date_to,
        "fid_org_adj_prc": "0",
        "fid_period_div_code": "D"
    }
    res = requests.get(URL, headers=headers, params=params)
    response_list = res.json()['output2']
    for response in response_list:
        cur_end_price = int(response['stck_clpr'])
        end_price_list.insert(0, cur_end_price)
    return end_price_list


def get_access_token():
    """토큰 발급"""
    headers = {"content-type": "application/json"}
    body = {"grant_type": "client_credentials",
            "appkey": APP_KEY,
            "appsecret": APP_SECRET}
    PATH = "oauth2/tokenP"
    URL = f"{URL_BASE}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    ACCESS_TOKEN = res.json()["access_token"]
    return ACCESS_TOKEN


try:
    # 초기화
    ACCESS_TOKEN = get_access_token()
    symbol_list = {  # 종목 리스트
        "326030": "SK바이오팜",
        "066575": "LG전자우",
        "007660": "이수페타시스",
        "005930": "삼성전자",
        "000270": "기아",
        "005380": "현대차",
        "009830": "한화솔루션",
    }
    raw_data = {}
    for key in symbol_list.keys():
        raw_data[symbol_list[key]] = get_daily_price(key)
    raw_data = pandas.DataFrame(raw_data)  # 데이터 프레임으로 전환
    raw_data.to_excel(excel_writer='sample.xlsx', engine='openpyxl')  # 엑셀로 저장
except Exception as e:
    print(f"[오류 발생]{e}")
