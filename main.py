from playwright.sync_api import sync_playwright
import random

def main(playwright):
    page = run(playwright)

    if page:
        if navigation(page):
            print("Sent successful")
        else:
            print("Sent failed")
    else:
        print("Failed to launch browser")

def run(playwright):
    try:   
        context = playwright.chromium.launch_persistent_context(
        "session_data",
        headless=True,
        args=["--disable-blink-features=AutomationControlled"],  # Прячет navigator.webdriver
    )
        page = context.pages[0]
        page.goto("https://www.tiktok.com/messages?lang=uk-UA")
        return page
    except Exception as exception:
        print(f"Error while launching browser: {exception}")
        return None
    
def navigation(page):
    try:
        page.get_by_role("paragraph").filter(has_text="Mavrodi").click()
        page.locator(".public-DraftStyleDefault-block").fill(random.choice(["🔥", "😀", "👍"]))
        page.get_by_role("button", name="Відправити").click()
        return True
    except Exception as exception:
        print(f"Error during navigation: {exception}")
        return False
    



if __name__ == "__main__":
    with sync_playwright() as playwright:
        main(playwright)