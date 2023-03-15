import os
import openai
openai.organization = "org-WE8sJZEE7ZJuLyym6HyXaKDZ"
openai.api_key = "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"  #os.getenv("")
# print(openai.Model.list())


print("For system content")

sys_msg = input()

post_msg = []
[
    {"role": "system", "content": sys_msg},
]
while True:
    curr_msg = input("What do you want to ask?\n")
    post_msg.append(
        {
            "role": "user",
            "content": curr_msg
        }
    )
    print("Responding...")
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=post_msg,
            stream=True
        )
    except:
        post_msg.pop(-1)
        continue
    res_msg = ""
    res_role = ""
    for chunk in res:
        if chunk["choices"][0]["delta"].get("role"):
            res_role = chunk["choices"][0]["delta"]["role"]
        if chunk["choices"][0]["delta"].get("content"):
            msg = chunk["choices"][0]["delta"]["content"]
            res_msg += msg
            print(msg, end='')
    post_msg.append(
        {
            "role": res_role,
            "content": res_msg
        }
    )
    print("----- msg end -----")