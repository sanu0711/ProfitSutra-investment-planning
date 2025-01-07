# ProfitSutra - Investment Planning with Gen AI Bot

## Description

The "Investment Planning with Gen AI Bot" is a web application developed using Django that assists users in planning their investments. The bot understands the customer's financial status and goals through a detailed questionnaire and provides personalized investment strategies. The app also offers an interactive dashboard to track the performance of investments in real-time.

## Key Features

- **User-friendly Questionnaire**: A dynamic form that helps profile the customer's financial status and investment goals.
- **AI-Driven Investment Advice**: The bot analyzes user inputs and generates personalized investment strategies.
- **Integration with Financial Data Sources**: Fetches real-time financial data to offer accurate investment recommendations.
- **Interactive Dashboard**: Allows users to track and visualize their investment performance.

## Technologies Used

- **Django**: Backend framework for developing the web application.
- **Python**: Primary programming language for the backend.
- **HTML/CSS/JavaScript**: For frontend development.
- **Bootstrap**: Used for responsive web design.
- **AI Model**: Integration of Gen AI  to analyze financial data and provide investment recommendations.
- **Financial Data API**: Used to integrate real-time market data.

## Getting Started

Follow these steps to set up and run the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/sanu0711/ProfitSutra-investment-planning.git
   ```

2. Navigate to the project directory:
```bash
   cd ProfitSutra-investment-planning
   ```

3. Create and activate a virtual environment:
```bash
   python -m venv venv
   venv/Scripts/activate
   ```

4. Install project dependencies:
```bash
   pip install -r requirements.txt
   ```
5. Set up the database migrations:
```bash
    python manage.py makemigrations
    python manage.py migrate
   ```
6. Run the development server:
```bash
   python manage.py runserver
   ```


