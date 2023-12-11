import time
import json
import zenoh


KEY_PUB_1 = 'demo/example/pub1'
KEY_PUB_2 = 'demo/example/pub2'
KEY_PUB_ALL = 'demo/example/**'

HOST_1 = '127.0.0.1'            # 送付先IPアドレス1
HOST_2 = '127.0.0.1'            # 送付先IPアドレス2
PORT = 7447

if __name__ == '__main__':
    conf = zenoh.Config()
    conf.insert_json5(zenoh.config.CONNECT_KEY,
                      json.dumps([f'tcp/{HOST_1}:{PORT}',
                                  f'tcp/{HOST_2}:{PORT}']))

    zenoh.init_logger()
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
        time.sleep(1)

    print('done')
    pub_all.put('done')

    pub1.undeclare()
    pub2.undeclare()
    pub_all.undeclare()
    session.close()
