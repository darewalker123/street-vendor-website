# Street Vendor Connect

**Street Vendor Connect** is a Flask-based web application designed to connect street vendors with suppliers of fresh raw materials. Vendors can register to list and manage their materials, while consumers can browse and search for materials and view vendor profiles.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Customizations](#customizations)
- [File Overview](#file-overview)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- Vendor and Consumer registration & login with role-based access.
- Vendor dashboard: Add, edit, delete raw materials.
- Consumer dashboard: Browse, search materials by category.
- View vendor profile with contact details and material listings.
- Password secured with hashing (bcrypt).
- Responsive, modern UI with images and gradient styling.
- Image icons by material category.
- Session-based authentication and navigation.

---

## Project Structure

```
street-vendor-app/
│
├── app.py                  # Main Flask application routes and logic
├── models.py               # SQLAlchemy ORM models (User, RawMaterial)
│
├── /templates              # HTML templates (Jinja2)
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── vendor_dashboard.html
│   ├── vendor_add_edit.html
│   ├── consumer_dashboard.html
│   ├── vendor_profile.html
│
├── /static                 # Static files (CSS, images, icons)
│   ├── style.css           # Main stylesheet with modern UI improvements
│   ├── vendor-market.jpg   # Hero image displayed on homepage
│   └── /icons              # Folder for raw material category icons (png/svg)
│       ├── vegetable.png
│       ├── fruit.png
│       └── ...
│
└── vendor.db               # SQLite database (auto-created on first run)
```

---

## Technologies Used

- Python 3.x
- Flask
- Flask-Bcrypt
- SQLAlchemy (ORM)
- SQLite (lightweight relational database)
- HTML5, CSS3 (modern styling with gradients and responsive design)
- Jinja2 templating engine

---

## Setup and Installation

1. **Clone the repository:**

   ```
   git clone https://github.com/yourusername/street-vendor-connect.git
   cd street-vendor-connect
   ```

2. **(Optional) Create and activate a virtual environment:**

   ```
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies:**

   ```
   pip install -r requirements.txt
   ```

   *(If you don't have a `requirements.txt`, install manually:)*

   ```
   pip install flask flask-bcrypt flask-sqlalchemy
   ```

4. **Run the Flask application:**

   ```
   flask run
   ```

   Or if you use `app.py` directly:

   ```
   python app.py
   ```

5. **Open your browser:**

   Navigate to `http://127.0.0.1:5000` to view the app.

---

## Usage

- Register as a **Vendor** or **Consumer**.
- Vendors can add, edit, delete raw materials via their dashboard.
- Consumers can browse and search for raw materials, then view supplier profiles.
- Use the navigation bar to access `Login`, `Register`, `Browse`, and dashboards.
- Passwords are hashed for security.
- The UI is designed to be responsive and visually appealing with category icons and hero images.

---

## Customizations

- To update the hero image, replace `/static/vendor-market.jpg`.
- Add or update category icons in `/static/icons/` using PNGs named according to categories (e.g., `vegetable.png`).
- Adjust styling in `/static/style.css` to fit your branding.
- No backend code changes are necessary to modify frontend visuals.

---

## File Overview

- `app.py`: Flask routes and app setup.
- `models.py`: Database models.
- `templates/`: Jinja2 HTML templates for all pages.
- `static/style.css`: Styling with modern gradients, button hover effects, and responsive layout.
- `static/vendor-market.jpg`: Homepage hero image.
- `static/icons/`: Icons representing material categories.

---

## Deployment

For deploying your Flask app with Python backend, free hosting options include:

- [PythonAnywhere](https://www.pythonanywhere.com)  
- [Render](https://render.com)  
- [Railway](https://railway.app)  

These provide easy setups for Flask apps with free tiers for small projects.

If you intend to deploy, ensure:

- Environment variables for SECRET_KEY and database URI are set securely.
- Static file serving and debug mode are configured appropriately.
- Consider adding SSL, production server (e.g., Gunicorn), and domain setup for production readiness.

---

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to fork the repo and submit pull requests.

---

## License

This project is open source and available under the MIT License.

---

**Thank you for using Street Vendor Connect!**

If you have any questions or need assistance, please open an issue or contact the maintainer.
```

### Option 2: I can create a ZIP file with README.md inside and provide a download link here

If you want, just say **“Yes, please provide a ZIP”** and I will prepare it for you.

If you want me to help more with whichever method you prefer, just let me know!
