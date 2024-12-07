"""
P2P publisher (no wait)

Usage:
 $ python pub_nowait.py

 待ち時間なしでdemo/**, demo/pub1, demo/pub2を順にpublishする。
"""

import time
import json
import zenoh


KEY_PUB_1 = 'demo/pub1'
KEY_PUB_2 = 'demo/pub2'
KEY_PUB_ALL = 'demo/**'

HOSTS = []  # 送り先IPアドレスを文字列のリストで指定（未指定でlocalhost）
PORT = 7447


if __name__ == '__main__':
    conf = zenoh.Config()

    # subscriberのホストを追加
    if HOSTS:
        hosts = []
        for host in HOSTS:
            hosts.append(f'tcp/{host}:{PORT}')
        conf.insert_json5(zenoh.config.CONNECT_KEY, json.dumps(hosts))

    # 実行
    zenoh.init_log_from_env_or('error')
    session = zenoh.open(conf)
    pub1 = session.declare_publisher(KEY_PUB_1)
    pub2 = session.declare_publisher(KEY_PUB_2)
    pub_all = session.declare_publisher(KEY_PUB_ALL)

    for idx in range(10):
        st = idx % 3
        msg = ''
        key = ''
        if st == 1:
            key = KEY_PUB_1
            msg = f'message to pub1 {idx}'
            pub1.put(msg)
        elif st == 2:
            key = KEY_PUB_2
            msg = f'message to pub2 {idx}'
            pub2.put(msg)
        else:
            key = KEY_PUB_ALL
            msg = f'message to pub all {idx}'
            pub_all.put(msg)

        print(f">> [Publisher] Sent PUT ('{key}': '{msg}')")

    print('done')
    pub_all.put('done')

    pub1.undeclare()
    pub2.undeclare()
    pub_all.undeclare()
    session.close()
