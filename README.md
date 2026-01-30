# Crux - Climbing Training Planner

Crux is a local web application built with Django and Bootstrap 5 designed to help climbers plan and track their training sessions. It features a horizontal calendar view, custom activity types, and progress tracking.

## Features

- **Training Plans:** Create and manage customized training plans with specific start and end dates.
- **Interactive Calendar:** Scrollable horizontal calendar view to visualize your entire training block.
- **Custom Activities:** Define your own activities (e.g., Climbing, Rest, Kilter Board, Yoga) with custom colors.
- **Session Tracking:** Mark sessions as complete and add notes.
- **Progress Monitoring:** Automatically tracks if you are ahead or behind schedule.

## Getting Started

### Prerequisites

- Python 3.12+
- `uv` (Universal Python Package/Project Manager)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd crux
    ```

2.  **Install dependencies:**
    ```bash
    uv sync
    ```

3.  **Run Migrations:**
    ```bash
    uv run python manage.py migrate
    ```

4.  **Create Superuser (Optional, for admin access):**
    ```bash
    uv run python manage.py createsuperuser
    ```

### Running the Application

1.  **Start the development server:**
    ```bash
    uv run python manage.py runserver
    ```

2.  **Access the app:**
    Open your browser and navigate to `http://127.0.0.1:8000`.

## Usage

1.  **Create Activity Types:** Go to "Activities" and define your training types (e.g., "Strength", "Endurance").
2.  **Create a Plan:** Click "Create New Plan" and set your dates.
3.  **Plan Sessions:** (Feature in progress: Click on calendar cells to add sessions).
4.  **Track:** Mark sessions as done to see your "Ahead/Behind" status update.

## Development Status

- **Backend:** Django 6.0, SQLite.
- **Frontend:** Bootstrap 5, Django Templates.
- **CI/CD:** GitHub Actions configured.
