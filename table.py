import xml.etree.ElementTree as ET
import csv
import re

def strip_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def parse_item_details(xml_data):
    root = ET.fromstring(xml_data)
    ns = {'ebay': 'urn:ebay:apis:eBLBaseComponents'}
    
    item_id = root.find('ebay:Item/ebay:ItemID', ns).text
    title = root.find('ebay:Item/ebay:Title', ns).text
    price = root.find('ebay:Item/ebay:StartPrice', ns).attrib['currencyID'] + " " + root.find('ebay:Item/ebay:StartPrice', ns).text
    location = root.find('ebay:Item/ebay:Location', ns).text
    seller = root.find('ebay:Item/ebay:Seller/ebay:UserID', ns).text
    listing_url = root.find('ebay:Item/ebay:ListingDetails/ebay:ViewItemURL', ns).text
    quantity = root.find('ebay:Item/ebay:Quantity', ns).text
    description = strip_html_tags(root.find('ebay:Item/ebay:Description', ns).text)
    condition = root.find('ebay:Item/ebay:ConditionDisplayName', ns).text
    condition_id = root.find('ebay:Item/ebay:ConditionID', ns).text
    category = root.find('ebay:Item/ebay:PrimaryCategory/ebay:CategoryName', ns).text
    start_time = root.find('ebay:Item/ebay:ListingDetails/ebay:StartTime', ns).text
    end_time = root.find('ebay:Item/ebay:ListingDetails/ebay:EndTime', ns).text
    
    shipping_cost_elem = root.find('ebay:Item/ebay:ShippingDetails/ebay:ShippingServiceOptions/ebay:ShippingServiceCost', ns)
    shipping_cost = shipping_cost_elem.text if shipping_cost_elem is not None else 'N/A'
    
    item_specifics = root.find('ebay:Item/ebay:ItemSpecifics', ns)
    specifics = []
    if item_specifics:
        for specific in item_specifics.findall('ebay:NameValueList', ns):
            name = specific.find('ebay:Name', ns).text
            value = specific.find('ebay:Value', ns).text
            specifics.append(f"{name}: {value}")
    specifics_str = '; '.join(specifics)
    
    picture_urls = [pic.text for pic in root.findall('ebay:Item/ebay:PictureDetails/ebay:PictureURL', ns)]
    picture_urls_str = ', '.join(picture_urls)
    
    brand_elem = root.find('ebay:Item/ebay:ProductListingDetails/ebay:BrandMPN/ebay:Brand', ns)
    brand = brand_elem.text if brand_elem is not None else 'N/A'
    
    return {
        'ItemID': item_id,
        'Title': title,
        'Price': price,
        'Location': location,
        'Seller': seller,
        'ListingURL': listing_url,
        'Quantity': quantity,
        'Description': description,
        'Condition': condition,
        'ConditionID': condition_id,
        'Category': category,
        'StartTime': start_time,
        'EndTime': end_time,
        'ShippingCost': shipping_cost,
        'ItemSpecifics': specifics_str,
        'PictureURLs': picture_urls_str,
        'Brand': brand
    }

def main():
    with open('output.txt', 'r') as file:
        data = file.read().split('Details for ')[1:]  # Split by 'Details for ' and ignore the first empty split

    items = []
    for item_data in data:
        item_number, xml_data = item_data.split('\n', 1)
        item_details = parse_item_details(xml_data)
        items.append(item_details)

    with open('table.csv', 'w', newline='') as csvfile:
        fieldnames = [
            'ItemID', 'Title', 'Price', 'Location', 'Seller', 'ListingURL', 'Quantity', 
            'Description', 'Condition', 'ConditionID', 'Category', 'StartTime', 'EndTime', 
            'ShippingCost', 'ItemSpecifics', 'PictureURLs', 'Brand'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in items:
            writer.writerow(item)

if __name__ == "__main__":
    main()