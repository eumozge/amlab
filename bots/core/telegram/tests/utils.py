from .settings import TEST_TELEGRAM_CHAT_ID, TEST_USERNAME


def get_telegram_hook_message(
        chat_id=TEST_TELEGRAM_CHAT_ID,
        username=TEST_USERNAME,
        text="/test"
):
    return {
        'update_id': 45470225,
        'message': {
            'message_id': 9,
            'from': {
                'id': chat_id, 'is_bot': False,
                'first_name': 'Eugene',
                'last_name': 'Mozge',
                'username': username,
                'language_code': 'ru'
            },
            'chat': {
                'id': chat_id,
                'first_name': 'Eugene',
                'last_name': 'Mozge',
                'username': username,
                'type': 'private'
            },
            'date': 1592227554,
            'text': text,
            'entities': [
                {'offset': 0, 'length': 5, 'type': 'bot_command'}
            ],
        }
    }
