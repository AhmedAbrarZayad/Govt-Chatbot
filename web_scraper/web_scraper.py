from playwright.sync_api import sync_playwright

url = "https://resource.ogrlegal.com/licences/basic/tin/#step-1-portal-access-and-initial-registration"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.goto(url, wait_until="networkidle")
    
    # Extract clean plain text from the main article only
    clean_text = page.locator('.article-content').inner_text()
    
    browser.close()

# Save as .txt file
with open("TIN_for_Companies_Bangladesh.txt", "w", encoding="utf-8") as f:
    f.write(clean_text)

print("✅ Done! Clean content saved as: TIN_for_Companies_Bangladesh.txt")