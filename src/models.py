from db import get_connection
import sqlite3
import bcrypt

def insert_member(name, email, phone, plan_id, start_date, is_active=1):
   conn = get_connection()
   cursor = conn.cursor()
   cursor.execute("""
       INSERT INTO members (name, email, phone, plan_id, start_date, is_active)
       VALUES (?, ?, ?, ?, ?, ?)
   """, (name, email, phone, plan_id, start_date, is_active))
   conn.commit()
   conn.close()


def get_all_members():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def remove_member(member_id):
   conn = get_connection()
   cursor = conn.cursor()
   cursor.execute("DELETE FROM members WHERE id=?", (member_id,))
   conn.commit()
   conn.close()
def update_member_plan(member_id, new_plan_id):
   conn = get_connection()
   cursor = conn.cursor()
   cursor.execute("UPDATE members SET plan_id=? WHERE id=?", (new_plan_id, member_id))
   conn.commit()
   conn.close()
def update_member_status():
   conn = get_connection()
   cursor = conn.cursor()
   cursor.execute("UPDATE members SET is_active=0 WHERE end_date < date('now')")
   conn.commit()
   conn.close()
def get_expiring_members(days=7):
   conn = get_connection()
   cursor = conn.cursor()
   cursor.execute("""
       SELECT * FROM members
       WHERE end_date BETWEEN date('now') AND date('now', ? || ' days')
   """, (days,))
   results = [dict(row) for row in cursor.fetchall()]
   conn.close()
   return results
def insert_payment(member_id, date_paid, amount, plan_id):
   conn = get_connection()
   cursor = conn.cursor()
   cursor.execute("""
       INSERT INTO payments (member_id, date, amount, plan_id)
       VALUES (?, ?, ?, ?)
   """, (member_id, date_paid, amount, plan_id))
   conn.commit()
   conn.close()
def get_monthly_revenue():
   conn = get_connection()
   cursor = conn.cursor()
   cursor.execute("""
       SELECT strftime('%m', date) AS month, SUM(amount) AS revenue
       FROM payments
       GROUP BY strftime('%m', date)
   """)
   results = [dict(row) for row in cursor.fetchall()]
   conn.close()
   return results
def flag_inactive_members(min_checkins=4):
   conn = get_connection()
   cursor = conn.cursor()
   cursor.execute("""
       SELECT m.id, m.name, COUNT(c.id) AS checkin_count
       FROM members m
       LEFT JOIN checkins c ON m.id = c.member_id
       WHERE c.checkin_time >= date('now', '-1 month')
       GROUP BY m.id, m.name
       HAVING COUNT(c.id) < ?
   """, (min_checkins,))
   results = [dict(row) for row in cursor.fetchall()]
   conn.close()
   return results

def insert_admin(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    try:
        cursor.execute("""
            INSERT INTO admins (username, password_hash)
            VALUES (?, ?)
        """, (username, hashed))
        conn.commit()
        print("Admin added successfully.")
    except sqlite3.IntegrityError:
        print("Username already exists. Please choose another one.")
    finally:
        conn.close()

def check_admin(username, password):
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT username FROM admins WHERE username = ?", (username,))
  result = cursor.fetchone()
  if result == None:
    print("Username not found.")
    return False

  cursor.execute("SELECT password_hashed FROM admins WHERE username = ?", (username,))
  the_password = cursor.fetchone()
  if not bcrypt.checkpw(password.encode('utf-8'), the_password):
    print("Password incorrect.")
    return False

  return True