# 🌍 Crowd-Funding Web App (Backend with Django)

> Backend-only project built using Django to support fundraising campaigns in Egypt.

![Made with Django](https://img.shields.io/badge/Made%20with-Django-green)
![Project Type](https://img.shields.io/badge/Type-Team%20Project-blueviolet)
![Status](https://img.shields.io/badge/Version-1.0-success)

---

## 🧑‍💻 Developed By

- Moaz Ahmed sayed
- Mahmoud Samir Oraby
- Ebram Rasmy Ayad
- Abdullah Ayman Mohamed
- Girgis Kelliny Girgis Abdelmalak

---

## 🎯 Project Goal

To build a backend system that enables users to:

- Create fundraising projects
- Donate to campaigns
- Rate & comment
- Manage their profile
- And more...

> Inspired by platforms like [GoFundMe](https://www.gofundme.com) & [Kickstarter](https://www.kickstarter.com)

---

## 💡 Features Overview

### 🔐 Authentication

- Email verification (expires in 24 hours)
- Egyptian mobile number validation
- Login, register, reset password
- Facebook login (bonus)

### 👤 Profile System

- View/edit profile, view projects & donations
- Delete account with confirmation & password

### 📦 Projects

- Title, details, tags, target, category
- Upload multiple images
- Comments + replies
- Rating + reporting
- Similar projects recommendation

### 🏠 Homepage Logic

- Top 5 rated projects
- Featured/latest projects
- Categories + search by title/tag

---

## 🛠️ Tech Stack

- **Framework:** Django
- **Language:** Python
- **Database:** PostgreSQL 
- **Email:** SMTP (Gmail)
- **Auth:** Django Auth System

---

## 🚀 Getting Started (Locally)

```bash
# Clone the repo
git clone https://github.com/MoazAhmedS/fundme.git

# Navigate into the project
cd fundme

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Run server
python manage.py runserver
```

---

## 🔧 Environment Setup

This project uses environment variables to store sensitive configuration such as database credentials and email settings.

### 1. Create a `.env` file

In the root of the project (where `manage.py` is), create a `.env` file with the following content:

```env
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host  # e.g., localhost
DB_PORT=postgres_port_number

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

---

## 🔧 Facebook Login Setup

This project supports Facebook login. Follow the steps below to make it work:

### 1. Create a Facebook App
1. Go to the [Facebook Developers](https://developers.facebook.com/) page.
2. Create a new app.
3. Navigate to **Settings > Basic** and add your app's domain.
4. Under **Products**, add **Facebook Login**.
5. Configure the Site URL.

### 1. Create a Superuser (Admin)

To access Django admin where you’ll configure Facebook:
```bash
python manage.py createsuperuser
```

### 2. Configure Facebook Login in Django Admin
1. Go to Django Admin (`http://localhost:8000/admin`).
2. Navigate to **Social Accounts > Social Applications**.
3. Click on **Sites** and ensure your site is added (e.g., `http://localhost:8000`).
4. Click on **Add Social Application**.
5. Add a new Social Application:
   - Name: Facebook
   - Provider: Facebook
   - Client ID: Your Facebook App ID
   - Secret Key: Your Facebook App Secret
   - Sites: Add your site (e.g., `http://localhost:8000`)
6. Save the application.

### 3. Done!
Now you can use Facebook login in your application. Users can log in using their Facebook accounts, and the app will handle authentication seamlessly.