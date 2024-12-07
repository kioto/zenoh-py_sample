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


HOST = ''  # publisherと異なるIPアドレスならここで設定する
PORT = 7447
DEFAULT_KEY = 'demo/pub1'


StateDone = False


def listener(sample: zenoh.Sample):
    global StateDone
    kind = sample.kind
    key_expr = sample.key_expr
    payload = sample.payload.to_string()
    print(f">> [Subscriber] Received {kind} ('{key_expr}': '{payload}')")
    if payload == 'done':
        StateDone = True


def main(conf):
    zenoh.init_log_from_env_or('error')
    session = zenoh.open(conf)
    print("Declaring Subscriber on '{}'...".format(key))

    sub = session.declare_subscriber(key, listener)

    while True:
        time.sleep(1)
        if StateDone:
            break

    sub.undeclare()
    session.close()


if __name__ == '__main__':
    key = DEFAULT_KEY
    if len(sys.argv) > 1:
        # 引数があればそれをkeyにする
        key = sys.argv[1]
    conf = zenoh.Config()

    # subscriberのホストを追加
    if HOST:
        conf.insert_json5(zenoh.config.LISTEN_KEY,
                          json.dumps([f'tcp/{HOST}:{PORT}']))

    main(conf)
