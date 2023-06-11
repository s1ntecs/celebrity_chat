import asyncgpt
from create_bot import OPENAI_TOKEN

bot = asyncgpt.GPT(apikey=OPENAI_TOKEN)


async def get_answer_gpt(message_text, char_name):
    content = f"You are {char_name}. Do not give dangerous information."
    completion = await bot.chat_complete(
        [{'role': 'system', 'content': content},
         {'role': 'user', 'content': message_text}])
    return str(completion.choices[0])
