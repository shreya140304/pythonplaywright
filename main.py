import asyncio
import os
from playwright.async_api import async_playwright

STORAGE_STATE = "storage_state.json"

# Replace with your app details
BASE_URL = "https://example.com/login"
USERNAME = "your_username"
PASSWORD = "your_password"

USERNAME_SELECTOR = "input[name='username']"
PASSWORD_SELECTOR = "input[name='password']"
LOGIN_BUTTON_SELECTOR = "button[type='submit']"
AUTH_MARKER_SELECTOR = "text=Dashboard"  # something visible only after login


async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        context_args = {}
        if os.path.exists(STORAGE_STATE):
            print("✅ Using existing session")
            context_args["storage_state"] = STORAGE_STATE

        context = await browser.new_context(**context_args)
        page = await context.new_page()

        if not os.path.exists(STORAGE_STATE):
            print("🔑 No session found, logging in...")
            await page.goto(BASE_URL)
            await page.fill(USERNAME_SELECTOR, USERNAME)
            await page.fill(PASSWORD_SELECTOR, PASSWORD)
            await page.click(LOGIN_BUTTON_SELECTOR)
            # Wait for something that confirms login succeeded
            await page.wait_for_selector(AUTH_MARKER_SELECTOR, timeout=15000)

            # Save session
            await context.storage_state(path=STORAGE_STATE)
            print("💾 Session saved!")

        # At this point, you’re logged in
        await page.goto("https://example.com/dashboard")
        await page.wait_for_timeout(5000)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
