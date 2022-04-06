def get_feedback_test_request_data() -> dict:
    return {
        "full_name": "John",
        "phone_number": "0009908098",
        "email": "example@gmail.com",
        "score": 2,
    }


def get_feedback_test_response_data() -> dict:
    return {
        "full_name": "John",
        "phone_number": "0009908098",
        "email": "example@gmail.com",
        "score": 2,
        "comment": None,
        "waiter_id": None,
    }


def get_waiters_test_responce_data() -> list:
    return [
        {"id": "1", "name": "Mark Lutz"},
        {"id": "2", "name": "Yuvraj Gupta"},
        {"id": "3", "name": "Paul Barry"},
        {"id": "4", "name": "Virat Kohli"},
        {"id": "5", "name": "James Anderson"},
        {"id": "6", "name": "Kevin Pietersen"},
        {"id": "7", "name": "Ricky Ponting"},
    ]
