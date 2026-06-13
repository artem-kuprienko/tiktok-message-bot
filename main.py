from playwright.sync_api import sync_playwright
import random
import datetime
import time

def note_error(exception):
    with open("error_log.txt", "a") as file:
        file.write(f"{datetime.datetime.now()}: {exception}\n")

def main(playwright):
    try:
        while True:
            if datetime.datetime.now().hour > 8: 
                current_time = datetime.datetime.now().strftime("%d-%m-%Y")
                with open("timer.txt", "a+") as file:
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

            time.sleep(600)
    except Exception as exception:
        print(f"Error while timer function: {exception}")
        note_error(f"Error while timer function: {exception}")

def run_browser(playwright):
    try:   
        context = playwright.chromium.launch_persistent_context(
        "session_data",
        headless=True,
        args=["--disable-blink-features=AutomationControlled"],  # Прячет navigator.webdriver
    )
        page = context.pages[0]
        page.goto("https://www.tiktok.com/messages?lang=uk-UA")
        
        try:
            page.get_by_role("paragraph").filter(has_text="Mavrodi").click()
            page.locator(".public-DraftStyleDefault-block").fill(random.choice(["🔥", "😀", "👍"]))
            page.get_by_role("button", name="Відправити").click()
            page.wait_for_timeout(2000)
            return True
        except Exception as exception:
            print(f"Error during navigation: {exception}")
            note_error(f"Error during navigation: {exception}")
            return False
    
    except Exception as exception:
        print(f"Error while launching browser: {exception}")
        note_error(f"Error while launching browser: {exception}")
        return None



if __name__ == "__main__":
    with sync_playwright() as playwright:
        main(playwright)