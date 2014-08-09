import cleverbot
import omegle


class CleverbotOmegleBridge(omegle.OmegleAPI):
    def __init__(self):
        super().__init__()
        self._cleverbot = cleverbot.Cleverbot()

    def handle_message(self, message: str) -> str:
        return self._cleverbot.ask(message)


if __name__ == '__main__':
    CleverbotOmegleBridge().start()