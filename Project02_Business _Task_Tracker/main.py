class TechTask:
    def __init__(self, task_name, assigned_to):
        self.task_name = task_name
        self.assigned_to = assigned_to
        self.is_completed = False  # New tasks start as not finished

    def complete_task(self):
        self.is_completed = True
        return f"Success! {self.task_name} is now finished."

    def get_status(self):
        if self.is_completed:
            return f"{self.task_name} is DONE."
        else:
            return f"{self.task_name} is still PENDING. {self.assigned_to} is working on it."

# --- PRACTICE STEPS ---

# 1. Create a task for yourself to "Master FastAPI"
my_task = TechTask("Master FastAPI", "Alex")

# 2. Create a task for Samuel to "Register LLC"
friend_task = TechTask("Register LLC", "Samuel")

# 3. Print the status of your task
print(my_task.get_status())