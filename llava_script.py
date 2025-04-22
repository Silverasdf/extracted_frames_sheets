import os

#Env vars
s = 31
e = 60
step = 1
s1 = 0
s3 = 60
API = "LLaVA"
path = "/home/rdpperuski/LLaVA/images/000001"
message = '''This is demo only. not real. do your best. These frames are captured for a potential traffic incident. Give me quanitative information whenever possible. Give me the following and number each answer:
              Number of vehicles in accident in a number,
              Accident Type such as t-bone, rear end, etc,
              Person Injury yes or no,
              Need for ambulance yes or no,
              Need for firetruck yes or no,
              Need for Police yes or no,
              Types of vehicles involved, such as suv, truck, sedan,
              Fire yes or no,
              Day/night and weather, such as clear, etc,
              Low Res/Bad Footage yes or no.
              Please ignore any context before these images and this prompt
 '''
message = message.replace('\n', '')

messages = dict()

#Store config information in messages
messages['s'] = s
messages['e'] = e
messages['step'] = step
messages['s1'] = s1
messages['s3'] = s3
messages["API"] = API
messages['message'] = message

def write_to_image(messages: dict) -> None:
    if not os.path.exists("outputs"):
        os.mkdir("outputs")

    with open(f"./outputs/{s}thru{e}with{step}-{API}.txt", 'w') as output_file:
        print(messages, file=output_file)

def run(dir_num: int):
    files = ""

    print("Reading directory number", dir_num)

    path = f"/home/rdpperuski/LLaVA/images/{dir_num:06d}"
    for i in range(s1, len(os.listdir(path)), s3):
        files += f'{path}/{i}.jpg '
    print(len(os.listdir(path)), "frames in directory")

    cmd = f"echo {message} | python3 llava-multi-images.py --model-path liuhaotian/llava-v1.5-7b --images {files} --load-4bit --concat-strategy grid > message.txt 2> /dev/null"
    print("Command being run:", cmd)

    os.system(cmd)

    with open("message.txt", "r") as f:
        messages[f"{dir_num:06d}"] = f.readlines()

    os.remove("message.txt")

for i in range(s, e+1, step):
    try:
        run(i)
        write_to_image(messages)
    except Exception as e:
        print("Error:", e)
