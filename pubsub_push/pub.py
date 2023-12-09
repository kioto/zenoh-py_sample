import time
import zenoh


KEY_BASE = 'demo/example/'
KEY_PUB_1 = KEY_BASE + 'pub1'
KEY_PUB_2 = KEY_BASE + 'pub2'
KEY_PUB_ALL = KEY_BASE + '**'

CONF = zenoh.Config()


if __name__ == '__main__':
    zenoh.init_logger()
    session = zenoh.open(CONF)

    value = 'Pub from Python!'

    pub1 = session.declare_publisher(KEY_PUB_1)
    pub2 = session.declare_publisher(KEY_PUB_2)
    pub_all = session.declare_publisher(KEY_PUB_ALL)

    for idx in range(10):
        st = idx % 3
        if st == 1:
            pub1.put(f'message to pub1 {idx}')
        elif st == 2:
            pub2.put(f'message to pub2 {idx}')
        else:
            pub_all.put(f'message to pub all {idx}')

        time.sleep(1)

    pub_all.put('done')

    pub1.undeclare()
    pub2.undeclare()
    pub_all.undeclare()
    session.close()
