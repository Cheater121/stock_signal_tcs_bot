# Stock Price Tracker (stock_signal_tcs_bot) 
This is MVP for my friend. 

 






This project is a stock price tracker that uses the Tinkoff API and the Telegram Bot API to provide real-time updates on stock prices and send notifications when certain price thresholds are met.

Moving Average: 20-50-100-200 days. High/low: 1-7-30 days.


## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

- Python 3.x
- Tinkoff API token
- Telegram Bot token

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/Cheater121/stock_signal_tcs_bot.git
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root directory and add the following variables:

   ```
   TCS_TOKEN=YOUR_TINKOFF_API_TOKEN
   TG_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
   ```

## Usage

1. Start the bot by running the `stock_signal_tcs_bot.py` script:

   ```
   python stock_signal_tcs_bot.py
   ```

2. Open your Telegram app and search for the bot username. Send the `/start` command to the bot to start receiving price updates.

3. Use the available commands to interact with the bot and manage your notifications.

## Commands

- `/start` - Start the bot and begin receiving price updates.
- `/stop` - Stop receiving price updates and exit the bot.
- `/status` - Check the status of the bot and whether it's currently active.
- `/stocks` - Get a list of supported stock tickers.
- `/help` - Display the available commands and their usage.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Feel free to customize and modify the README.md according to your project's specific details and requirements.
