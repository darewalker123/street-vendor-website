from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key_change_this_in_production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vendor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False) 
    role = db.Column(db.String(10), nullable=False)  # 'vendor' or 'consumer'
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))

class RawMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    unit = db.Column(db.String(20), default='kg')

    user = db.relationship('User', backref=db.backref('materials', lazy=True))

# Create DB tables on app start
with app.app_context():
    db.create_all()

# Routes

@app.route('/')
def home():
    materials = RawMaterial.query.limit(6).all()
    return render_template('home.html', featured_materials=materials)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        phone = request.form.get('phone')
        address = request.form.get('address')

        if not (name and email and password and role):
            flash('Please fill all required fields.', 'error')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, email=email, password=hashed_pw, role=role, phone=phone, address=address)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Please enter both email and password.', 'error')
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            session['name'] = user.name

            if user.role == 'vendor':
                return redirect(url_for('vendor_dashboard'))
            else:
                return redirect(url_for('consumer_dashboard'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# Vendor routes

@app.route('/vendor/dashboard')
def vendor_dashboard():
    if 'user_id' not in session or session.get('role') != 'vendor':
        flash('Please log in as a vendor first.', 'error')
        return redirect(url_for('login'))

    materials = RawMaterial.query.filter_by(user_id=session['user_id']).all()
    return render_template('vendor_dashboard.html', materials=materials)

@app.route('/vendor/add', methods=['GET', 'POST'])
def vendor_add():
    if 'user_id' not in session or session.get('role') != 'vendor':
        flash('Please log in as a vendor first.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        price = request.form.get('price')
        qty = request.form.get('qty')
        description = request.form.get('description')
        unit = request.form.get('unit', 'kg')

        # Basic validation
        if not (name and category and price and qty):
            flash('Please fill all required fields.', 'error')
            return redirect(url_for('vendor_add'))

        try:
            price = float(price)
            qty = int(qty)
        except ValueError:
            flash('Invalid price or quantity.', 'error')
            return redirect(url_for('vendor_add'))

        new_material = RawMaterial(user_id=session['user_id'], name=name, category=category, price=price,
                                   qty=qty, description=description, unit=unit)
        db.session.add(new_material)
        db.session.commit()
        flash('Material added successfully.', 'success')
        return redirect(url_for('vendor_dashboard'))

    return render_template('vendor_add_edit.html', mode='add')

@app.route('/vendor/edit/<int:material_id>', methods=['GET', 'POST'])
def vendor_edit(material_id):
    if 'user_id' not in session or session.get('role') != 'vendor':
        flash('Please log in as a vendor first.', 'error')
        return redirect(url_for('login'))

    material = RawMaterial.query.get_or_404(material_id)
    if material.user_id != session['user_id']:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('vendor_dashboard'))

    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        price = request.form.get('price')
        qty = request.form.get('qty')
        description = request.form.get('description')
        unit = request.form.get('unit', 'kg')

        if not (name and category and price and qty):
            flash('Please fill all required fields.', 'error')
            return redirect(url_for('vendor_edit', material_id=material_id))

        try:
            price = float(price)
            qty = int(qty)
        except ValueError:
            flash('Invalid price or quantity.', 'error')
            return redirect(url_for('vendor_edit', material_id=material_id))

        material.name = name
        material.category = category
        material.price = price
        material.qty = qty
        material.description = description
        material.unit = unit
        db.session.commit()
        flash('Material updated successfully.', 'success')
        return redirect(url_for('vendor_dashboard'))

    return render_template('vendor_add_edit.html', material=material, mode='edit')

@app.route('/vendor/delete/<int:material_id>')
def vendor_delete(material_id):
    if 'user_id' not in session or session.get('role') != 'vendor':
        flash('Please log in as a vendor first.', 'error')
        return redirect(url_for('login'))

    material = RawMaterial.query.get_or_404(material_id)
    if material.user_id != session['user_id']:
        flash('Unauthorized.', 'error')
        return redirect(url_for('vendor_dashboard'))

    db.session.delete(material)
    db.session.commit()
    flash('Material deleted.', 'success')
    return redirect(url_for('vendor_dashboard'))

# Consumer routes

@app.route('/consumer/dashboard')
def consumer_dashboard():
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '')

    query = RawMaterial.query
    if search:
        query = query.filter(RawMaterial.name.ilike(f'%{search}%'))
    if category:
        query = query.filter(RawMaterial.category == category)

    materials = query.order_by(RawMaterial.name).all()
    categories = [c[0] for c in db.session.query(RawMaterial.category).distinct()]

    return render_template('consumer_dashboard.html', materials=materials, categories=categories,
                           search=search, selected_category=category)

@app.route('/vendor/profile/<int:vendor_id>')
def vendor_profile(vendor_id):
    vendor = User.query.filter_by(id=vendor_id, role='vendor').first_or_404()
    materials = RawMaterial.query.filter_by(user_id=vendor.id).all()
    return render_template('vendor_profile.html', vendor=vendor, materials=materials)

if __name__ == '__main__':
    app.run(debug=True)
