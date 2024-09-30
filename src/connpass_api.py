import requests

def fetch_events(hostname : str):
    """
    Connpass APIを使用して指定されたホスト名からイベントを取得します。

    この関数は指定されたホスト名を使用してURLを構築し、GETリクエストを送信してイベントデータを取得します。
    403エラーを回避するためにUser-Agentヘッダーを設定します。

    引数:
        hostname (str): Connpass APIのホスト名。

    戻り値:
        list: リクエストが成功した場合（ステータスコード200）、イベントのリストを返します。
                参考(イベントサーチAPI) : https://connpass.com/about/api/
        None: リクエストが失敗した場合。

    例外:
        requests.exceptions.RequestException: HTTPリクエストに問題がある場合に発生します。
    """
    url = f"{hostname}/api/v1/event/"
    params = {"count": 5, "order": 3}
    # User-Agentがpython/requestsになっていると403エラーが発生するため、curlに変更
    headers = {"User-Agent": "curl/7.81.0"}
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        events = response.json()
        return events
    else:
        print(response)
        return None