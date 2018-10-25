import pytest

from alicemsg import AliceClient
from alicemsg.models import messages


class TestMessengerClient:
    def test_init(self):
        client = AliceClient()
        assert client.text_message_processor is None
        assert client.callback_processor is None

        msg_json = {
            "meta": {
                "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
                "interfaces": {
                    "screen": {}
                },
                "locale": "ru-RU",
                "timezone": "UTC"
            },
            "request": {
                "command": "",
                "nlu": {
                    "entities": [],
                    "tokens": []
                },
                "original_utterance": "",
                "type": "SimpleUtterance"
            },
            "session": {
                "message_id": 0,
                "new": True,
                "session_id": "4d561804-a51d901c-fbb986a4-1699b7",
                "skill_id": "934d5268-3d49-4b5a-bb53-97200edd0a0b",
                "user_id": "1AF98159AEAC9F1ABA46DC479ECD790CB97E75F3D0DA5E84331279FF57296926"
            },
            "version": "1.0"
        }
        with pytest.raises(AttributeError):
            client.process_json(msg_json)

        msg_json = {
            "meta": {
                "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
                "interfaces": {
                    "screen": {}
                },
                "locale": "ru-RU",
                "timezone": "UTC"
            },
            "request": {
                "nlu": {
                    "entities": [],
                    "tokens": []
                },
                "payload": {
                    "aaa": "bbb"
                },
                "type": "ButtonPressed"
            },
            "session": {
                "message_id": 3,
                "new": False,
                "session_id": "1cd02173-43c63383-3f975d2e-54738",
                "skill_id": "934d5268-3d49-4b5a-bb53-97200edd0a0b",
                "user_id": "1AF98159AEAC9F1ABA46DC479ECD790CB97E75F3D0DA5E84331279FF57296926"
            },
            "version": "1.0"
        }

        with pytest.raises(AttributeError):
            client.process_json(msg_json)

    def test_text_message_processor(self):
        client = AliceClient()

        @client.register_text_message_processor()
        def f(request):
            return messages.Message('text')

        assert client.text_message_processor == f

        msg_json = {
            "meta": {
                "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
                "interfaces": {
                    "screen": {}
                },
                "locale": "ru-RU",
                "timezone": "UTC"
            },
            "request": {
                "command": "",
                "nlu": {
                    "entities": [],
                    "tokens": []
                },
                "original_utterance": "",
                "type": "SimpleUtterance"
            },
            "session": {
                "message_id": 0,
                "new": True,
                "session_id": "4d561804-a51d901c-fbb986a4-1699b7",
                "skill_id": "934d5268-3d49-4b5a-bb53-97200edd0a0b",
                "user_id": "1AF98159AEAC9F1ABA46DC479ECD790CB97E75F3D0DA5E84331279FF57296926"
            },
            "version": "1.0"
        }
        response = client.process_json(msg_json)
        assert response.to_dict() == {
            'response': {
                'text': 'text',
                'end_session': False,
            },
            "session": {
                "message_id": 0,
                "session_id": "4d561804-a51d901c-fbb986a4-1699b7",
                "user_id": "1AF98159AEAC9F1ABA46DC479ECD790CB97E75F3D0DA5E84331279FF57296926"
            },
            "version": "1.0"
        }

        @client.register_text_message_processor()
        def f(request):
            return 1

        with pytest.raises(TypeError):
            client.process_json(msg_json)

    def test_callback_processor(self):
        client = AliceClient()

        @client.register_callback_processor()
        def f(request):
            return messages.Message('text')

        assert client.callback_processor == f

        msg_json = {
            "meta": {
                "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
                "interfaces": {
                    "screen": {}
                },
                "locale": "ru-RU",
                "timezone": "UTC"
            },
            "request": {
                "nlu": {
                    "entities": [],
                    "tokens": []
                },
                "payload": {
                    "aaa": "bbb"
                },
                "type": "ButtonPressed"
            },
            "session": {
                "message_id": 3,
                "new": False,
                "session_id": "1cd02173-43c63383-3f975d2e-54738",
                "skill_id": "934d5268-3d49-4b5a-bb53-97200edd0a0b",
                "user_id": "1AF98159AEAC9F1ABA46DC479ECD790CB97E75F3D0DA5E84331279FF57296926"
            },
            "version": "1.0"
        }

        response = client.process_json(msg_json)
        assert response.to_dict() == {
            'response': {
                'text': 'text',
                'end_session': False,
            },
            "session": {
                "message_id": 3,
                "session_id": "1cd02173-43c63383-3f975d2e-54738",
                "user_id": "1AF98159AEAC9F1ABA46DC479ECD790CB97E75F3D0DA5E84331279FF57296926"
            },
            "version": "1.0"
        }

        @client.register_callback_processor()
        def f(request):
            return 1

        with pytest.raises(TypeError):
            client.process_json(msg_json)

    def test_incorrect_request(self):
        client = AliceClient()
        msg_json = {
            "meta": {
                "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
                "interfaces": {
                    "screen": {}
                },
                "locale": "ru-RU",
                "timezone": "UTC"
            },
            "request": {
                "nlu": {
                    "entities": [],
                    "tokens": []
                },
                "payload": {
                    "aaa": "bbb"
                },
                "type": "FAIL"
            },
            "session": {
                "message_id": 3,
                "new": False,
                "session_id": "1cd02173-43c63383-3f975d2e-54738",
                "skill_id": "934d5268-3d49-4b5a-bb53-97200edd0a0b",
                "user_id": "1AF98159AEAC9F1ABA46DC479ECD790CB97E75F3D0DA5E84331279FF57296926"
            },
            "version": "1.0"
        }

        with pytest.raises(ValueError):
            client.process_json(msg_json)
        with pytest.raises(TypeError):
            client.process_json(1)
        with pytest.raises(KeyError):
            client.process_json({})
        with pytest.raises(KeyError):
            client.process_json({'request': {}})
        with pytest.raises(TypeError):
            client.process_json({'request': {'type': 1}})