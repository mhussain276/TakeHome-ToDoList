import requests  # Library for making HTTP requests

# Base URL of the Flask API
BASE_URL = "http://127.0.0.1:5000"

class TodoCLI:
    # Display the main menu
    def show_menu(self):
        print("\n-- ToDo CLI App (via API) --")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Delete Task")
        print("4. View Missing Priorities")
        print("5. Exit")

    # Add a new task via POST request
    def add_task(self):
        name = input("Enter task name: ").strip()  # Get task name
        try:
            priority = int(input("Enter task priority (positive integer): "))  # Get and validate priority
        except ValueError:
            print("Invalid priority.")  # Handle invalid input
            return

        # Send POST request to add task
        response = requests.post(f"{BASE_URL}/tasks", json={"name": name, "priority": priority})
        # Print response message
        print(response.json().get("message", response.json().get("error", "Unknown error")))

    # List all tasks from the API
    def list_tasks(self):
        response = requests.get(f"{BASE_URL}/tasks")  # GET request for task list
        if response.status_code == 200:
            tasks = response.json()  # Parse response JSON
            if not tasks:
                print("No tasks.")
                return
            # Display each task with ID, name, and priority
            for task in tasks:
                print(f"(ID: {task['id']}) (task: {task['name']}) (priority:[{task['priority']}])")
        else:
            print("Error fetching tasks.")

    # Delete a task using its ID
    def delete_task(self):
        try:
            task_id = int(input("Enter task ID to delete: "))  # Get ID input
        except ValueError:
            print("Invalid ID.")  # Handle non-integer input
            return

        # Send DELETE request
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        # Print message from API
        print(response.json().get("message", response.json().get("error", "Unknown error")))

    # View missing priorities by calling the API
    def view_missing_priorities(self):
        response = requests.get(f"{BASE_URL}/tasks/missing_priorities")  # GET request
        if response.status_code == 200:
            missing = response.json()["missing_priorities"]
            if missing:
                print("Missing priorities:", missing)
            else:
                print("No missing priorities.")
        else:
            print("Error retrieving missing priorities.")

    # Main loop to run the CLI
    def run(self):
        while True:
            self.show_menu()  # Show options
            choice = input("Choose an option (1-5): ").strip()  # Get user's choice

            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.list_tasks()
            elif choice == '3':
                self.delete_task()
            elif choice == '4':
                self.view_missing_priorities()
            elif choice == '5':
                print("Thanks for using the API-based ToDo App!")
                break
            else:
                print("Invalid option.")

# Entry point for the CLI app
if __name__ == '__main__':
    cli = TodoCLI()
    cli.run()
