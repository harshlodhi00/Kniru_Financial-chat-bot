from flask import Flask, render_template, request, jsonify
from typing import Union

import openai

OPENAI_API_KEY = 'YOUR_API_KEY' #paste you api key at the place of YOUR_API_KEY

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
@app.route("/")

def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET","POST"])                
                             
def chat():
    msg = request.form["msg"]
    input = msg
    return get_Chat_response(input)

def get_api_response(prompt: str) -> str | None:
    text: str | None = None

    try:
        response: dict = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
        )

        choices: dict = response.get('choices')[0]
        text = choices.get('text')

    except Exception as e:
        print('Some Problem Occurs: ', e)

    return text


def update_list(message: str, pl: list[str]):
    pl.append(message)


def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = message
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt


def get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
    else:
        bot_response = 'Something went wrong...'

    return bot_response


def get_Chat_response(input):
    prompt_list: list[str] = ['You are a fianancial assistance and you have to assist the personal with his financial data',
                              '\nHere it his/her financial data in json file, you have to give suggestion based on this data',
                              '{ "date": "2021-01-01", "amount": 1000, "category": "income", "description": "salary" },{ "date": "2021-01-02", "amount": -50, "category": "groceries", "description": "milk and eggs" },{ "date": "2021-01-03", "amount": -100, "category": "entertainment", "description": "movie tickets" },{ "date": "2021-01-04", "amount": -20, "category": "transportation", "description": "bus fare" },{ "date": "2021-01-05", "amount": -200, "category": "bills", "description": "electricity bill" },{ "date": "2021-01-06", "amount": -30, "category": "groceries", "description": "bread and cheese" },{ "date": "2021-01-07", "amount": -150, "category": "clothing", "description": "new shoes" },{ "date": "2021-01-08", "amount": -40, "category": "healthcare", "description": "prescription drugs" },{ "date": "2021-01-09", "amount": -80, "category": "education", "description": "online course" },{ "date": "2021-01-10", "amount": -60, "category": "entertainment", "description": "pizza delivery" }']
    
    user_input: str = input
    response: str = get_bot_response(user_input, prompt_list)
    return response


if __name__ == '__main__':

    app.run()