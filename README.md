```
 Bethany Harvest Collaboration Lost Book
```
This Flask web application that enables anonymous communication between people who lost books and those who found them.

## Features

- *Public Notice Board*: Browse all lost book reports without logging in
- *User Accounts*: Register and login to post notices
- *Anonymous Messaging*: Contact book owners without revealing your identity
- *Conversation Management*: Owners can view and reply to all anonymous inquiries
- *Session-Based Anonymity*: Each finder gets a unique anonymous ID per conversation

## Tech Stack

- *Backend*: Python Flask
- *Storage*: JSON files (users, notices, conversations)
- *Authentication*: Session-based with secure cookies
- *Frontend*: HTML/CSS with Jinja2 templates

## Installation


## Clone the repository
```bash
cd lostbook
```

## Install dependencies
```
pip install flask
```
## Run the application
```
python app.py
```

## How It Works

1. **Post a Notice**: Register an account and describe your lost book
2. **Two-Way Chat**: Communicate back and forth while the finder remains anonymous
3. **Arrange Return**: Coordinate book return without awkward confrontations




## Use Case

Perfect for schools, libraries, and communities where books frequently get misplaced or accidentally taken. Encourages honest returns by removing the fear of being accused of theft.

## Privacy

- Finders remain anonymous unless they choose to reveal themselves
- Anonymous IDs are cryptographically generated and session-based
- Only book owners can view conversations related to their notices
