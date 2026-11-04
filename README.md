# FreshCart — Online Grocery Shopping

## Run in VS Code (Windows)
1. Extract this ZIP.
2. Open the `FreshCart_Project` folder in VS Code.
3. Open Terminal and run:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install flask
python app.py
```

4. Open **http://127.0.0.1:5000** in your browser.

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## Features
- Responsive grocery storefront, product search and category filters
- Shopping cart with quantity controls
- Checkout form and order saving in SQLite (`freshcart.db`)
- Admin order dashboard at **http://127.0.0.1:5000/admin**

This is a student/demo project. Payment is simulated; no real payment gateway is connected.
