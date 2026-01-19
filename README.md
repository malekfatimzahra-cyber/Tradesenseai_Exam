# TradeSense AI - Exam Project

## Project Structure

This repository is organized as follows:

- **/backend**: Flask Application (API, Database Models, Logic)
  - `app.py`: Main application entry point.
  - `models.py`: Database models (SQLAlchemy).
  - `requirements.txt`: Python dependencies.

- **/frontend**: React Application (Vite, TypeScript, TailwindCSS)
  - `App.tsx`: Main React component.
  - `components/`: UI Components.
  - `store.ts`: State management (Zustand).

- **database.sql**: Full MySQL database export (Schema + Data).

## Setup Instructions

### Backend
1. Navigate to `/backend`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the server: `python app.py`.

### Frontend
1. Navigate to `/frontend`.
2. Install dependencies: `npm install`.
3. Run the development server: `npm run dev`.

### Database
- Import `database.sql` into your MySQL server to restore the full project state.
