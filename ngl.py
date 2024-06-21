import random
import string
import requests
import os
from flask_socketio import SocketIO

def deviceId():
    characters = string.ascii_lowercase + string.digits
    return f"{''.join(random.choices(characters, k=8))}-" \
           f"{''.join(random.choices(characters, k=4))}-" \
           f"{''.join(random.choices(characters, k=4))}-" \
           f"{''.join(random.choices(characters, k=4))}-" \
           f"{''.join(random.choices(characters, k=12))}"

def UserAgent():
    with open('user-agents.txt', 'r') as file:
        user_agents = file.readlines()
    return random.choice(user_agents).strip()

def Proxy():
    with open('proxies.txt', 'r') as file:
        proxies_list = file.readlines()
    if not proxies_list:
        raise ValueError("Error: proxies.txt is empty. Please add proxies to the file.")
    random_proxy = random.choice(proxies_list).strip()
    return {'http': random_proxy, 'https': random_proxy}

def ngl(nglusername, message, count, use_proxy, socketio):
    if use_proxy:
        proxies = Proxy()
    else:
        proxies = None

    value = 1  # Start from 1 instead of 0
    notsend = 0
    while value <= count:
        headers = {
            'Host': 'ngl.link',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': UserAgent(),
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'https://ngl.link',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': f'https://ngl.link/{nglusername}',
            'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        data = {
            'username': nglusername,
            'question': message,
            'deviceId': deviceId(),
            'gameSlug': '',
            'referrer': '',
        }

        try:
            response = requests.post('https://ngl.link/api/submit', headers=headers, data=data, proxies=proxies)
            if response.status_code == 200:
                socketio.emit('log', {'message': f"Send => {value}"})
                value += 1
            else:
                notsend += 1
                socketio.emit('log', {'message': "Not Send"})
            if notsend == 4:
                socketio.emit('log', {'message': "Changing information"})
                deviceId()
                UserAgent()
                if use_proxy:
                    proxies = Proxy()
                notsend = 0
        except requests.exceptions.ProxyError:
            if use_proxy:
                proxies = Proxy()
