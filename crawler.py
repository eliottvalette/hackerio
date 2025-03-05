from firecrawl import FirecrawlApp
import json

# Initialize the Firecrawl app
app = FirecrawlApp(api_key='fc-d17aa838a5794d808b37a5721b24ec92')

try:
    print("Starting s0urce.io crawler...")
    
    # Scrape with login actions
    response = app.scrape_url(
        url='https://s0urce.io',
        params={
            'formats': ['markdown'],
            'actions': [
                # Wait for page to load
                { "type": "wait", "milliseconds": 2000 },
                
                # Click on username field
                { "type": "click", "selector": "input[name='input']" },
                
                # Type username
                { "type": "write", "text": "Anonyme", "selector": "input[name='input']" },
                
                # Click Play button
                { "type": "click", "selector": "button.grey.svelte-ec9kqa" },
                
                # Wait for login
                { "type": "wait", "milliseconds": 3000 },
                
                # Take screenshot
                { "type": "screenshot" },
                
                # Final scrape
                { "type": "scrape" }
            ]
        }
    )
    
    print("Crawl successful!")
    
    # Save the response to a file
    with open('s0urce_scrape.md', 'w') as f:
        f.write(response['markdown'])
    
    print("Scraped content saved to s0urce_scrape.md")
    
    # If there are screenshots in the response, print their URLs
    if 'actions' in response and 'screenshots' in response['actions'] and response['actions']['screenshots']:
        print(f"Screenshots captured: {len(response['actions']['screenshots'])}")
        for i, screenshot_url in enumerate(response['actions']['screenshots']):
            print(f"Screenshot {i+1}: {screenshot_url}")
    
except Exception as e:
    print(f"Error: {e}")
    
    # Try to get more details if it's an HTTP error
    if hasattr(e, 'response') and hasattr(e.response, 'text'):
        try:
            error_details = json.loads(e.response.text)
            print(f"Error details: {json.dumps(error_details, indent=2)}")
        except:
            print(f"Raw error response: {e.response.text}")

