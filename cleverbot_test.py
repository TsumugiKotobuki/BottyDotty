from time import sleep
import cleverbot
import omegle


class CleverbotOmegleBridge(omegle.OmegleAPI):
    def __init__(self):
        super().__init__()
        self._cleverbot = cleverbot.Cleverbot()

    def handle_message(self, message: str) -> str:
        while True:
            try:
                return self._cleverbot.ask(message)
            except cleverbot.CleverbotAPIRejection as ex:
                print("Exception:", type(ex), ex)
                sleep(1)


if __name__ == '__main__':
    CleverbotOmegleBridge().start()