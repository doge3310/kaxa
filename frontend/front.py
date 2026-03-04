import os
from interfaces import get_messages, get_users, send_message, register, login, delete_user


class UserAccount:
    def __init__(self):
        self.token = None
        self.ip = "192.168.1.7"

        self.menu = [
            "register (r)",
            "login (l)",
            "send message (s)",
            "get all users (u)",
            "delete me and messages (d)",
            "my messages (m)",
            "quit (q)"
        ]

    def run(self):
        while True:
            os.system('cls')

            if not self.token:
                print("\n".join(self.menu[0:2]))

            else:
                print(f"\nLogged in as: {self.current_user}")
                print("\n".join(self.menu[2:]) + "\n")

            choice = input("your choice: ").lower()

            if choice == 'r' and not self.token:
                self._register()

            elif choice == 'l' and not self.token:
                self._login()

            elif choice == 's' and self.token:
                self._send_message()

            elif choice == 'u' and self.token:
                self._get_users()

            elif choice == 'd' and self.token:
                self._delete_user()

            elif choice == 'm' and self.token:
                self._get_messages()

            elif choice == 'q':
                break

            else:
                print("Invalid choice or not logged in!")
                input("Press Enter to continue...")

    def _register(self):
        name = input("Enter username: ")
        password = input("Enter password: ")

        try:
            register(self.ip, name, password)
            print("Registration successful!")

        except Exception as e:
            print(f"Registration failed: {e}")

        input("Press Enter to continue...")

    def _login(self):
        name = input("Enter username: ")
        password = input("Enter password: ")

        try:
            self.token = login(self.ip, name, password)
            self.current_user = name

            print("Login successful!")

        except Exception as e:
            print(f"Login failed: {e}")

        input("Press Enter to continue...")

    def _send_message(self):
        to_user = input("Enter recipient: ")
        message = input("Enter message: ")

        try:
            send_message(self.ip, self.token, self.current_user, to_user, message)
            print("Message sent!")

        except Exception as e:
            print(f"Failed to send message: {e}")

        input("Press Enter to continue...")

    def _get_users(self):
        try:
            users = get_users(self.ip, self.token)
            print("\nAll users:")

            for user in users:
                print(f"- {user}")

        except Exception as e:
            print(f"Failed to get users: {e}")

        input("Press Enter to continue...")

    def _delete_user(self):
        password = input("Enter password to confirm deletion: ")

        try:
            delete_user(self.ip, self.token, self.current_user, password)
            self.token = None
            self.current_user = None

            print("User deleted successfully!")

        except Exception as e:
            print(f"Failed to delete user: {e}")

        input("Press Enter to continue...")

    def _get_messages(self):
        try:
            messages = get_messages(self.ip, self.token)
            print("\nYour messages:")

            for msg in messages:
                print(f"From: {msg[1]}, To: {msg[2]}, Text: {msg[0]}, Time: {msg[-1]}")

        except Exception as e:
            print(f"Failed to get messages: {e}")

        input("Press Enter to continue...")


if __name__ == "__main__":
    user = UserAccount()
    user.run()
