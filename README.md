# CFP Tracker

A web application for tracking and managing Call for Proposals (CFPs) from various sources. The application allows users to view, filter, and get notified about upcoming CFPs through Slack.

## Features

- Aggregate CFPs from multiple sources
- Sort and filter CFPs by:
  - Closing date
  - Location
  - Target audience
  - Event type
- Slack integration for CFP notifications
- Modern web interface for easy management

## Tech Stack

- Backend: Python FastAPI
- Database: PostgreSQL with SQLAlchemy ORM
- Frontend: React with TypeScript
- Authentication: JWT
- Task Queue: Celery for background jobs
- CFP Scraping: BeautifulSoup4

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/webchick/vibe-coding-cfp.git
   cd vibe-coding-cfp
   ```

2. Install dependencies:
   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt

   # Frontend
   cd ../frontend
   npm install
   ```

3. Set up environment variables:
   ```bash
   # From the backend directory
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Initialize the database:
   ```bash
   # From the backend directory
   python -m init_db
   ```

5. Run the application:
   ```bash
   # From the project root directory
   ./run.sh
   ```

## Configuration

The following environment variables are required in `backend/.env`:

- `DATABASE_URL`: PostgreSQL connection string
- `SLACK_BOT_TOKEN`: Slack bot user OAuth token
- `SLACK_CHANNEL_ID`: Default Slack channel for notifications
- `JWT_SECRET`: Secret key for JWT token generation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
