import re
import cleverbot
import omeglebot


class CleverOmegleBot(omeglebot.OmegleBot):
    def __init__(self):
        super().__init__()
        self._cleverbot = cleverbot.Cleverbot()

    def handle_message(self, message: str) -> str:
        while True:
            try:
                response = self._cleverbot.ask(message)
                response = re.sub('&.+?;', '', response)
                response = re.sub('(bot|cleverbot)',
                                  'Shirley Bottleworth',
                                  response,
                                  re.IGNORECASE)
                return response

            except cleverbot.CleverbotAPIRejection as ex:
                print("Exception:", type(ex), ex)
                return "How does that make you feel?"


if __name__ == '__main__':
    CleverOmegleBot().start()