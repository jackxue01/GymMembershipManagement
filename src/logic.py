from models import insert_member, get_all_members, flag_inactive_members, insert_payment, update_member_status, get_expiring_members, update_member_plan
import csv
from db import *

def add_member():
    name = input("Enter name: ")
    email = input("Enter email: ")
    phone = input("Enter phone: ")
    plan_id = int(input("Enter plan ID: "))
    start_date = input("Enter start date (YYYY-MM-DD): ")
    insert_member(name, email, phone, plan_id, start_date)
    print("Member added successfully!")

def list_members():
    update_member_status()
    members = get_all_members()
    for member in members:
        print(member)

def make_payment():
    member_id = input("Enter member ID: ")
    date_paid = input("Enter the date (YYYY-MM-DD): ")
    plan_id = input("Enter the plan ID: ")
    amount = input("Enter the amount: ")
    insert_payment(member_id, date_paid, amount, plan_id)
    print("Payment added successfully!")

def list_inactive_members(min_checkins=4):
    inactive_members = flag_inactive_members(min_checkins)
    if not inactive_members:
        print("No inactive members found in the last month.")
        return

    print("Inactive Members (low check-ins in the past month):")
    for member in inactive_members:
        print(f"ID: {member['id']}, Name: {member['name']}, Check-ins: {member['checkin_count']}")

def remove_member_ui():
    member_id = input("Enter the member ID to remove: ")
    all_members = get_all_members()
    member_exists = any(str(member['id']) == member_id for member in all_members)

    if not member_exists:
        print(f"No member found with ID {member_id}.")
        return

    remove_member(member_id)
    print(f"Member ID {member_id} removed successfully!")

def export_inactive_members_csv(filename="inactive_members.csv", min_checkins=4):
    inactive_members = flag_inactive_members(min_checkins)
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "checkin_count"])
        writer.writeheader()
        writer.writerows(inactive_members)
    print(f"Inactive members exported to {filename}")

def export_monthly_revenue_csv(filename="monthly_revenue.csv"):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT MONTH(date) AS month, SUM(amount) AS revenue FROM payments GROUP BY MONTH(date)")
    revenue = cursor.fetchall()
    conn.close()
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["month", "revenue"])
        writer.writeheader()
        writer.writerows(revenue)
    print(f"Monthly revenue exported to {filename}")
