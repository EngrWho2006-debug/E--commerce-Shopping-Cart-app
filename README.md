#  E-commerce Shopping Cart Application

A lightweight, secure, and fully functional Python-based e-commerce platform built using the **Flask** framework and an **SQLite** database. This application features dynamic product listings, a fully interactive shopping cart powered by Flask sessions, and a secure server-side mock payment processing pipeline.

---

##  Features

* **Product Catalog:** Renders a clean grid of available items dynamically fetched from the database.
* **Interactive Shopping Cart:** Users can seamlessly add items, remove items, and see calculations (item totals and grand total) update dynamically.
* **Secure Checkout Mock:** Simulates a tokenized payment processing workflow (e.g., Stripe/PayPal) by securely accepting credentials via POST requests over a simulated protected backend pipeline.
* **Modern UI:** Built with a clean, scannable, single-page responsive interface using Bootstrap 5.

---

## Author

Pragya Singh

---

##  Project Structure

```text
ecommerce_project/
│
├── app.py              # Core application logic & SQLite setup
├── .gitignore          # Tells Git which files to ignore (e.g., .venv)
├── README.md           # Documentation (You are here!)
└── templates/          # HTML templates
    ├── index.html      # Main product listing and interactive sidebar cart
    └── success.html    # Post-payment confirmation page
