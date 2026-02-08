# Task Master

A simple and elegant task management web application built with Flask and PostgreSQL.

## Features

- **Create Tasks** - Add tasks with title, category, and due date
- **Categories** - Organize tasks by Work, Personal, School, or Urgent
- **Mark Complete** - Check off tasks when done
- **Delete Tasks** - Remove tasks you no longer need
- **Browser Notifications** - Get reminders 5 minutes before and at due time
- **Responsive Design** - Works on desktop and mobile

## Tech Stack

- **Backend**: Python, Flask
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Render

## Setup

### Prerequisites

- Python 3.x
- PostgreSQL

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/SaiSriSatvic2005/task-manager.git
   cd task-manager
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL database:
   - Create a database named `todo_app`
   - Update credentials in `app.py` if needed

4. Run the application:
   ```bash
   python app.py
   ```

5. Open http://localhost:5000 in your browser

### Deployment on Render

1. Create a PostgreSQL database on Render
2. Create a Web Service connected to your GitHub repo
3. Set environment variable:
   - `DATABASE_URL`: Your Render PostgreSQL connection string
4. Deploy!

## Project Structure

```
flask_todo/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── static/
│   └── style.css       # Stylesheet
└── templates/
    └── index.html      # Main page template
```

## Live Demo

https://task-manager-aza0.onrender.com

## License

MIT
