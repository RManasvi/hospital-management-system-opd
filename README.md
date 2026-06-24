# Hospital Management System - Advanced SQL Edition

A Python and MySQL command-line project that demonstrates advanced SQL concepts using a simple hospital database. Built as a practice project to get comfortable with SQL topics that come up often in interviews, like views, stored procedures, triggers, window functions, indexing, and CTEs.

## Overview

This is a basic hospital system with two main tables, patients and doctors. Instead of just doing simple SELECT and JOIN queries, the project goes further and includes a working example of almost every important SQL concept, each one runnable from a menu in the terminal.

## Tech Stack

- Language: Python 3
- Database: MySQL
- Connector: mysql.connector
- Interface: Command-line menu

## Features

### 1. View
`vw_patient_doctor_summary` is a saved query that joins the patients and doctors tables. Once created, you can just select from this view instead of writing the join again every time.

### 2. Trigger
`trg_before_patient_delete` runs automatically right before a patient is deleted. It saves the patient's ID and name into a separate `patient_audit_log` table, without needing any extra code in Python to handle it.

### 3. Stored Procedures
- `sp_doctors_by_department` takes a department name and returns the doctors in it, sorted by experience.
- `sp_patient_bill` takes a patient ID and returns their bill details in one go.

These are called from Python using `mycursor.callproc()`.

### 4. Window Functions
- `RANK() OVER` to rank doctors by number of patients, both overall and within their own department.
- `SUM`, `AVG`, and `MAX` with `OVER (PARTITION BY ...)` to show department totals and averages next to each doctor's row, without collapsing the rows like GROUP BY does.
- A running total of appointments by date using `SUM() OVER (ORDER BY ...)`.
- `LAG()` and `LEAD()` to compare each patient visit with the previous or next visit for the same doctor.

### 5. Indexing
- Creates indexes on `doctor_id`, `DateofVisit`, and `department`.
- Includes a demo using `SHOW INDEX` to list existing indexes.
- Includes an `EXPLAIN` demo comparing a query that uses an index against one that does a full table scan, so you can see the difference in the execution plan.

### 6. CTEs (Common Table Expressions)
- A basic CTE to find the top-earning doctors.
- Multiple CTEs chained together to find the top doctor in each department.
- A recursive CTE that generates a number series from 1 to 10, the same pattern used for things like org charts or date ranges.

### 7. NULL Handling
Shows how `IS NULL`, `COALESCE`, and `NULLIF` work, and what happens when you do math with a NULL value.

### 8. Subquery Patterns
- A scalar subquery to find the doctor with the highest fee.
- `IN` and `NOT IN` subqueries.
- `EXISTS`, which is usually faster since it stops at the first match.
- A correlated subquery to find doctors earning more than their department's average.

### 9. UNION and UNION ALL
Combines doctor and patient names using both UNION and UNION ALL, and compares the row counts to show how UNION removes duplicates.

### 10. Regex
Uses `REGEXP` to match doctor names starting with certain letters, and to validate phone number and name formats.

### 11. Normalization
Walks through how the patients and doctors tables follow 1NF, 2NF, and 3NF, and includes a live query that checks the actual foreign key relationship in the database.

## Project Structure

```
hospital-management-system/
|
|-- main.py        (all the code: setup, demos, menu)
|-- README.md
```

This is currently a single file. It can be split into smaller files later, like views.py, procedures.py, and triggers.py, to keep things organized.

## Getting Started

### Requirements
- Python 3
- MySQL Server running locally
- A database named hospital with the doctors and patients tables already created

### Install the dependency
```bash
pip install mysql-connector-python
```

### Set up the connection
Update this part of the script with your own MySQL username and password:
```python
mydb = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="hospital"
)
```

### Run it
```bash
python main.py
```

The first time you run it, choose option 0 from the menu. This creates the view, trigger, audit table, and stored procedures. After that, you can pick any other option to try out a feature.

## Menu Guide

| Option | What it does |
|---|---|
| 1-2 | View (show all appointments / search a patient) |
| 3-4 | Stored procedures (doctors by department / patient bill) |
| 5-6 | Trigger (delete a patient and check the audit log) |
| 7-10 | Window functions (ranking, totals, averages, LAG/LEAD) |
| 11-13 | Indexing (create, view, and EXPLAIN) |
| 14-16 | CTEs (basic, multiple, recursive) |
| 17 | NULL handling |
| 18 | Subquery patterns |
| 19-21 | UNION, Regex, Normalization |
| 0 | First-time setup |
| 99 | Exit |

## Why This Project

Most beginner SQL projects stop at basic SELECT and JOIN queries. This one goes a step further and puts the more advanced topics into practice on the same dataset, which makes it easier to explain and defend in an interview, especially for data analytics or backend roles where SQL knowledge gets tested directly.

## Possible Improvements
- Split the code into separate files by feature
- Add a requirements.txt file
- Move the database password into an environment variable instead of hardcoding it
- Add a schema file with sample data so others can set it up quickly
- Add basic tests to check query outputs

---
Built while preparing for SQL interviews, covering window functions, CTEs, stored procedures, triggers, and database design.
