"""
P2P(push) subscriber

Usage:
 $ python sub.py [demo/pub2]

 - 引数なしならdemo/pub1でsubscribe
 - 引数を指定（例えばdemo/pub2）すると、そのキーでsubscribe
"""
import sys
import time
import json
import zenoh
from zenoh import Reliability, Sample


HOST = ''  # publisherと異なるIPアドレスならここで設定する
PORT = 7447
DEFAULT_KEY = 'demo/pub1'


StateDone = False


def listener(sample: Sample):
    global StateDone
    kind = sample.kind
    key_expr = sample.key_expr
    payload = sample.payload.decode('utf-8')
    print(f">> [Subscriber] Received {kind} ('{key_expr}': '{payload}')")
    if payload == 'done':
        StateDone = True


if __name__ == '__main__':
    key = DEFAULT_KEY
    if len(sys.argv) > 1:
        # 引数があればそれをkeyにする
        key = sys.argv[1]

    conf = zenoh.Config()
    if HOST:
        conf.insert_json5(zenoh.config.LISTEN_KEY,
                          json.dumps([f'tcp/{HOST}:{PORT}']))
    zenoh.init_logger()
    session = zenoh.open(conf)
    print("Declaring Subscriber on '{}'...".format(key))

    sub = session.declare_subscriber(key, listener,
                                     reliability=Reliability.RELIABLE())

    while True:
        time.sleep(1)
        if StateDone:
            break

    sub.undeclare()
    session.close()
