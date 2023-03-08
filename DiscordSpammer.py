import time
import datetime
import requests
import msvcrt
import os

P = '\033[35m' # pink
G = '\033[90m' # grey
w = '\033[37m' # white
P = '\033[35m' # purple
R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
RE = '\033[0m' # reset
Y = '\033[33m' # yellow
B = '\033[34m' # blue
LG = '\033[37m' # lightgrey

os.system('cls')

def start():
    os.system('cls')
    spammer()

def spammer():
    delete = False
    now = datetime.datetime.now()
    while True:
        delInput = input(f"{C}> {w}Delete webhook on exit (Y/N): ")
        while delInput.capitalize() not in ["Y", "N"]:
            print("\033[F\033[K", end="")
            print(f"{R}Invalid")
            time.sleep(1.5)
            print("\033[F\033[K", end="")
            delInput = input(f"{C}> {w}Delete webhook on exit (Y/N): ")
        if delInput == "Y":
            print(f"Delete: {R}True")
            delete = True
        
        url = input(f"{C}> {w}Enter webhook URL: ")
        while not url.startswith("https://discord.com/api/webhooks/"):
            print("\033[F\033[K", end="")
            print(f"{R}Invalid URL!")
            time.sleep(1.5)
            print("\033[F\033[K", end="")
            url = input(f"{C}> {w}Enter webhook URL: ")

        msg = input(f"{C}> {w}Enter message: ")
        while not msg:
            print("\033[F\033[K", end="")
            print(f"{R}Message cannot be empty!")
            time.sleep(1.5)
            print("\033[F\033[K", end="")
            msg = input(f"{C}> {w}Enter message: ")

        rate = input(f"{C}> {w}Enter rate (in seconds): ")
        while True:
            try:
                rate = float(rate)
                break
            except ValueError:
                print("\033[F\033[K", end="")
                print(f"{R}Invalid rate!")
                time.sleep(1.5)
                print("\033[F\033[K", end="")
                rate = input(f"{C}> {w}Enter rate (in seconds): ")

        cooldown = input(f"{C}> {w}Enter cooldown (in seconds): ")
        while True:
            try:
                cooldown = float(cooldown)
                break
            except ValueError:
                print("\033[F\033[K", end="")
                print(f"{R}Invalid cooldown!")
                time.sleep(1.5)
                print("\033[F\033[K", end="")
                cooldown = input(f"{C}> {w}Enter cooldown (in seconds): ")
        break

    tries = 0
    counter = 0
    current_time = now.strftime("%H:%M:%S")
    response = requests.post(url, json={"content": msg})
    print("\033[F"*4, "\033[K", "\033[K", "\033[K", "\033[K", "\033[K")
    print("\n")
    print(f"\n{C}> {w}Press 'Q' to stop.")
    print(f"{C}{current_time} {w}=> {R}[{response.status_code}] {w}Attempting to send {Y}'{msg}' {w}to '{url}' every {R}{rate} {w}seconds")
    while True:
        if msvcrt.kbhit() and msvcrt.getch() == b"q":
            print(f"{R}Exiting...{RE}")
            if delete:
                requests.delete(url)
                print(f"{Y}Webhook deleted.{RE}")
            return
        response = requests.post(url, json={"content": msg})
        if response.status_code == 204:
            counter += 1
            print(f"{C}{current_time} {w}=> {R}[{response.status_code}] {w}Webhook Spammer | Sent {R}{counter} {w}messages")
            time.sleep(rate)
        elif response.status_code == 429:
            print(f"Spammer | You are being rate-limited")
            print(f"Taking a {R}{cooldown} {w}second break...")
            time.sleep(cooldown)
        elif tries != 5:
            tries += 1
            if response.status_code == 404:
                print(f"{C}{current_time} {w}=> {R}[{response.status_code}] {w}Webhook not found!")
            else:
                print(f"{C}{current_time} {w}=> {R}[{response.status_code}] {w}Request failed!")

            print(f"{C}{current_time} {w}=> {R}[{response.status_code}] {w}Reattempting...")
            time.sleep(rate)
        else:
            print("\nToo many failed attempts!\nReloading...")
            time.sleep(3.5)
            start()

if __name__ == "__main__":
    spammer()