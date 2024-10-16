import aiohttp
import asyncio
import configparser

# Read the IAF_TOKEN from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
IAF_TOKEN = config['eBayAPI']['IAF_TOKEN']

EBAY_API_ENDPOINT = "https://api.ebay.com/ws/api.dll"

async def fetch_item_details(session, item_number):
    headers = {
        "X-EBAY-API-SITEID": "0",
        "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
        "X-EBAY-API-CALL-NAME": "GetItem",
        "X-EBAY-API-IAF-TOKEN": IAF_TOKEN,
        "Content-Type": "text/xml",
    }
    
    xml_payload = f"""<?xml version="1.0" encoding="utf-8"?>
    <GetItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
        <ErrorLanguage>en_US</ErrorLanguage>
        <WarningLevel>High</WarningLevel>
        <ItemID>{item_number}</ItemID>
        <DetailLevel>ReturnAll</DetailLevel>
    </GetItemRequest>"""
    
    async with session.post(EBAY_API_ENDPOINT, headers=headers, data=xml_payload) as response:
        if response.status == 200:
            return await response.text()
        else:
            print(f"Error fetching item {item_number}: {response.status} - {await response.text()}")
            return None

async def main():
    async with aiohttp.ClientSession() as session:
        with open('items.txt', 'r') as file:
            item_numbers = [line.strip() for line in file.readlines()]

        tasks = [fetch_item_details(session, item_number) for item_number in item_numbers]
        item_details_list = await asyncio.gather(*tasks)

        with open('output.txt', 'w') as output_file:
            for item_number, item_details in zip(item_numbers, item_details_list):
                if item_details:
                    output_file.write(f"Details for {item_number}:\n{item_details}\n\n")

if __name__ == "__main__":
    asyncio.run(main())
