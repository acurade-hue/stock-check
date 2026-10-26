"""Yu Nishimura 판화 재입고 감시.

재고가 생기면 ntfy로 폰에 푸시 알림을 보낸다.
  python check_stock.py         재고 확인
  python check_stock.py --test  재고와 상관없이 테스트 알림 발송
ntfy 채널 이름은 환경변수 NTFY_TOPIC 에서 읽는다.
"""

import json
import os
import random
import sys
import time
import urllib.error
import urllib.request

SHOP = "https://shop.lafayetteanticipations.com"
PRODUCT_URL = f"{SHOP}/en/products/impression-edition-limitee-yu-nishimura"
CHECKOUT_URL = f"{SHOP}/cart/55457966784839:1"  # 상품이 담긴 결제 페이지
USER_AGENT = "Mozilla/5.0 (stock-check)"
BACKOFF_SECONDS = [30, 60, 120, 240]  # 429일 때 재시도 전 대기 시간 (요청은 최대 5번)
MAX_WAIT = 300  # Retry-After 헤더 값의 상한


def fetch_product():
    """429(요청 과다)를 받으면 대기 시간을 늘려가며 재시도한다."""
    time.sleep(random.uniform(0.5, 1.2))
    req = urllib.request.Request(PRODUCT_URL + ".js", headers={"User-Agent": USER_AGENT})
    for attempt, backoff in enumerate(BACKOFF_SECONDS + [None], start=1):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code != 429 or backoff is None:
                raise
            retry_after = e.headers.get("Retry-After", "")
            wait = min(int(retry_after), MAX_WAIT) if retry_after.isdigit() else backoff
            print(f"429 응답 ({attempt}번째 시도) - {wait}초 후 재시도")
            time.sleep(wait)


def is_available():
    product = fetch_product()
    return bool(product.get("available")) or any(v.get("available") for v in product.get("variants", []))


def notify(title, message):
    topic = os.environ.get("NTFY_TOPIC", "").strip()
    if not topic:
        sys.exit("NTFY_TOPIC 환경변수가 없습니다.")
    body = json.dumps({
        "topic": topic,
        "title": title,
        "message": message,
        "priority": 5,
        "tags": ["tada"],
        "click": CHECKOUT_URL,
    }).encode("utf-8")
    req = urllib.request.Request("https://ntfy.sh/", data=body, method="POST",
                                 headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=20).close()


def main():
    if "--test" in sys.argv:
        notify("테스트 알림", "알림이 잘 옵니다. 누르면 결제 페이지가 열립니다.")
        print("테스트 알림을 보냈습니다.")
        return

    if is_available():
        notify("재입고! Yu Nishimura 판화", "지금 구매 가능합니다. 누르면 결제 페이지로 이동합니다.")
        print("재입고 확인 - 알림을 보냈습니다.")
    else:
        print("아직 SOLD OUT 입니다.")


if __name__ == "__main__":
    main()
