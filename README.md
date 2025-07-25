# 🍽️ ClickToEat – Traditional Food Ordering Web Application

**ClickToEat** is a modern, responsive, full-stack Django web application designed for ordering authentic, traditional food online.
It provides a seamless experience from browsing food menus to placing orders, with a secure user system and an intuitive admin interface for restaurant management.

---

## 📌 Key Features

- 🔐 **User Authentication**
  - Sign Up, Login, Logout
  - Session-based secure access

- 🧾 **Dynamic Food Menu**
  - Categories and filtering
  - Live search bar
  - Menu cards with images and prices

- 🛒 **Cart System**
  - Add/remove items with AJAX (no page reload)
  - Cart summary and total cost

- 🚚 **Order Placement Flow**
  - Address entry form
  - Dummy payment simulation
  - Order confirmation with success page
  - Cart auto-clear after order

- 📦 **My Orders Section**
  - View all past orders
  - Track order status

- 🛠️ **Admin Panel**
  - Manage categories, food items, orders, users

- 💌 **Contact Form**
  - Stores messages in database
  - Sends confirmation auto-reply to user
  - Sends formatted HTML email to admin

- 🌙 **Dark Mode Support**
  - Toggle light/dark themes with persistence

- 💡 **Responsive Design**
  - Fully mobile-friendly using Tailwind CSS (CDN)

---

## 🛠️ Tech Stack

| Technology      | Purpose                       |
|----------------|-------------------------------|
| **Python**      | Backend language              |
| **Django**      | Web framework (MVC/MVT)       |
| **SQLite/PostgreSQL** | Database                    |
| **HTML/CSS**    | Page structure & styling      |
| **Tailwind CSS**| Responsive UI styling         |
| **JavaScript**  | Interactivity (AJAX/cart)     |
| **jQuery** (optional) | DOM updates for AJAX       |
| **Bootstrap Icons** | Iconography                 |

---

## ⚙️ Installation (Local Development)

1. **Clone the project**
```bash
git clone https://github.com/roshan7600/clicktoeat.git
cd clicktoeat

# 📁 Step 1: Set up virtual environment
python -m venv venv
source venv/bin/activate       # For Windows: venv\Scripts\activate

# 📦 Step 2: Install dependencies
pip install -r requirements.txt

# 🛠️ Step 3: Apply database migrations
python manage.py migrate

# 👤 Step 4: Create admin superuser
python manage.py createsuperuser

# 🚀 Step 5: Run the development server
python manage.py runserver

🌐 Visit the app at:
http://127.0.0.1:8000

## 📸 Screenshots

### 🏠 Home Page
![Home Page](screenshots/home_page.png)

### 🍽️ Menu Page
![Menu Page](screenshots/menu_page.png)

### 🛒 Cart Page
![Cart Page](screenshots/cart_page.png)

### 💳 Dummy Payment Page
![Dummy Payment](screenshots/dummy_payment.png)

### ✅ Order Placed Successfully
![Order Success](screenshots/order_success.png)

### 📦 My Orders Page
![My Orders](screenshots/my_orders.png)

### 🧾 Order History (Admin/User View)
![Order History](screenshots/order_history.png)

### 🙍 Profile Page
![Profile](screenshots/profile.png)

### 📬 Mail Sent Confirmation
![Mail Sending](screenshots/mail_sent.png)





