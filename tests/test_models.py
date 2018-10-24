import pytest

from alicemsg.models.messages import Button, Buttons, Message
from alicemsg.models.requests import CallbackRequest, TextMessageRequest
from alicemsg.models.responses import AliceResponse


class TestButtons:
    def test_Button(self):
        button = Button('title', 'url.com', {'aa': 'bb'}, False)
        assert button.to_dict() == {'title': 'title',
                                    'url': 'url.com',
                                    'payload': {'aa': 'bb'},
                                    'hide': False}
        with pytest.raises(TypeError):
            Button(1, 'vk.com')
        with pytest.raises(TypeError):
            Button('title', {})
        with pytest.raises(TypeError):
            Button('title', 'vk.com', {'aa': 'bb'}, 42)

    def test_Buttons(self):
        buttons = Buttons([Button('title1')])
        with pytest.raises(TypeError):
            buttons.add(1)
        with pytest.raises(TypeError):
            Buttons(1)
        with pytest.raises(TypeError):
            Buttons([1])
        button1 = Button('title2', payload={'aa': 'bb'})
        button2 = Button('title3', 'url', 'payload', False)
        buttons.add(button1)
        buttons.add(button2)
        assert buttons.to_dict() == [
            {'title': 'title1', 'hide': True},
            {'title': 'title2', 'payload': {'aa': 'bb'}, 'hide': True},
            {'title': 'title3', 'url': 'url', 'payload': 'payload', 'hide': False}
        ]


class TestMessage:
    def test_Message_without_Buttons(self):
        message = Message('text')
        assert message.to_dict() == {'text': 'text', 'end_session': False}
        message = Message('text', end_session=True)
        assert message.to_dict() == {'text': 'text', 'end_session': True}
        with pytest.raises(TypeError):
            Message(1)
        with pytest.raises(TypeError):
            Message('1', end_session=1)

    def test_Message_with_Buttons(self):
        buttons = Buttons([Button('title1')])
        message = Message('text', buttons)
        assert message.to_dict() == {'text': 'text', 'end_session': False,
                                     'buttons': [{'title': 'title1', 'hide': True}]}
        with pytest.raises(TypeError):
            Message('text', 22)


class TestRequests:
    def test_TextMessageRequest(self):
        TextMessageRequest({}, '', '', '', [])
        with pytest.raises(TypeError):
            TextMessageRequest(1, '', '', '', [])
        with pytest.raises(TypeError):
            TextMessageRequest({}, 1, '', '', [])
        with pytest.raises(TypeError):
            TextMessageRequest({}, '', 1, '', [])
        with pytest.raises(TypeError):
            TextMessageRequest({}, '', '', 1, [])
        with pytest.raises(TypeError):
            TextMessageRequest({}, '', '', '', 1)

    def test_CallbackRequest(self):
        CallbackRequest({}, '', '', '')
        with pytest.raises(TypeError):
            CallbackRequest(1, '', '', '')
        with pytest.raises(TypeError):
            CallbackRequest({}, 1, '', '')
        with pytest.raises(TypeError):
            CallbackRequest({}, '', 1, '')


class TestAliceResponse:
    def test_AliceResponse(self):
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
        message = Message('text')
        response = AliceResponse(message=message, session=msg_json['session'], version=msg_json['version'])
        with pytest.raises(TypeError):
            AliceResponse({}, {}, '')
        with pytest.raises(TypeError):
            AliceResponse(message, 1, '')
        with pytest.raises(TypeError):
            AliceResponse(message, {}, 1)

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
