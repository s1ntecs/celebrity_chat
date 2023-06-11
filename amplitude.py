from amplitude import Amplitude, BaseEvent
from create_bot import AMPLITUDE_API_KEY

amplitude = Amplitude(AMPLITUDE_API_KEY)


async def register_user(user_id: int):
    amplitude.track(
        BaseEvent(
            event_type="user_register",
            user_id=user_id,
            event_properties={
                "source": "user registered"
            }
        )
        )


async def user_changed_char(user_id: int):
    amplitude.track(
        BaseEvent(
            event_type="changed_char",
            user_id=str(user_id),
            event_properties={
                "source": "user changed character"
            }
        )
        )


async def get_question(user_id: int):
    amplitude.track(
        BaseEvent(
            event_type="get_question",
            user_id=str(user_id),
            event_properties={
                "source": "get question from client"
            }
        )
        )


async def send_client(user_id: int):
    amplitude.track(
        BaseEvent(
            event_type="send_answer",
            user_id=str(user_id),
            event_properties={
                "source": "answer sent to client"
            }
        )
        )
