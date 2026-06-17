from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import random
import datetime
import time
import os


def note_error(exception):
    with open("error_log.txt", "a", encoding="utf-8") as file:
        file.write(f"{datetime.datetime.now()}: {exception}\n")


def main(playwright):
    
    CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL_SEC", "600"))
    SEND_TIME_HOUR = int(os.getenv("SEND_TIME_HOUR", "8"))
    
    try:
        while True:
            now = datetime.datetime.now()
            current_date = now.strftime("%d-%m-%Y")
            
            # Проверь: уже ли нужное время И еще не отправлено сегодня
            if now.hour >= SEND_TIME_HOUR:
                with open("timer.txt", "a+", encoding="utf-8") as file:
                    file.seek(0)
                    
                    if current_date not in file.read():
                        print(f"Time is {now.hour}:{now.minute:02d}, sending now...")
                        result = run_browser(playwright)
                        
                        if result is True:
                            print("Sent successfully")
                            file.write(current_date + "\n")
                        elif result is None:
                            print("Failed to launch browser")
                            note_error("Failed to launch browser")
                        else: # False
                            print("Sent failed")
                            note_error("Sent failed")
                    else:
                        print(f"Already sent today")
            else:
                print(f"Not yet time. Current: {now.hour}:{now.minute:02d}, Target: {SEND_TIME_HOUR}:00")
            
            time.sleep(CHECK_INTERVAL)

    except Exception as exception:
        print(f"Error while timer function: {exception}")
        note_error(f"Error while timer function: {exception}")
    

def run_browser(playwright):

    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true" # set in .env
    print(f"Headless mode: {HEADLESS}")
    
    FRIEND_NAME = os.getenv("FRIEND_NAME") # set in .env
    if not FRIEND_NAME:
        print("Error: FRIEND_NAME not set in .env file")
        note_error("FRIEND_NAME not set in .env file")
        return None

    messages_str = os.getenv("MESSAGES")
    if not messages_str:
        print("Error: MESSAGES not set in .env file")
        note_error("MESSAGES not set in .env file")
        return None
    
    messages = messages_str.split("|")
    MESSAGE = random.choice(messages) # set in .env (possible one or multi/random message, to make random text use |, text1|text2)
    print(f"Selected message: {MESSAGE}")

    context = None
    try:   
        context = playwright.chromium.launch_persistent_context(
            "session_data_tiktok",
            headless=HEADLESS,
            locale="uk-UA", # browser language
            timezone_id="Europe/Kiev", #browser timezone
            args=["--disable-blink-features=AutomationControlled"], # arg disables webDriver, without impossible to start tiktok
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