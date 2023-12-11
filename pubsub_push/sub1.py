import time
import json
import zenoh
from zenoh import Reliability, Sample


HOST = ''  # publisherと異なるIPアドレスならここで設定する
PORT = 7447
KEY = 'demo/example/pub1'


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
    conf = zenoh.Config()
    if HOST:
        conf.insert_json5(zenoh.config.LISTEN_KEY,
                          json.dumps([f'tcp/{HOST}:{PORT}']))
    zenoh.init_logger()
    session = zenoh.open(conf)
    print("Declaring Subscriber on '{}'...".format(KEY))

    sub = session.declare_subscriber(KEY, listener,
                                     reliability=Reliability.RELIABLE())

    while True:
        time.sleep(1)
        if StateDone:
            break

    sub.undeclare()
    session.close()
