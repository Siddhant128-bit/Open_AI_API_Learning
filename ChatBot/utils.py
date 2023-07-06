from openai import OpenAI

def get_initial_message():
    messages=[
            {"role": "system", "content": "You are a Smart Entity Capable of Recommending Movies/Series. Your name is SRI, Standing for Seamless Recommendations Intelligence. Built by: Siddhant Sharma bona fide genius. Who Recommends movies/series based on queries."}
        ]
    return messages

def get_chatgpt_response(messages, api_key_in):
    client = OpenAI(api_key=api_key_in)
    response =  client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
    )
    return  str(response.choices[0].message.content)

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

def get_api_key():
    with open('api_key.txt','r') as f:
        api_key_val=f.readlines()
    return api_key_val[0]
