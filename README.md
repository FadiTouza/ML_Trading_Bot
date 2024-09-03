# ML Trading Bot

## Description

The **ML Trading Bot** is a machine learning-driven trading bot that utilizes predictive algorithms and the lumibot API to analyze financial market data and execute trades based on predefined strategies. The project is designed to automate trading processes, optimize decision-making, and improve trading performance by leveraging data-driven insights.

This project is suitable for developers, data scientists, and financial enthusiasts who want to explore the intersection of machine learning and trading. The bot is flexible and can be adapted to various trading strategies and markets.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Contributing](#contributing)
4. [Coming Features](#coming-features)
5. [License](#license)
6. [Authors](#authors)
7. [Acknowledgments](#acknowledgments)

## Installation

### Prerequisites
Before you begin, ensure you have the following installed on your system:
- **Python 3.x**: The programming language used for this project.
- **pip**: Python package manager.
- **Git**: Version control system.

### Installation Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/FadiTouza/ML_Trading_Bot.git
    cd ML_Trading_Bot
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Once the installation is complete, you can start using the ML Trading Bot. Below is an example of how to run the bot:

1. **Configuration**: Set up your trading parameters and API keys in the `creds.py` file.
   
2. **Running the Bot**: Currently the bot only supports backtesting using historical data to validate the strategy before live trading. To do this, run:
    ```bash
    python trading_bot.py
    ```

4. **Examples**:
   - **Basic Trading**: The bot executes trades based on the model's predictions.
   - **Advanced Configuration**: Customize the trading strategy and risk management settings.

## Contributing

Contributions are welcome! If you'd like to contribute to the ML Trading Bot, please follow these guidelines:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## Coming Features
1. Find better news sources for the model through webscraping or other backtesting tools
2. Improve the pretty crude strategy on every iteration
3. Write code that documents the result of each trade to get better evulation on how good the model predictions are

## License

This project is licensed under the MIT License

## Authors

- **Fadi Touza** - [GitHub Profile](https://github.com/FadiTouza)

## Acknowledgments

- Special thanks to the open-source community and various contributors whose work made this project possible.