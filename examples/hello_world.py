from flask import Flask, request, jsonify
from alicemsg import AliceClient, messages

app = Flask(__name__)
client = AliceClient()


@client.register_text_message_processor()
def text_handler(incoming):
    return messages.Message(incoming.text)


@app.route('/incoming')
def incoming():
    response = client.process_json(request.json)
    return jsonify(response.to_dict())
