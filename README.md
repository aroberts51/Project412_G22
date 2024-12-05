# **Project412_G22**

A Django-based web application for managing a personalized game list, connecting with other gamers, and exploring game feeds. This project is designed to provide users with an intuitive interface for managing their game preferences and social connections.

---

## **Features**

### **User Profile**
- Upload and display profile pictures (with a default fallback image).
- Manage a personalized game list with drag-and-drop reordering.
- Edit account information such as username, email, and password.

<img width="928" alt="Screenshot 2024-11-28 at 9 44 35 AM" src="https://github.com/user-attachments/assets/2e9114f2-e96c-4130-b9b6-066a92e52d28">


### **Game Feed**
- View games shared by users you follow.
- Explore genres and descriptions of games in an interactive feed format.

<img width="928" alt="Screenshot 2024-11-28 at 9 45 07 AM" src="https://github.com/user-attachments/assets/33264276-b8bc-4ced-8985-9284351ae267">


### **Followers and Following**
- View your followers and following lists in visually appealing card formats.
- Unfollow users or follow back users who follow you.

<img width="929" alt="Screenshot 2024-11-28 at 9 45 23 AM" src="https://github.com/user-attachments/assets/87e56375-8c30-4734-9956-c30b600c4040">

<img width="927" alt="Screenshot 2024-11-28 at 9 45 40 AM" src="https://github.com/user-attachments/assets/f72e23d9-ae99-49ab-9e83-fb1a31d0bf8e">


### **Game Search**
- Search for games with a search bar.
- Navigate to a detailed game information page.
- Add games to your personal list directly from the search results.

<img width="929" alt="Screenshot 2024-11-28 at 9 45 58 AM" src="https://github.com/user-attachments/assets/6312c210-b92f-4cd4-9eaa-3dca2aec6c5e">


---

## **Tech Used**

- **Backend**: Django 5.1.3 (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL
- **Static Files**: Managed with Django's `collectstatic`

---

## **Installation Steps**

### Step 1: Clone the Repository
```bash
git clone https://github.com/aroberts51/Project412_G22.git
cd Project412_G22
```

  
### Step 2
```bash
  python3 -m venv venv
  source venv/bin/activate
```

### Step 3
```bash
  pip install -r requirements.txt
```

### Step 4
```bash
  python manage.py migrate
```

### Step 5
```bash
  python manage.py runserver
```

### Step 6
```bash
  http://127.0.0.1:8000/
```

This code is a collaborated effort of ASU students of Group 22 in the CSE412 course.
