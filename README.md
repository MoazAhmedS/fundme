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
