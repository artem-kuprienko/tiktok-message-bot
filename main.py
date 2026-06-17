from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import random
import datetime
import time
import os
import sys


def note_error(exception):
    with open("error_log.txt", "a", encoding="utf-8") as file:
        file.write(f"{datetime.datetime.now()}: {exception}\n")


def main(playwright):
    try:
        while True:
            if datetime.datetime.now().hour > 7: 
                current_time = datetime.datetime.now().strftime("%d-%m-%Y")
                with open("timer.txt", "a+", encoding="utf-8") as file:
                    file.seek(0)

                    if current_time not in file.read():
                        print("Not sent today, sending now...")

                        result = run_browser(playwright)

                        if result is True:
                            print("Sent successfull")

                            file.write(current_time + "\n")
                            print("Date added successfully")
                                    
                        elif result is None:
                            print("Failed to launch browser")
                            note_error("Failed to launch browser")
                        else:
                            print("Sent failed")
                            note_error("Sent failed")
                    else:
                        print("Already sent today")

            CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL_SEC", "600")) # set in .env, 10m default
            time.sleep(CHECK_INTERVAL)
    except Exception as exception:
        print(f"Error while timer function: {exception}")
        note_error(f"Error while timer function: {exception}")
    

def run_browser(playwright):

    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    print(f"Headless mode: {HEADLESS}")
    
    FRIEND_NAME = os.getenv("FRIEND_NAME")
    if not FRIEND_NAME:
        sys.exit("Error: FRIEND_NAME not set in .env file")

    messages_str = os.getenv("MESSAGES")
    if not messages_str:
        sys.exit("Error: MESSAGES not set in .env file")
    
    messages = messages_str.split("|")
    MESSAGE = random.choice(messages)
    print(f"Selected message: {MESSAGE}")

    context = None
    try:   
        context = playwright.chromium.launch_persistent_context(
        "session_data_tiktok",
        headless=HEADLESS,
        locale="uk-UA",
        timezone_id="Europe/Kiev",
        args=["--disable-blink-features=AutomationControlled"],
    )
        page = context.pages[0]
        page.goto("https://www.tiktok.com/messages?lang=uk-UA")
        page.wait_for_load_state("networkidle")
        
        try:
            # Клик по нужному контакту
            page.locator(f'[data-e2e="dm-new-conversation-nickname"]:has-text("{FRIEND_NAME}")').click()
            
            # Жди поле ввода
            page.wait_for_selector(".public-DraftStyleDefault-block", timeout=5000)
            
            # Заполни и отправь
            page.locator(".public-DraftStyleDefault-block").fill(MESSAGE)
            page.get_by_role("button", name="Відправити").click()
            page.wait_for_timeout(1000)
            return True
        except Exception as e:
            note_error(f"Error during send: {e}")
            return False
    
    except Exception as exception:
        print(f"Error while launching browser: {exception}")
        note_error(f"Error while launching browser: {exception}")
        return None

    finally:
        if context:
            context.close()


if __name__ == "__main__":

    load_dotenv()
    with sync_playwright() as playwright:
        main(playwright)