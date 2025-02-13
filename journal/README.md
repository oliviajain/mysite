# One Question a Day

This is a simple web application that asks users one question a day and records their answers. Users can view their responses and log out of the application.

## Features
- User-friendly interface with a modern design
- Responsive layout using W3.CSS
- Records user answers and displays them
- Navigation bar with links to home, responses, and logout

## Technologies Used
- Flask (Python web framework)
- HTML
- CSS (W3.CSS and custom styles)
- Google Fonts (Lato)
- Font Awesome (icons)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/oliviajain/journal.git
    cd journal
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask application:
    ```bash
    flask run
    ```

## Usage
- Navigate to `http://127.0.0.1:5000/` in your web browser.
- Enter your name to start answering questions.
- View your responses by clicking on the "Responses" tab in the navigation bar.
- Log out by clicking on the "Logout" tab in the navigation bar.
