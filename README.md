# TINDAHAN - Retail Inventory & Sales Management System

## Title & Description

**TINDAHAN** is a menu-driven Flask web application designed to manage product inventory, process sales transactions, and generate comprehensive business reports. It helps retailers track stock levels accurately, record sales efficiently, and analyze business performance through automated reporting.

The system features role-based access control with separate functionalities for Admin and Staff users, ensuring proper oversight and operational efficiency.

**Version:** 1.0  
**Last Updated:** April 15, 2026

---

## Prerequisites

Before installing and running the project, ensure you have the following:

### System Requirements

- **Operating System:** Windows, macOS, or Linux
- **Python:** Version 3.8 or higher
- **RAM:** Minimum 2GB (recommended 4GB)

### Required Software

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **pip** (Python Package Manager) - Comes with Python
- **Git** (Optional, for version control) - [Download](https://git-scm.com/)
- **Code Editor:** VS Code, PyCharm, or any text editor

### Python Libraries (Installed via pip)

- `Flask==2.3.0` - Web framework
- `Werkzeug` - WSGI utility library (dependency of Flask)

### Browser

- Any modern web browser (Chrome, Firefox, Edge, Safari)

---

## Installation

### Step 1: Clone or Download the Project

**Using Git:**

```bash
git clone https://github.com/reygodz/tindahan.git
cd tindahan
```

**Or download manually:**

1. Download the project as ZIP
2. Extract to your desired location
3. Open terminal/command prompt in the project directory

### Step 2: Create a Virtual Environment (Recommended)

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies

```bash
pip install flask==2.3.0
```

Or install from requirements.txt (if available):

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

You should see output similar to:

```
 * Running on http://127.0.0.1:5000
 * DEBUG mode: on
```

### Step 5: Access the Application

Open your web browser and navigate to:

```
http://localhost:5000
```

You should see the TINDAHAN login page.

### Step 6: Login with Demo Credentials

**Admin Account:**

- Username: `admin`
- Password: `admin123`

**Staff Account:**

- Username: `staff`
- Password: `staff123`

---

## Module Descriptions

### **Module 1: Product Management (Inventory Setup)**

**Status:** ✅ Fully Implemented & Functioning

#### Access

- **Admin Only** | Route: `/inventory`

#### Features

1. **Add New Product**
   - Click `+ Add Product` button
   - Fill in product name, price, and initial quantity
   - System auto-generates product ID (prod_001, prod_002, etc.)
   - Product is immediately added to inventory

2. **View Product List (All Products)**
   - Access via `/inventory`
   - Displays all products in tabular format
   - Shows: Product ID, Name, Price, Quantity, Total Value
   - Stock status indicator (In Stock, Low Stock, Out of Stock)

3. **View Individual Product Details**
   - Click on any product row to view detailed information
   - Shows complete product specifications
   - Displays current pricing and quantity

4. **Update Product Information**
   - Click `Edit` button on any product
   - Modify: Product Name, Price, Quantity
   - Changes saved immediately to inventory
   - Stock history automatically logged

5. **Delete Product**
   - Click `Delete` button on any product
   - Product removed from active inventory
   - Deletion logged in stock history
   - Cannot delete products with pending sales

#### Data Stored

- Product ID (auto-generated)
- Product Name
- Unit Price
- Current Quantity
- Timestamp of creation/modification
- Admin who made changes

#### Example Workflow

```
1. Admin logs in → Dashboard
2. Clicks "Inventory" → Views all products
3. Clicks "+ Add Product"
4. Fills: Name="Pasta", Price="35.00", Qty="200"
5. System creates "prod_006" with all data
6. Product appears in inventory list
```

---

### **Module 2: Stock Management**

**Status:** ✅ Fully Implemented & Functioning

#### Access

- **Admin Only** | Route: `/stock-management`

#### Features

1. **View Low-Stock Products**
   - Dedicated alert section showing all items with stock < 20
   - Shows product name and current quantity
   - Color-coded status (Red = Out of Stock, Orange = Low Stock)

2. **Increase Stock (Restocking)**
   - Click `Restock` button on any product
   - Enter quantity to add
   - Items added to existing stock
   - System automatically updates total
   - Timestamp and user logged

   Example:

   ```
   Current Stock: 15 units
   Restock Amount: +50 units
   New Stock: 65 units
   ```

3. **Decrease Stock (Manual Adjustment)**
   - Click `Adjust` button on any product
   - Enter quantity to remove
   - System validates sufficient stock exists
   - Updates inventory immediately
   - Useful for: Damaged goods, corrections, theft

   Example:

   ```
   Current Stock: 100 units
   Adjustment: -5 units (damaged goods)
   New Stock: 95 units
   ```

4. **View All Current Stock Levels**
   - Master table showing all products
   - Real-time quantity display
   - Status indicator for each item
   - Quick action buttons for restock/adjust

#### Stock History Tracking

Every stock change is logged with:

- Product ID & Name
- Old Quantity → New Quantity
- Action Type (RESTOCK, MANUAL_ADJUSTMENT, SALE)
- Timestamp
- User who made change

#### Example Workflow

```
1. Admin sees product "Rice" at 5 units
2. Alert flag: "Low Stock"
3. Clicks "Restock" for Rice
4. Enters 95 units to add
5. Stock updates: 5 → 100
6. Logged: "admin restocked Rice on 2026-04-15 14:30"
```

---

### **Module 3: Sales Transaction Processing**

**Status:** ✅ Fully Implemented & Functioning

#### Access

- **Admin & Staff** | Route: `/sales`

#### Features

1. **Create New Sale Transaction**
   - Access `/sales` page
   - Real-time form to process sales
   - Only products with stock > 0 available

2. **Select Product(s) to Sell**
   - Dropdown list showing available products
   - Product name + current stock displayed
   - Non-stocked items hidden from dropdown

3. **Input Quantity Per Product**
   - Enter desired selling quantity
   - System validates:
     - Quantity > 0 (positive numbers only)
     - Stock available ≥ requested quantity
     - Real-time error messages if validation fails

4. **Automatic Computation**
   - **Subtotal:** Unit Price × Quantity
   - **Total Amount:** Auto-calculated as user enters quantity
   - Currency formatted to 2 decimal places
   - Philippine Peso (₱) symbol displayed

   Example:

   ```
   Product: Rice
   Unit Price: ₱50.00
   Quantity: 10
   Total: ₱50.00 × 10 = ₱500.00 ✓ Auto-calculated
   ```

5. **Automatic Stock Deduction**
   - Upon successful sale, stock decreases immediately
   - No manual inventory update needed
   - Prevents overselling

   Example:

   ```
   Before Sale: Rice = 100 units
   Process Sale: 10 units of Rice
   After Sale: Rice = 90 units (automatic)
   ```

#### Transaction Details Recorded

- Unique Transaction ID (8-character UUID)
- Product ID & Name
- Quantity Sold
- Unit Price at time of sale
- Total Amount
- Timestamp (Date & Time)
- Cashier/Staff member name
- Sale Date (YYYY-MM-DD format for reporting)

#### Recent Sales Display

- Last 10 transactions shown in reverse chronological order
- Quick reference during shift
- Links to full transaction details

#### Example Workflow

```
1. Staff logs in → Dashboard
2. Clicks "Sales" → Process Sale page
3. Dropdown: Selects "Sugar"
4. Input: Quantity = 5
5. Form: ₱60.00 × 5 = ₱300.00 (auto-calculated)
6. Clicks "Process Sale"
7. Validation passes ✓
8. Stock: Sugar 75 → 70
9. Transaction saved: ID=a1b2c3d4
10. Recent sales list updates
```

---

### **Module 4: Sales History Management**

**Status:** ✅ Fully Implemented & Functioning

#### Access

- **Admin & Staff** | Routes: `/sales-history`, `/sales/details/<id>`

#### Features

1. **Save Every Sale Transaction**
   - Automatic recording of all sales
   - Data stored in-memory during session
   - Complete audit trail maintained
   - No manual entry needed

2. **View All Transactions**
   - Access `/sales-history`
   - Complete transaction list
   - Sorted by date/time (newest first)
   - Displays:
     - Transaction ID
     - Date & Time
     - Product Name
     - Quantity Sold
     - Unit Price
     - Total Amount
     - Cashier Name

3. **View Transaction Details**
   - Click "View Details" on any transaction
   - Dedicated detail page shows:
     - Transaction ID
     - Complete timestamp
     - Product ID & Name
     - Exact quantity sold
     - Unit price at sale time
     - Total transaction amount
     - Cashier who processed it
   - Route: `/sales/details/<transaction_id>`

#### Data Persistence

- All transactions stored in `sales` list
- Maintains: Date, Time, Product, Quantity, Prices
- Linked to cashier for accountability
- Used for: Reporting, auditing, analysis

#### Example Workflow

```
1. Staff/Admin clicks "Sales History"
2. View all transactions since system startup
3. See: "04-15-2026 10:30 | Rice | 10 units | ₱500.00"
4. Click "View Details"
5. Full transaction breakdown displayed
6. Can verify sale details anytime
```

#### Use Cases

- **Verify Sale:** "Was 500 units of Rice sold?"
- **Customer Service:** "What time was my purchase?"
- **Audit Trail:** "Track all sales by specific cashier"
- **Troubleshoot:** "Check stock deductions"

---

### **Module 5: Reporting Module**

**Status:** ✅ Fully Implemented & Functioning

#### Access

- **Admin Only** | Routes: `/reports`, `/reports/daily`, `/reports/monthly`, `/reports/inventory`

#### Reports Menu

- Click "Reports" in navbar
- Three report options displayed with descriptions
- Easy navigation to each report type

---

#### **5.1 Daily Sales Report**

**Route:** `/reports/daily`  
**Viewable:** Every day, auto-selects today's date

##### Features

1. **Total Number of Transactions**
   - Count of all sales today
   - Resets daily at midnight

2. **Total Sales Amount**
   - Sum of all sales values today
   - Currency formatted (₱)
   - Includes incomplete/returned sales

3. **Best-Selling Product**
   - Product with highest revenue today
   - Shows: Product Name, Quantity Sold, Total Value
   - "N/A" shown if no sales today

4. **Transaction Listing**
   - All today's sales in detailed table
   - Columns: Time, Product, Quantity, Unit Price, Total, Cashier
   - Reverse chronological order (newest first)

##### Example Report

```
Date: 2026-04-15

Total Transactions: 12
Total Sales Amount: ₱5,450.00
Best-Selling Product: Rice (45 units - ₱2,250.00)

Transactions Today:
10:45 | Sugar | 5 | ₱60.00 | ₱300.00 | Admin
10:30 | Rice  | 10| ₱50.00 | ₱500.00 | Staff
[more...]
```

---

#### **5.2 Monthly Sales Report**

**Route:** `/reports/monthly`  
**Default:** Current month, can select different month

##### Features

1. **Total Monthly Sales**
   - Sum of all sales in selected month
   - Accurate to peso

2. **Average Daily Sales**
   - Total sales ÷ Days with sales
   - Shows productivity metrics

3. **Monthly Product Sales Summary**
   - Products sold ranked by revenue
   - Shows: Product Name, Quantity Sold, Sales Value
   - Top products easily identified

4. **Daily Breakdown**
   - Day-by-day sales amount
   - Identifies best/worst performing days
   - Helps detect patterns and trends

5. **Month Selection**
   - Input field to select any month (YYYY-MM format)
   - View historical data anytime

##### Example Report

```
Month: 2026-04

Total Transactions: 287
Total Monthly Sales: ₱125,340.00
Average Daily Sales: ₱4,178.00

Product Sales Summary:
1. Rice       | 450 units | ₱22,500.00
2. Cooking Oil| 150 units | ₱27,000.00
3. Sugar      | 320 units | ₱19,200.00

Daily Breakdown:
2026-04-01 | ₱4,500.00
2026-04-02 | ₱3,200.00
[more...]
```

---

#### **5.3 Inventory Report**

**Route:** `/reports/inventory`  
**Viewable:** Real-time, always current

##### Features

1. **Current Stock Levels**
   - All products with current quantities
   - Total items in inventory
   - Total inventory value calculation
   - Columns: Product ID, Name, Quantity, Unit Price, Total Value

2. **Low Stock Alerts**
   - Products with stock < 20 units
   - Color-coded (Orange/Yellow)
   - Highlighted section for quick identification
   - Includes current quantity for restocking

3. **Out-of-Stock Products**
   - Products with 0 units
   - Red-flagged section
   - Critical for ordering decisions
   - Shows price for re-ordering reference

4. **Summary Statistics**
   - Total Items in Stock (count)
   - Total Inventory Value (₱)
   - Number of Out-of-Stock items

##### Example Report

```
INVENTORY REPORT

Total Items: 375 units
Total Value: ₱18,950.00

🚨 OUT OF STOCK (3 products):
- Onions | ₱0 value
- Garlic | ₱0 value

⚠️ LOW STOCK (5 products):
- Salt | 12 units | ₱300.00
- Flour| 18 units | ₱810.00

ALL PRODUCTS:
Product ID | Name        | Qty | Price | Value
prod_001   | Rice        | 100 | ₱50   | ₱5,000
prod_002   | Sugar       | 75  | ₱60   | ₱4,500
[more...]
```

---

## User Roles & Access Control

### **Admin Role**

**Features Available:**

- ✅ Manage Products (Add, Update, Delete)
- ✅ Stock Management (Restock, Adjust)
- ✅ Process Sales
- ✅ View Sales History
- ✅ View All Reports (Daily, Monthly, Inventory)

**Login:**

- Username: `admin` | Password: `admin123`

### **Staff Role**

**Features Available:**

- ✅ Process Sales (Primary function)
- ✅ View Sales History
- ❌ Manage Products
- ❌ Stock Management
- ❌ View Reports

**Login:**

- Username: `staff` | Password: `staff123`

---

## System Architecture

### Technology Stack

- **Backend:** Python 3.8+ with Flask 2.3.0
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Data Storage:** In-Memory (Python dictionaries & lists)
- **Authentication:** Session-based (Flask sessions)

### Data Models

#### Products

```python
products = {
    "prod_001": {
        'name': 'Rice',
        'price': 50.00,
        'quantity': 100
    }
}
```

#### Sales

```python
sales = [{
    'transaction_id': 'a1b2c3d4',
    'product_id': 'prod_001',
    'product_name': 'Rice',
    'quantity': 10,
    'unit_price': 50.00,
    'total_price': 500.00,
    'timestamp': '2026-04-15 10:30:45',
    'date': '2026-04-15',
    'cashier': 'admin'
}]
```

#### Stock History

```python
stock_history = [{
    'product_id': 'prod_001',
    'old_qty': 100,
    'new_qty': 90,
    'action': 'SALE',
    'timestamp': '2026-04-15 10:30:45',
    'user': 'admin'
}]
```

---

## File Structure

```
tindahan/
├── app.py                              # Main Flask application
├── templates/                          # HTML templates
│   ├── login.html                      # Login page
│   ├── dashboard.html                  # Main dashboard
│   ├── inventory.html                  # Product management
│   ├── stock_management.html           # Stock restocking & adjustment
│   ├── sales.html                      # Sales transaction form
│   ├── sales_history.html              # Transaction history list
│   ├── transaction_details.html        # Individual transaction view
│   ├── reports_menu.html               # Report selection menu
│   ├── daily_report.html               # Today's sales report
│   ├── monthly_report.html             # Monthly sales analysis
│   ├── inventory_report.html           # Inventory status report
│   ├── unauthorized.html               # 403 error page
│   ├── 404.html                        # 404 error page
│   └── 500.html                        # 500 error page
├── static/                             # Static files
│   └── style.css                       # Styling for all pages
└── README.md                           # This file
```

---

## Usage Examples

### Example 1: A Complete Sales Day

```
09:00 - Admin logs in, checks dashboard
        Total inventory value: ₱18,950.00

09:15 - Staff processes first sale:
        10 units of Rice @ ₱50.00 = ₱500.00
        Rice stock: 100 → 90

10:30 - Staff processes another sale:
        5 units of Sugar @ ₱60.00 = ₱300.00
        Sugar stock: 75 → 70

14:00 - Admin reviews daily sales report
        Total transactions: 47
        Total sales: ₱8,234.50
        Best seller: Rice (₱3,500.00)

17:00 - Admin checks inventory report
        Low stock alert for Salt (12 units)
        Initiates restock of Salt: +50 units
        New stock: 170 units
```

### Example 2: Monthly Analysis

```
Admin wants to analyze April performance:
1. Go to Reports → Monthly Sales Report
2. Select month: 2026-04
3. View:
   - Total sales: ₱125,340.00
   - Average daily: ₱4,178.00
   - Top product: Cooking Oil (₱27,000.00)
   - Trend: Week 1 slower, Week 3-4 peak
4. Decision: Plan promotional sale for Week 2
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:** Install Flask

```bash
pip install flask==2.3.0
```

### Issue: "Address already in use"

**Solution:** Flask app already running

```bash
# Kill process on port 5000, or run on different port:
python app.py --port 5001
```

### Issue: "Login credentials not working"

**Solution:** Check spelling

- Admin: `admin` / `admin123`
- Staff: `staff` / `staff123`

### Issue: "Data disappears after restart"

**Normal Behavior:** In-memory database resets on app restart.  
For persistent data, implement SQLite or PostgreSQL (future feature).

---

## Future Enhancements

- [ ] Database persistence (SQLite/PostgreSQL)
- [ ] User registration & password management
- [ ] Advanced search & filtering
- [ ] Bulk import products (CSV)
- [ ] Export reports to PDF/Excel
- [ ] Multi-location support
- [ ] Customer loyalty program
- [ ] Mobile app version

---

## License

This project is proprietary software. All rights reserved.

---

## Contact & Support

**Project:** TINDAHAN - Retail Inventory & Sales Management  
**Version:** 1.0  
**Last Updated:** April 15, 2026  
**Author:** Development Team

For issues, feature requests, or support:

- GitHub: [reygodz/tindahan](https://github.com/reygodz/tindahan)

---

## Changelog

### Version 1.0 (April 15, 2026)

✅ Module 1: Product Management  
✅ Module 2: Stock Management  
✅ Module 3: Sales Transaction Processing  
✅ Module 4: Sales History Management  
✅ Module 5: Reporting Module  
✅ Role-Based Access Control  
✅ Stock History Tracking
