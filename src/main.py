from logic import *

def admin_login():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    if username and password:
        print("Login successful!")
        return True
    else:
        print("Invalid login.")
        return False

def view_menu():
    while True:
        print("\n=== View Data ===")
        print("1. List All Members")
        print("2. List Inactive Members")
        print("3. View Expiring Memberships")
        print("4. Back to Main Menu")
        print("5. Export Inactive Members CSV")
        print("6. Export Monthly Revenue CSV")

        choice = input("Enter your choice: ")

        if choice == "1":
            list_members()
        elif choice == "2":
            list_inactive_members()
        elif choice == "3":
            expiring = get_expiring_members()
            if not expiring:
                print("No memberships expiring in the next 7 days.")
            else:
                print("Members expiring soon:")
                for m in expiring:
                    print(f"{m['id']} - {m['name']} (expires {m['end_date']})")
        elif choice == "4":
            break
        elif choice == "5":
            export_inactive_members_csv()
        elif choice == "6":
            export_monthly_revenue_csv()
        else:
            print("Invalid choice. Please try again.")

def edit_menu():
    if not admin_login():
        return

    while True:
        print("\n=== Edit Data (Admin) ===")
        print("1. Add Member")
        print("2. Remove Member")
        print("3. Add Payment")
        print("4. Upgrade/Downgrade Member Plan")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_member()
        elif choice == "2":
            remove_member_ui()
        elif choice == "3":
            make_payment()
        elif choice == "4":
            member_id = input("Enter Member ID: ")
            new_plan_id = int(input("Enter New Plan ID: "))
            update_member_plan(member_id, new_plan_id)
            print(f"Member {member_id} plan updated to {new_plan_id}")
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    while True:
        print("\n=== Gym Management System ===")
        print("1. View Data")
        print("2. Edit Data (Admin Only)")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_menu()
        elif choice == "2":
            edit_menu()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

