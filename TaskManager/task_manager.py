import sqlite3

# Function to create a new task
def create_task(conn, task):
    sql = '''INSERT INTO tasks(name, status)
             VALUES(?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid



# Function to mark a task as completed
def complete_task(conn, task_id):
    sql = '''UPDATE tasks
             SET status = 'Completed'
             WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (task_id,))
    conn.commit()



# Function to retrieve all tasks
def get_all_tasks(conn):
    sql = 'SELECT * FROM tasks'
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows



# Function to delete a task
def delete_task(conn, task_id):
    sql = '''DELETE FROM tasks
             WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (task_id,))
    conn.commit()



# Connect to the database
conn = sqlite3.connect('tasks.db')



# Create the tasks table if it doesn't exist
create_table_sql = '''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        status TEXT NOT NULL
                    );'''
conn.execute(create_table_sql)



# Main program loop
while True:
    print("1. Add Task")
    print("2. Complete Task")
    print("3. View All Tasks")
    print("4. Delete Task")
    print("5. Quit")

    choice = input("Enter your choice (1-5): ")

    if choice == '1':
        task_name = input("Enter task name: ")
        task_status = 'Incomplete'
        task = (task_name, task_status)
        create_task(conn, task)
        print("Task created successfully!")

    elif choice == '2':
        task_id = int(input("Enter task ID to mark as completed: "))
        complete_task(conn, task_id)
        print("Task marked as completed!")

    elif choice == '3':
        tasks = get_all_tasks(conn)
        if len(tasks) == 0:
            print("No tasks found.")
        else:
            print("ID\tName\t\tStatus")
            for task in tasks:
                print(f"{task[0]}\t{task[1]}\t\t{task[2]}")

    elif choice == '4':
        task_id = int(input("Enter task ID to delete: "))
        delete_task(conn, task_id)
        print("Task deleted successfully!")

    elif choice == '5':
        break

    else:
        print("Invalid choice. Please try again.")

# Close the database connection
conn.close()
