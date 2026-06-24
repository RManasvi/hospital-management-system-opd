

import mysql.connector

# ============================================================
#   HOSPITAL MANAGEMENT SYSTEM - ADVANCED SQL EDITION
#   Added: VIEW | STORED PROCEDURE | TRIGGER | WINDOW FUNCTION
# ============================================================

mydb = mysql.connector.connect(
    host="localhost",
    user="Manasvi",
    password="manasvi",
    database="hospital"
)
mycursor = mydb.cursor()

# ============================================================
#  SECTION 1: SETUP — Create Advanced SQL Objects
#  (Run once to create VIEW, TRIGGER, STORED PROCEDURES)
# ============================================================

def setup_advanced_sql():
    """
    Creates all advanced SQL objects in the database.
    Call this ONCE after your tables are ready.
    """
    print("\n[SETUP] Creating advanced SQL objects...\n")

    # ── 1. VIEW ─────────────────────────────────────────────
    # A saved query — no need to write JOIN every time
    # Interview point: VIEW simplifies complex queries & adds security layer
    mycursor.execute("DROP VIEW IF EXISTS vw_patient_doctor_summary")
    mycursor.execute("""
        CREATE VIEW vw_patient_doctor_summary AS
        SELECT
            p.id_patients,
            p.DateofVisit,
            p.name_patients,
            p.age,
            p.gender,
            p.current_prob,
            p.Blood_Pressure,
            d.id_doctor,
            d.name_doc       AS doctor_name,
            d.department,
            d.qualifications,
            d.charges        AS consultation_fee
        FROM patients p
        JOIN doctors d ON p.doctor_id = d.id_doctor
    """)
    print("  VIEW created: vw_patient_doctor_summary")

    # ── 2. AUDIT TABLE for Trigger ───────────────────────────
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS patient_audit_log (
            log_id       INT AUTO_INCREMENT PRIMARY KEY,
            patient_id   INT,
            patient_name VARCHAR(255),
            deleted_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            deleted_by   VARCHAR(50) DEFAULT 'SYSTEM'
        )
    """)
    print("  TABLE created: patient_audit_log")

    # ── 3. TRIGGER ──────────────────────────────────────────
    # Automatically fires BEFORE a patient record is deleted
    # Interview point: Trigger = automatic action on DB event (INSERT/UPDATE/DELETE)
    mycursor.execute("DROP TRIGGER IF EXISTS trg_before_patient_delete")
    mycursor.execute("""
        CREATE TRIGGER trg_before_patient_delete
        BEFORE DELETE ON patients
        FOR EACH ROW
        BEGIN
            INSERT INTO patient_audit_log (patient_id, patient_name)
            VALUES (OLD.id_patients, OLD.name_patients);
        END
    """)
    print("  TRIGGER created: trg_before_patient_delete")

    # ── 4. STORED PROCEDURE 1 — Search by Department ────────
    # Interview point: Stored Proc = precompiled SQL, reusable, faster
    mycursor.execute("DROP PROCEDURE IF EXISTS sp_doctors_by_department")
    mycursor.execute("""
        CREATE PROCEDURE sp_doctors_by_department(IN dept_name VARCHAR(50))
        BEGIN
            SELECT id_doctor, name_doc, qualifications,
                   Years_Of_Experience, charges
            FROM doctors
            WHERE department = dept_name
            ORDER BY Years_Of_Experience DESC;
        END
    """)
    print("  STORED PROCEDURE created: sp_doctors_by_department")

    # ── 5. STORED PROCEDURE 2 — Patient Bill Summary ────────
    mycursor.execute("DROP PROCEDURE IF EXISTS sp_patient_bill")
    mycursor.execute("""
        CREATE PROCEDURE sp_patient_bill(IN p_id INT)
        BEGIN
            SELECT
                p.id_patients,
                p.name_patients,
                p.DateofVisit,
                d.name_doc,
                d.department,
                d.charges AS total_bill
            FROM patients p
            JOIN doctors d ON p.doctor_id = d.id_doctor
            WHERE p.id_patients = p_id;
        END
    """)
    print("  STORED PROCEDURE created: sp_patient_bill")

    mydb.commit()
    print("\n[SETUP] All advanced SQL objects created successfully!\n")


# ============================================================
#  SECTION 2: VIEW USAGE
# ============================================================

def show_all_appointments_via_view():
    """Uses VIEW instead of raw JOIN — cleaner & reusable."""
    print("\n📋 ALL APPOINTMENTS (via VIEW: vw_patient_doctor_summary)")
    print("=" * 70)
    mycursor.execute("SELECT * FROM vw_patient_doctor_summary ORDER BY DateofVisit DESC")
    rows = mycursor.fetchall()
    if not rows:
        print("No appointments found.")
        return
    headers = ["P.ID", "Date", "Patient", "Age", "Gender", "Problem", "BP",
               "D.ID", "Doctor", "Dept", "Quals", "Fee"]
    col_w = [5, 12, 20, 4, 7, 20, 10, 5, 20, 15, 10, 6]
    header_line = " | ".join(str(h).ljust(w) for h, w in zip(headers, col_w))
    print(header_line)
    print("-" * len(header_line))
    for row in rows:
        print(" | ".join(str(val).ljust(w) for val, w in zip(row, col_w)))
    print("=" * 70)


def search_patient_via_view():
    """Search a specific patient using the VIEW."""
    pid = int(input("\nEnter Patient ID: "))
    print(f"\n🔍 PATIENT DETAILS (via VIEW)")
    print("=" * 50)
    mycursor.execute(
        "SELECT * FROM vw_patient_doctor_summary WHERE id_patients = %s", (pid,)
    )
    row = mycursor.fetchone()
    if row:
        labels = ["Patient ID", "Date of Visit", "Patient Name", "Age", "Gender",
                  "Current Problem", "Blood Pressure", "Doctor ID", "Doctor Name",
                  "Department", "Qualifications", "Consultation Fee"]
        for label, val in zip(labels, row):
            print(f"  {label:<20}: {val}")
    else:
        print("  Patient not found.")
    print("=" * 50)


# ============================================================
#  SECTION 3: STORED PROCEDURE CALLS
# ============================================================

def search_doctors_by_department():
    """Calls stored procedure sp_doctors_by_department."""
    dept = input("\nEnter Department name (e.g. Cardiology, Ortho): ").strip()
    print(f"\n🏥 DOCTORS IN '{dept}' (via Stored Procedure)")
    print("=" * 60)
    mycursor.callproc("sp_doctors_by_department", [dept])
    found = False
    for result in mycursor.stored_results():
        rows = result.fetchall()
        if rows:
            found = True
            print(f"  {'ID':<5} {'Name':<20} {'Quals':<15} {'Exp(Yrs)':<10} {'Fee'}")
            print("  " + "-" * 55)
            for row in rows:
                print(f"  {row[0]:<5} {row[1]:<20} {row[2]:<15} {row[3]:<10} ₹{row[4]}")
        else:
            print(f"  No doctors found in department: {dept}")
    if not found:
        print(f"  No doctors found in department: {dept}")
    print("=" * 60)


def get_patient_bill_via_procedure():
    """Calls stored procedure sp_patient_bill."""
    pid = int(input("\nEnter Patient ID for bill: "))
    print(f"\n🧾 PATIENT BILL (via Stored Procedure)")
    print("=" * 50)
    mycursor.callproc("sp_patient_bill", [pid])
    found = False
    for result in mycursor.stored_results():
        row = result.fetchone()
        if row:
            found = True
            labels = ["Patient ID", "Patient Name", "Date of Visit",
                      "Doctor Name", "Department", "Total Bill"]
            for label, val in zip(labels, row):
                prefix = "₹" if label == "Total Bill" else ""
                print(f"  {label:<18}: {prefix}{val}")
    if not found:
        print("  Patient ID not found.")
    print("=" * 50)


# ============================================================
#  SECTION 4: TRIGGER DEMO
# ============================================================

def show_audit_log():
    """Shows the audit log table — proof that TRIGGER is working."""
    print("\n📝 PATIENT DELETION AUDIT LOG (Trigger recorded these)")
    print("=" * 65)
    mycursor.execute("SELECT * FROM patient_audit_log ORDER BY deleted_at DESC")
    rows = mycursor.fetchall()
    if not rows:
        print("  No deletions recorded yet.")
    else:
        print(f"  {'Log ID':<8} {'Patient ID':<12} {'Patient Name':<25} {'Deleted At'}")
        print("  " + "-" * 60)
        for row in rows:
            print(f"  {row[0]:<8} {row[1]:<12} {row[2]:<25} {row[3]}")
    print("=" * 65)


def delete_patient_with_trigger_demo():
    """
    Deletes a patient — trigger auto-logs it.
    Interview: 'Trigger fires automatically, no app-level code needed for audit.'
    """
    pid = int(input("\nEnter Patient ID to delete: "))
    confirm = input(f"  ⚠️  Delete patient ID {pid}? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("  Cancelled.")
        return
    mycursor.execute("DELETE FROM patients WHERE id_patients = %s", (pid,))
    mydb.commit()
    if mycursor.rowcount > 0:
        print(f"  Patient {pid} deleted. Trigger auto-logged this action.")
        print("     Run 'Show Audit Log' to verify.")
    else:
        print("  Patient ID not found.")


# ============================================================
#  SECTION 5: WINDOW FUNCTIONS
# ============================================================

def doctor_patient_ranking():
    """
    Window Function: RANK doctors by patient count using RANK() OVER()
    Interview point: Window functions work on result set without collapsing rows
    """
    print("\n🏆 DOCTOR RANKING BY PATIENT COUNT (Window Function: RANK)")
    print("=" * 60)
    mycursor.execute("""
        SELECT
            d.id_doctor,
            d.name_doc,
            d.department,
            COUNT(p.id_patients)                          AS total_patients,
            RANK() OVER (ORDER BY COUNT(p.id_patients) DESC)  AS rank_overall,
            RANK() OVER (
                PARTITION BY d.department
                ORDER BY COUNT(p.id_patients) DESC
            )                                             AS rank_in_dept
        FROM doctors d
        LEFT JOIN patients p ON d.id_doctor = p.doctor_id
        GROUP BY d.id_doctor, d.name_doc, d.department
        ORDER BY rank_overall
    """)
    rows = mycursor.fetchall()
    print(f"  {'ID':<5} {'Doctor':<20} {'Dept':<15} {'Patients':<10} {'Overall Rank':<14} {'Rank in Dept'}")
    print("  " + "-" * 70)
    for row in rows:
        print(f"  {row[0]:<5} {row[1]:<20} {row[2]:<15} {row[3]:<10} #{row[4]:<13} #{row[5]}")
    print("=" * 60)


def department_wise_stats():
    """
    Window Function: SUM OVER + AVG OVER for department analytics
    Interview point: Aggregate + Window = see individual row AND group total together
    """
    print("\n📊 DEPARTMENT-WISE ANALYTICS (Window Functions: SUM OVER, AVG OVER)")
    print("=" * 75)
    mycursor.execute("""
        SELECT
            d.department,
            d.name_doc,
            d.charges,
            COUNT(p.id_patients)                                           AS patients_seen,
            SUM(d.charges) OVER (PARTITION BY d.department)               AS dept_total_revenue,
            ROUND(AVG(d.charges) OVER (PARTITION BY d.department), 2)     AS dept_avg_fee,
            MAX(d.charges) OVER (PARTITION BY d.department)               AS dept_max_fee
        FROM doctors d
        LEFT JOIN patients p ON d.id_doctor = p.doctor_id
        GROUP BY d.id_doctor, d.name_doc, d.department, d.charges
        ORDER BY d.department, d.charges DESC
    """)
    rows = mycursor.fetchall()
    print(f"  {'Dept':<15} {'Doctor':<20} {'Fee':<8} {'Pts':<5} {'Dept Revenue':<14} {'Avg Fee':<10} {'Max Fee'}")
    print("  " + "-" * 80)
    for row in rows:
        print(f"  {row[0]:<15} {row[1]:<20} ₹{row[2]:<7} {row[3]:<5} ₹{row[4]:<13} ₹{row[5]:<9} ₹{row[6]}")
    print("=" * 75)


def running_total_appointments():
    """
    Window Function: Cumulative/Running total of appointments by date
    Interview point: SUM() OVER (ORDER BY date) = running total pattern
    """
    print("\n📈 RUNNING TOTAL OF APPOINTMENTS BY DATE (Window: SUM OVER ORDER BY)")
    print("=" * 55)
    mycursor.execute("""
        SELECT
            DateofVisit,
            COUNT(*)                                                      AS appointments_on_day,
            SUM(COUNT(*)) OVER (ORDER BY DateofVisit ROWS UNBOUNDED PRECEDING) AS running_total
        FROM patients
        GROUP BY DateofVisit
        ORDER BY DateofVisit
    """)
    rows = mycursor.fetchall()
    if not rows:
        print("  No appointment data found.")
    else:
        print(f"  {'Date':<14} {'That Day':<12} {'Running Total'}")
        print("  " + "-" * 38)
        for row in rows:
            print(f"  {str(row[0]):<14} {row[1]:<12} {row[2]}")
    print("=" * 55)


def lag_lead_appointments():
    """
    Window Function: LAG/LEAD to compare consecutive visits
    Interview point: LAG = previous row value, LEAD = next row value
    """
    print("\n🔄 PATIENT VISIT COMPARISON — LAG & LEAD (Window Functions)")
    print("=" * 70)
    mycursor.execute("""
        SELECT
            id_patients,
            name_patients,
            DateofVisit,
            LAG(DateofVisit)  OVER (PARTITION BY doctor_id ORDER BY DateofVisit) AS prev_visit_same_doc,
            LEAD(DateofVisit) OVER (PARTITION BY doctor_id ORDER BY DateofVisit) AS next_visit_same_doc
        FROM patients
        ORDER BY doctor_id, DateofVisit
    """)
    rows = mycursor.fetchall()
    print(f"  {'P.ID':<6} {'Name':<20} {'Visit Date':<13} {'Prev Visit':<13} {'Next Visit'}")
    print("  " + "-" * 65)
    for row in rows:
        prev = str(row[3]) if row[3] else "—"
        nxt  = str(row[4]) if row[4] else "—"
        print(f"  {row[0]:<6} {row[1]:<20} {str(row[2]):<13} {prev:<13} {nxt}")
    print("=" * 70)


# ============================================================
#  MAIN MENU
# ============================================================

def advanced_sql_menu():
    while True:
        print("""
╔══════════════════════════════════════════════════════╗
║     HOSPITAL MANAGEMENT — ADVANCED SQL FEATURES      ║
╠══════════════════════════════════════════════════════╣
║  ── VIEW ──────────────────────────────────────────  ║
║  1. Show All Appointments (via VIEW)                 ║
║  2. Search Patient Details (via VIEW)                ║
║                                                      ║
║  ── STORED PROCEDURES ─────────────────────────────  ║
║  3. Search Doctors by Department (Stored Proc)       ║
║  4. Get Patient Bill (Stored Proc)                   ║
║                                                      ║
║  ── TRIGGER ───────────────────────────────────────  ║
║  5. Delete Patient (Trigger auto-logs it)            ║
║  6. Show Audit Log (Trigger proof)                   ║
║                                                      ║
║  ── WINDOW FUNCTIONS ──────────────────────────────  ║
║  7. Doctor Ranking by Patients (RANK OVER)           ║
║  8. Department Analytics (SUM OVER, AVG OVER)        ║
║  9. Running Total of Appointments (SUM OVER ORDER)   ║
║  10. Visit Comparison - LAG & LEAD                   ║
║                                                      ║
║  ── SETUP ─────────────────────────────────────────  ║
║  0. First-Time Setup (create VIEW/PROC/TRIGGER)      ║
║  99. Exit                                            ║
╚══════════════════════════════════════════════════════╝""")

        try:
            choice = int(input("\n  Enter choice: "))
        except ValueError:
            print("  Enter a valid number.")
            continue

        if   choice == 0:  setup_advanced_sql()
        elif choice == 1:  show_all_appointments_via_view()
        elif choice == 2:  search_patient_via_view()
        elif choice == 3:  search_doctors_by_department()
        elif choice == 4:  get_patient_bill_via_procedure()
        elif choice == 5:  delete_patient_with_trigger_demo()
        elif choice == 6:  show_audit_log()
        elif choice == 7:  doctor_patient_ranking()
        elif choice == 8:  department_wise_stats()
        elif choice == 9:  running_total_appointments()
        elif choice == 10: lag_lead_appointments()
        elif choice == 99:
            print("\n  Goodbye! 👋\n")
            break
        else:
            print("  Invalid choice.")


# if __name__ == "__main__":
#     advanced_sql_menu()


# ============================================================
#  SECTION 6: INDEX DEMO
#  Topic: Index — speeds up SELECT, clustered vs non-clustered
# ============================================================

def create_indexes():
    """
    Creates indexes on commonly searched columns.
    Interview: Index = B+ Tree structure, speeds up WHERE/JOIN/ORDER BY.
    Downside: slows INSERT/UPDATE (index must be updated too).
    """
    print("\n⚡ CREATING INDEXES (B+ Tree based)")
    print("=" * 50)

    queries = [
        ("idx_patients_doctor_id",
         "CREATE INDEX idx_patients_doctor_id ON patients(doctor_id)",
         "patients(doctor_id) — speeds up JOIN with doctors"),
        ("idx_patients_date",
         "CREATE INDEX idx_patients_date ON patients(DateofVisit)",
         "patients(DateofVisit) — speeds up date-based search"),
        ("idx_doctors_dept",
         "CREATE INDEX idx_doctors_dept ON doctors(department)",
         "doctors(department) — speeds up department filter"),
    ]

    for idx_name, sql, reason in queries:
        try:
            mycursor.execute(sql)
            print(f"  Index created: {idx_name}")
            print(f"     Reason: {reason}")
        except Exception as e:
            if "Duplicate key name" in str(e):
                print(f"  ℹ️  Index already exists: {idx_name}")
            else:
                print(f"  ⚠️  {e}")

    mydb.commit()
    print("=" * 50)


def show_indexes():
    """
    Shows all indexes on doctors and patients tables.
    Interview: SHOW INDEX tells you what indexes exist + column order (for composite).
    """
    for table in ["doctors", "patients"]:
        print(f"\n📑 INDEXES ON TABLE: {table}")
        print("=" * 65)
        mycursor.execute(f"SHOW INDEX FROM {table}")
        rows = mycursor.fetchall()
        print(f"  {'Key Name':<30} {'Column':<20} {'Unique':<8} {'Seq'}")
        print("  " + "-" * 60)
        for row in rows:
            unique = "YES" if row[1] == 0 else "NO"
            print(f"  {row[2]:<30} {row[4]:<20} {unique:<8} {row[3]}")
        print("=" * 65)


def explain_query_demo():
    """
    EXPLAIN shows the query execution plan.
    Interview: Full table scan (type=ALL) = bad. Index used (type=ref) = good.
    """
    print("\n🔍 EXPLAIN — Query Execution Plan Demo")
    print("=" * 65)

    print("\n  [Query 1] Search patient by doctor_id (uses index):")
    mycursor.execute("EXPLAIN SELECT * FROM patients WHERE doctor_id = 1")
    rows = mycursor.fetchall()
    cols = ["id","select_type","table","partitions","type",
            "possible_keys","key","key_len","ref","rows","filtered","Extra"]
    for row in rows:
        for col, val in zip(cols, row):
            print(f"    {col:<15}: {val}")

    print("\n  [Query 2] Search patient by age (no index — full scan):")
    mycursor.execute("EXPLAIN SELECT * FROM patients WHERE age = 30")
    rows = mycursor.fetchall()
    for row in rows:
        for col, val in zip(cols, row):
            print(f"    {col:<15}: {val}")

    print("\n  💡 Interview Tip: Look at 'type' column:")
    print("     ALL  = full table scan (slow) ")
    print("     ref  = index used (fast)")
    print("=" * 65)


# ============================================================
#  SECTION 7: CTE — Common Table Expressions
#  Topics: Basic CTE, Multiple CTE, Recursive CTE
# ============================================================

def cte_basic_demo():
    """
    Basic CTE — same as subquery but more readable.
    Interview: CTE is defined with WITH keyword, exists only for that query.
    """
    print("\n📦 BASIC CTE — Top Earning Doctors")
    print("=" * 55)
    mycursor.execute("""
        WITH DoctorEarnings AS (
            SELECT
                d.id_doctor,
                d.name_doc,
                d.department,
                d.charges,
                COUNT(p.id_patients) AS total_patients,
                (d.charges * COUNT(p.id_patients)) AS estimated_revenue
            FROM doctors d
            LEFT JOIN patients p ON d.id_doctor = p.doctor_id
            GROUP BY d.id_doctor, d.name_doc, d.department, d.charges
        )
        SELECT *
        FROM DoctorEarnings
        ORDER BY estimated_revenue DESC
    """)
    rows = mycursor.fetchall()
    print(f"  {'ID':<5} {'Doctor':<20} {'Dept':<15} {'Fee':<7} {'Patients':<10} {'Revenue'}")
    print("  " + "-" * 65)
    for row in rows:
        print(f"  {row[0]:<5} {row[1]:<20} {row[2]:<15} ₹{row[3]:<6} {row[4]:<10} ₹{row[5]}")
    print("=" * 55)


def cte_multiple_demo():
    """
    Multiple CTEs — chain them with comma.
    Interview: Multiple CTEs make complex queries readable step-by-step.
    """
    print("\n📦 MULTIPLE CTE — Department Summary + Top Doctor per Dept")
    print("=" * 65)
    mycursor.execute("""
        WITH
        PatientCount AS (
            SELECT doctor_id, COUNT(*) AS total_patients
            FROM patients
            GROUP BY doctor_id
        ),
        DoctorWithCount AS (
            SELECT d.id_doctor, d.name_doc, d.department, d.charges,
                   COALESCE(pc.total_patients, 0) AS total_patients
            FROM doctors d
            LEFT JOIN PatientCount pc ON d.id_doctor = pc.doctor_id
        ),
        TopPerDept AS (
            SELECT *,
                   RANK() OVER (PARTITION BY department ORDER BY total_patients DESC) AS dept_rank
            FROM DoctorWithCount
        )
        SELECT id_doctor, name_doc, department, charges, total_patients, dept_rank
        FROM TopPerDept
        WHERE dept_rank = 1
        ORDER BY department
    """)
    rows = mycursor.fetchall()
    print(f"  {'ID':<5} {'Doctor':<20} {'Dept':<15} {'Fee':<8} {'Patients':<10} {'Rank in Dept'}")
    print("  " + "-" * 68)
    for row in rows:
        print(f"  {row[0]:<5} {row[1]:<20} {row[2]:<15} ₹{row[3]:<7} {row[4]:<10} #{row[5]}")
    print("\n  💡 Interview Tip: Multiple CTEs = step-by-step SQL logic, very readable.")
    print("=" * 65)


def cte_recursive_demo():
    """
    Recursive CTE — generates a series (e.g. appointment number sequence).
    Interview: Recursive CTE has anchor + recursive member, used for
               hierarchical data (org charts, category trees, date series).
    """
    print("\n🔁 RECURSIVE CTE — Generate Appointment Number Series (1 to 10)")
    print("=" * 55)
    mycursor.execute("""
        WITH RECURSIVE AppointmentSeries AS (
            -- Anchor: starting point
            SELECT 1 AS appointment_no

            UNION ALL

            -- Recursive member: keep adding 1
            SELECT appointment_no + 1
            FROM AppointmentSeries
            WHERE appointment_no < 10
        )
        SELECT appointment_no FROM AppointmentSeries
    """)
    rows = mycursor.fetchall()
    nums = [str(r[0]) for r in rows]
    print(f"  Generated series: {', '.join(nums)}")
    print("\n  💡 Interview Tip: Recursive CTE = anchor query UNION ALL recursive query.")
    print("     Real use: org hierarchy, folder tree, date range generation.")
    print("=" * 55)


# ============================================================
#  SECTION 8: NULL HANDLING DEMOS
#  Topics: IS NULL, COALESCE, NULLIF, IFNULL, NULL in math
# ============================================================

def null_handling_demo():
    """
    Demonstrates all NULL handling techniques on real hospital data.
    Interview: NULL != 0 != '' — it means UNKNOWN. NULL in math = NULL.
    """
    print("\n🚫 NULL HANDLING DEMOS")
    print("=" * 60)

    # IS NULL — find patients with no allergy medicine listed
    print("\n  [1] IS NULL — Patients with NO allergic medicine on record:")
    mycursor.execute("""
        SELECT id_patients, name_patients, allergy, allergic_medicine
        FROM patients
        WHERE allergic_medicine IS NULL OR allergic_medicine = ''
    """)
    rows = mycursor.fetchall()
    for row in rows:
        print(f"    Patient {row[0]}: {row[1]} | Allergy: {row[2]} | Medicine: {row[3]}")
    if not rows:
        print("    (No NULL allergic_medicine records — add some test data)")

    # COALESCE — replace NULL with default
    print("\n  [2] COALESCE — Show 'None listed' if allergic_medicine is NULL:")
    mycursor.execute("""
        SELECT id_patients, name_patients,
               COALESCE(NULLIF(allergic_medicine,''), 'None listed') AS safe_medicine
        FROM patients
    """)
    rows = mycursor.fetchall()
    for row in rows:
        print(f"    {row[0]}: {row[1]:<20} → {row[2]}")

    # NULL in math
    print("\n  [3] NULL in math — charges + NULL = NULL (always):")
    mycursor.execute("""
        SELECT name_doc, charges,
               charges + NULL AS null_math_result,
               COALESCE(charges + NULL, 0) AS safe_result
        FROM doctors LIMIT 3
    """)
    rows = mycursor.fetchall()
    print(f"    {'Doctor':<20} {'Charges':<10} {'+ NULL':<12} {'COALESCE(,0)'}")
    print("    " + "-" * 52)
    for row in rows:
        print(f"    {row[0]:<20} ₹{row[1]:<9} {str(row[2]):<12} ₹{row[3]}")

    print("\n  💡 Key Interview Points:")
    print("     IS NULL  — check for null (NOT: = NULL )")
    print("     COALESCE — returns first non-null value")
    print("     NULLIF(a,b) — returns NULL if a=b, else returns a")
    print("     IFNULL(col, default) — MySQL specific shorthand")
    print("=" * 60)


# ============================================================
#  SECTION 9: SUBQUERY PATTERNS
#  Topics: Scalar, Correlated, EXISTS vs IN, NOT EXISTS
# ============================================================

def subquery_patterns_demo():
    """
    Demonstrates key subquery patterns asked in interviews.
    """
    print("\n🔎 SUBQUERY PATTERNS")
    print("=" * 60)

    # Scalar subquery
    print("\n  [1] SCALAR SUBQUERY — Doctor with highest charges:")
    mycursor.execute("""
        SELECT name_doc, department, charges
        FROM doctors
        WHERE charges = (SELECT MAX(charges) FROM doctors)
    """)
    rows = mycursor.fetchall()
    for row in rows:
        print(f"    {row[0]} | {row[1]} | ₹{row[2]}")

    # IN subquery — doctors who have at least 1 patient
    print("\n  [2] IN SUBQUERY — Doctors who have patients:")
    mycursor.execute("""
        SELECT name_doc, department
        FROM doctors
        WHERE id_doctor IN (SELECT DISTINCT doctor_id FROM patients)
    """)
    rows = mycursor.fetchall()
    for row in rows:
        print(f"    {row[0]} ({row[1]})")

    # NOT IN — doctors with NO patients
    print("\n  [3] NOT IN — Doctors with no patients yet:")
    mycursor.execute("""
        SELECT name_doc, department
        FROM doctors
        WHERE id_doctor NOT IN (SELECT DISTINCT doctor_id FROM patients)
    """)
    rows = mycursor.fetchall()
    for row in rows:
        print(f"    {row[0]} ({row[1]})")
    if not rows:
        print("    (All doctors have patients)")

    # EXISTS
    print("\n  [4] EXISTS — Departments that have at least one doctor with experience > 5 yrs:")
    mycursor.execute("""
        SELECT DISTINCT department
        FROM doctors d1
        WHERE EXISTS (
            SELECT 1 FROM doctors d2
            WHERE d2.department = d1.department
            AND d2.Years_Of_Experience > 5
        )
    """)
    rows = mycursor.fetchall()
    for row in rows:
        print(f"    {row[0]}")

    # Correlated subquery
    print("\n  [5] CORRELATED SUBQUERY — Doctors earning above their dept average:")
    mycursor.execute("""
        SELECT name_doc, department, charges
        FROM doctors d_outer
        WHERE charges > (
            SELECT AVG(charges)
            FROM doctors d_inner
            WHERE d_inner.department = d_outer.department
        )
    """)
    rows = mycursor.fetchall()
    for row in rows:
        print(f"    {row[0]:<20} {row[1]:<15} ₹{row[2]}")
    if not rows:
        print("    (Need more doctors per department to show this)")

    print("\n  💡 Interview: Correlated subquery runs once PER ROW — slower than JOIN.")
    print("     EXISTS stops at first match — faster than IN for large datasets.")
    print("=" * 60)


# ============================================================
#  SECTION 10: UNION / UNION ALL / INTERSECT demo
# ============================================================

def union_demo():
    """
    UNION removes duplicates. UNION ALL keeps all rows.
    Interview: UNION ALL is faster (no dedup step).
    """
    print("\n🔗 UNION / UNION ALL DEMO")
    print("=" * 55)

    print("\n  [1] UNION — Combined list of all names (doctors + patients), no duplicates:")
    mycursor.execute("""
        SELECT name_doc AS name, 'Doctor' AS role FROM doctors
        UNION
        SELECT name_patients, 'Patient' FROM patients
        ORDER BY role, name
    """)
    rows = mycursor.fetchall()
    for row in rows:
        print(f"    {row[1]:<10} : {row[0]}")

    print("\n  [2] UNION ALL — Same but keeps duplicates (if any same name):")
    mycursor.execute("""
        SELECT name_doc AS name, 'Doctor' AS role FROM doctors
        UNION ALL
        SELECT name_patients, 'Patient' FROM patients
        ORDER BY role, name
    """)
    rows2 = mycursor.fetchall()
    print(f"    Total rows with UNION ALL: {len(rows2)}  (vs UNION: {len(rows)})")
    print("\n  💡 UNION ALL is faster — use when you know there are no duplicates.")
    print("=" * 55)


# ============================================================
#  SECTION 11: REGEX DEMO
# ============================================================

def regex_demo():
    """
    REGEXP / RLIKE in MySQL for pattern matching.
    Interview: More powerful than LIKE — supports full regex patterns.
    """
    print("\n🔤 REGEX IN SQL (REGEXP / RLIKE)")
    print("=" * 55)

    print("\n  [1] Doctor names starting with 'D' or 'S':")
    mycursor.execute("""
        SELECT name_doc, department
        FROM doctors
        WHERE name_doc REGEXP '^[DS]'
    """)
    rows = mycursor.fetchall()
    for row in rows:
        print(f"    {row[0]} ({row[1]})")
    if not rows:
        print("    (No doctors with name starting D or S in test data)")

    print("\n  [2] Patient phone numbers — validate 10 digit format:")
    mycursor.execute("""
        SELECT name_patients, Phone_number,
               CASE
                   WHEN Phone_number REGEXP '^[0-9]{10}$' THEN 'Valid'
                   ELSE 'Invalid'
               END AS phone_status
        FROM patients
    """)
    rows = mycursor.fetchall()
    for row in rows:
        print(f"    {row[0]:<20} {row[1]:<12} {row[2]}")

    print("\n  [3] Find patients whose name contains only letters (no numbers/symbols):")
    mycursor.execute("""
        SELECT name_patients
        FROM patients
        WHERE name_patients REGEXP '^[A-Za-z ]+$'
    """)
    rows = mycursor.fetchall()
    for row in rows:
        print(f"    {row[0]}")

    print("\n  💡 LIKE vs REGEXP:")
    print("     LIKE 'A%'       — starts with A (simple)")
    print("     REGEXP '^[A-C]' — starts with A, B, or C (powerful)")
    print("=" * 55)


# ============================================================
#  SECTION 12: NORMALIZATION DEMO (conceptual on real tables)
# ============================================================

def normalization_demo():
    """
    Shows how the hospital tables follow normalization rules.
    Interview: 1NF=atomic, 2NF=no partial dependency, 3NF=no transitive dependency.
    """
    print("\n📐 NORMALIZATION DEMO — Hospital Tables")
    print("=" * 65)

    print("""
  [1NF — First Normal Form]
  Rule: Each column must have atomic (indivisible) values. No repeating groups.
  Our 'patients' table:
     - Each column has one value per row (name, age, gender are all atomic)
     - phone_number is a single value, not a list
     - blood_group is atomic
  VIOLATION EXAMPLE (NOT in our DB):
     - If we stored "Dr.A, Dr.B" in a single doctor column → NOT 1NF

  [2NF — Second Normal Form]
  Rule: Must be 1NF + No partial dependency (non-key column depends on PART of PK).
  Our tables use single-column PKs (id_doctor, id_patients)
     → No composite PK → partial dependency impossible → 2NF satisfied
  VIOLATION EXAMPLE:
     - If PK was (patient_id, doctor_id) and doctor_name depended only on doctor_id
       → that would be partial dependency → NOT 2NF

  [3NF — Third Normal Form]
  Rule: Must be 2NF + No transitive dependency (non-key → non-key → non-key).
  Our design:
     - Doctor info (name, dept, charges) is in 'doctors' table
     - Patients table only stores doctor_id (FK), NOT doctor_name directly
     - If we stored doctor_name in patients table too → transitive dep → NOT 3NF
  This is why we use FK (doctor_id) instead of copying doctor details.
    """)

    # Show actual FK relationship
    print("  [Live Demo] Verifying FK relationship:")
    mycursor.execute("""
        SELECT
            TABLE_NAME, COLUMN_NAME,
            REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = 'hospital'
          AND REFERENCED_TABLE_NAME IS NOT NULL
    """)
    rows = mycursor.fetchall()
    for row in rows:
        print(f"    {row[0]}.{row[1]} → {row[2]}.{row[3]}  (3NF maintained via FK)")

    print("=" * 65)


# ============================================================
#  UPDATE MENU — add new options to existing menu
# ============================================================

def full_menu():
    while True:
        print("""
╔══════════════════════════════════════════════════════════════╗
║        HOSPITAL MANAGEMENT — COMPLETE SQL SHOWCASE           ║
╠══════════════════════════════════════════════════════════════╣
║  ── VIEW ──────────────────────────────────────────────────  ║
║  1.  Show All Appointments (via VIEW)                        ║
║  2.  Search Patient Details (via VIEW)                       ║
║                                                              ║
║  ── STORED PROCEDURES ─────────────────────────────────────  ║
║  3.  Search Doctors by Department (Stored Proc)              ║
║  4.  Get Patient Bill (Stored Proc)                          ║
║                                                              ║
║  ── TRIGGER ───────────────────────────────────────────────  ║
║  5.  Delete Patient (Trigger auto-logs it)                   ║
║  6.  Show Audit Log (Trigger proof)                          ║
║                                                              ║
║  ── WINDOW FUNCTIONS ──────────────────────────────────────  ║
║  7.  Doctor Ranking by Patients (RANK OVER)                  ║
║  8.  Department Analytics (SUM OVER, AVG OVER)               ║
║  9.  Running Total of Appointments (SUM OVER ORDER)          ║
║  10. Visit Comparison — LAG & LEAD                           ║
║                                                              ║
║  ── INDEX ─────────────────────────────────────────────────  ║
║  11. Create Indexes (B+ Tree)                                ║
║  12. Show All Indexes (SHOW INDEX)                           ║
║  13. EXPLAIN Query — Execution Plan Demo                     ║
║                                                              ║
║  ── CTE ───────────────────────────────────────────────────  ║
║  14. Basic CTE — Top Earning Doctors                         ║
║  15. Multiple CTEs — Top Doctor per Department               ║
║  16. Recursive CTE — Series Generation                       ║
║                                                              ║
║  ── NULL HANDLING ─────────────────────────────────────────  ║
║  17. NULL Handling Demo (IS NULL, COALESCE, NULLIF)          ║
║                                                              ║
║  ── SUBQUERY PATTERNS ─────────────────────────────────────  ║
║  18. Subquery Patterns (Scalar, IN, EXISTS, Correlated)      ║
║                                                              ║
║  ── UNION / REGEX / NORMALIZATION ─────────────────────────  ║
║  19. UNION vs UNION ALL Demo                                 ║
║  20. REGEX Demo (REGEXP patterns)                            ║
║  21. Normalization Demo (1NF, 2NF, 3NF on our tables)        ║
║                                                              ║
║  ── SETUP ─────────────────────────────────────────────────  ║
║  0.  First-Time Setup (VIEW / PROC / TRIGGER banana)         ║
║  99. Exit                                                    ║
╚══════════════════════════════════════════════════════════════╝""")

        try:
            choice = int(input("\n  Enter choice: "))
        except ValueError:
            print("  Enter a valid number.")
            continue

        if   choice == 0:  setup_advanced_sql()
        elif choice == 1:  show_all_appointments_via_view()
        elif choice == 2:  search_patient_via_view()
        elif choice == 3:  search_doctors_by_department()
        elif choice == 4:  get_patient_bill_via_procedure()
        elif choice == 5:  delete_patient_with_trigger_demo()
        elif choice == 6:  show_audit_log()
        elif choice == 7:  doctor_patient_ranking()
        elif choice == 8:  department_wise_stats()
        elif choice == 9:  running_total_appointments()
        elif choice == 10: lag_lead_appointments()
        elif choice == 11: create_indexes()
        elif choice == 12: show_indexes()
        elif choice == 13: explain_query_demo()
        elif choice == 14: cte_basic_demo()
        elif choice == 15: cte_multiple_demo()
        elif choice == 16: cte_recursive_demo()
        elif choice == 17: null_handling_demo()
        elif choice == 18: subquery_patterns_demo()
        elif choice == 19: union_demo()
        elif choice == 20: regex_demo()
        elif choice == 21: normalization_demo()
        elif choice == 99:
            print("\n  Goodbye! 👋\n")
            break
        else:
            print("  Invalid choice.")


# Override entry point to use full menu
if __name__ == "__main__":
    full_menu()