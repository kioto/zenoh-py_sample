"""
P2P(pull) subscriber

Usage:
 $ python sub.py [demo/pub2]

 - publishのタイミングに寄らず、subscribeしたデータを１秒ごとにqueueからを取り出す
 - 引数なしならdemo/pub1でsubscribe
 - 引数を指定（例えばdemo/pub2）すると、そのキーでsubscribe
"""
import sys
import json
import zenoh


HOST = ''  # publisherと異なるIPアドレスならここで設定する
PORT = 7447
DEFAULT_KEY = 'demo/pub1'


def main(conf):
    zenoh.init_log_from_env_or('error')

    with zenoh.open(conf) as session:
        print(f"Declaring Subscriber on '{key}'...")

        with session.declare_subscriber(key) as sub:
            # subがqueueになっているので、順に取り出す
            for sample in sub:
                payload = sample.payload.to_string()
                print(f">> [Subscriber] Received {sample.kind}"
                      f"('{sample.key_expr}': '{payload}')")
                if payload == 'done':
                    break

    print('done')


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
