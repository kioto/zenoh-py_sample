import time
import zenoh
from zenoh import Reliability, Sample

CONF = zenoh.Config()
KEY = 'demo/example/pub2'

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
    zenoh.init_logger()
    session = zenoh.open(CONF)
    print("Declaring Subscriber on '{}'...".format(KEY))

    sub = session.declare_subscriber(KEY, listener,
                                     reliability=Reliability.RELIABLE())

    while True:
        time.sleep(1)
        if StateDone:
            break

    sub.undeclare()
    session.close()
