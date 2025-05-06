import requests

def send_sms(to_numbers, message, auth_token):
    """
    Sends an SMS using Aakash SMS API.

    Args:
        to_numbers (str or list): A 10-digit number or a list of such numbers.
        message (str): The message to be sent.
        auth_token (str): Your Aakash SMS API token.

    Returns:
        dict: Contains status_code, response_text, and response_json.
    """
    if isinstance(to_numbers, list):
        to_numbers = ",".join(to_numbers)

    payload = {
        'auth_token': auth_token,
        'to': to_numbers,
        'text': message
    }

    try:
        r = requests.post("https://sms.aakashsms.com/sms/v3/send/", data=payload)
        return {
            'status_code': r.status_code,
            'response_text': r.text,
            'response_json': r.json() if r.headers.get("Content-Type", "").startswith("application/json") else {}
        }
    except requests.RequestException as e:
        return {
            'status_code': 500,
            'response_text': str(e),
            'response_json': {}
        }
