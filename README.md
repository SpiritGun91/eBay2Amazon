# eBay2Amazon

Import eBay listings to Amazon

## Overview

The `eBay2Amazon` project is designed to help users import eBay listings and generate a comprehensive CSV file that can be used for various purposes, including importing to Amazon. The script parses eBay XML data and extracts detailed item information. So far it doesn't import to Amazon yet, but it will.

## Features

- Extracts detailed item information from eBay XML data.
- Generates a CSV file with comprehensive item details.
- Handles missing elements gracefully to avoid runtime errors.
- Strips HTML tags from item descriptions.
- Supports additional fields including:
  - Brand
  - BuyItNowPrice
  - ConvertedStartPrice
  - ConvertedCurrentPrice
  - PostalCode
  - FeedbackScore
  - PositiveFeedbackPercent
  - ListingStatus
  - ReturnsAccepted
  - DispatchTimeMax
  - WeightMajor
  - WeightMinor

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/eBay2Amazon.git
   cd eBay2Amazon
   ```

2. Ensure you have Python installed. This script requires Python 3.x.

## Usage

1. Install the required Python packages:

   ```sh
   pip install -r requirements.txt
   ```

2. Create a `config.ini` file in the project directory with your eBay API token. Here is an example of what the `config.ini` file should look like:

   ```ini
   [ebay]
   api_token = YOUR_EBAY_API_TOKEN
   ```

3. Create a file named `items.txt` in the project directory and list the eBay item numbers you want to fetch, one per line. Here is an example of what the `items.txt` file should look like:

   ```plaintext
   1234567890
   0987654321
   1122334455
   ```

4. Run the `ebay.py` script to fetch item details:

   ```sh
   python ebay.py
   ```

5. This places your eBay XML data in a file named `output.txt` in the project directory.

6. Run the script:

   ```sh
   python table.py
   ```

7. The script will generate a `table.csv` file with the extracted item details.

## Example

Example structure of `output.txt`:

```plaintext
Details for Item 1
<xml>...</xml>
Details for Item 2
<xml>...</xml>
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue on GitHub or contact the repository owner.
