Social Media Platform 🌐

A Django-based social media web application that allows users to create accounts, make posts with captions and images, follow/unfollow others, like posts, and add comments — similar to platforms like Instagram or Twitter.

🚀 Features

- 🔐 User authentication (signup, login, logout)
- 👤 Public profiles with bio, location, birthdate, followers/following
- 📝 Create/edit/delete posts with image uploads
- ❤️ Like/unlike posts
- 💬 Add comments to posts
- ➕ Follow/unfollow users
- 📷 Profile picture support
- ⚙️ Responsive UI and interactive feedback (using CSS & JavaScript)

🛠️ Tech Stack

- **Backend**: Django 4.2
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite3 (default for Django)
- **Media Handling**: Django media storage
- **Other**: Django Custom User Model, Django Forms

📁 Project Structure

social_media_platform/
│
├── users/ # Custom user model, profile, authentication views
├── posts/ # Post creation, like/unlike logic
├── interactions/ # Follows, comments
├── templates/ # HTML templates
├── media/ # Uploaded media files
├── static/ # Static files (CSS, JS)
├── social_media_platform/ # Project settings and URLs
├── db.sqlite3 # SQLite database
└── manage.py # Django CLI entry point


⚙️ Installation

1. Clone the repo

   git clone https://github.com/your-username/social_media_platform.git
   cd social_media_platform

2. Create and activate a virtual environment

On macOS/Linux:

python3 -m venv venv
source venv/bin/activate

On Windows:

python -m venv venv
venv\Scripts\activate

3. Install required dependencies
pip install -r requirements.txt

4. Apply migrations

python manage.py migrate

5. Create superuser (admin account)

python manage.py createsuperuser

6. Run the development server

python manage.py runserver

7. Visit the app in your browser

Visit http://127.0.0.1:8000/users/login/ to start using the app!

