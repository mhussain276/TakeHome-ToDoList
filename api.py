from flask import Flask, request, jsonify  # Import necessary modules from Flask

app = Flask(__name__)  # Create a Flask app instance

todo_items = {}  # Dictionary to store tasks: {id: {'name': ..., 'priority': ...}}
next_id = 1      # Counter to assign unique IDs to tasks

# Custom function to return priority for sorting
def get_priority(task_tuple):
    # task_tuple is (id, {'name': ..., 'priority': ...})
    return task_tuple[1]['priority']

# Route to add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    global next_id  # Use the global next_id to keep ID count consistent
    data = request.get_json()  # Get the JSON data from the POST request
    name = data.get('name')  # Extract task name
    priority = data.get('priority')  # Extract task priority

    # Validate task input
    if not name or not isinstance(priority, int) or priority <= 0:
        return jsonify({'error': 'Invalid task data'}), 400  # Return error if input is invalid

    # Store the new task in the dictionary
    todo_items[next_id] = {'name': name, 'priority': priority}
    next_id += 1  # Increment the ID for the next task
    return jsonify({'message': 'Task added'}), 201  # Success response

# Route to list all tasks, sorted by priority
@app.route('/tasks', methods=['GET'])
def list_tasks():
    # Sort tasks using the custom get_priority function
    sorted_tasks = sorted(todo_items.items(), key=get_priority)

    # Return tasks as JSON list, adding the ID to each task
    tasks_with_id = []
    for task_id, data in sorted_tasks:
        task = {'id': task_id, 'name': data['name'], 'priority': data['priority']}
        tasks_with_id.append(task)

    return jsonify(tasks_with_id)

# Route to delete a specific task by its ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id in todo_items:
        del todo_items[task_id]  # Delete the task
        return jsonify({'message': 'Task deleted'}), 200  # Success message
    return jsonify({'error': 'Task not found'}), 404  # Error if ID doesn't exist

# Route to view missing priorities in the task list
@app.route('/tasks/missing_priorities', methods=['GET'])
def missing_priorities():
    if not todo_items:
        return jsonify({'missing_priorities': []})  # If no tasks, return empty list

    priorities = [item['priority'] for item in todo_items.values()]  # Collect all priorities
    max_priority = max(priorities)  # Get the highest priority number
    existing_set = set(priorities)  # Convert list to set to remove duplicates

    # Find missing integers between 1 and max_priority
    missing = [p for p in range(1, max_priority + 1) if p not in existing_set]
    return jsonify({'missing_priorities': missing})  # Return the missing ones

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)
