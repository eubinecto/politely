import os
import requests  # noqa


class Translator:
    def __call__(self, sent: str) -> str:
        url = "https://openapi.naver.com/v1/papago/n2mt"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Naver-Client-Id": os.environ['NAVER_CLIENT_ID'],
            "X-Naver-Client-Secret": os.environ['NAVER_CLIENT_SECRET']
        }
        data = {
            "source": "en",
            "target": "ko",
            "text": sent,
        }
        r = requests.post(url, headers=headers, data=data)
        r.raise_for_status()
        return r.json()['message']['result']['translatedText']
