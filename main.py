from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/")
    input()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)