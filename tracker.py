import bcrypt
from database import create_connection
from prompts import registration_prompt, workout_logging_prompt, progress_tracking_prompt, diet_recommendation_prompt, run_prompt

class FitnessTracker:
    def __init__(self):
        self.connection = create_connection()

    def register_user(self, username, password, training_type):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return "Username already exists."
        try:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            response = run_prompt(registration_prompt, username=username, training_type=training_type)
            cursor.execute("INSERT INTO users (username, password, training_type) VALUES (%s, %s, %s)", 
                           (username, hashed_password, training_type))
            self.connection.commit()
            return response
        except Exception as e:
            return f"Error during user registration: {str(e)}"

    def log_workout(self, username, workout_details):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if not cursor.fetchone():
            return "User not found."
        try:
            response = run_prompt(workout_logging_prompt, username=username, workout_details=workout_details)
            cursor.execute("INSERT INTO workouts (username, workout_details) VALUES (%s, %s)", 
                           (username, workout_details))
            self.connection.commit()
            return response
        except Exception as e:
            return f"Error during workout logging: {str(e)}"

    def track_progress(self, username, measurements):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if not cursor.fetchone():
            return "User not found."
        try:
            response = run_prompt(progress_tracking_prompt, username=username, measurements=measurements)
            cursor.execute("INSERT INTO measurements (username, measurements) VALUES (%s, %s)", 
                           (username, measurements))
            self.connection.commit()
            return response
        except Exception as e:
            return f"Error during progress tracking: {str(e)}"

    def get_diet_recommendations(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        if not user_data:
            return "User not found."

        try:
            cursor.execute("SELECT measurements FROM measurements WHERE username = %s ORDER BY created_at DESC LIMIT 1", 
                           (username,))
            last_measurements = cursor.fetchone()
            response = run_prompt(
                diet_recommendation_prompt,
                username=username,
                training_type=user_data[2],
                measurements=last_measurements[0] if last_measurements else "No measurements yet"
            )
            return response
        except Exception as e:
            return f"Error during diet recommendation: {str(e)}"

    def get_progress_report(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if not cursor.fetchone():
            return "User not found."

        cursor.execute("SELECT workout_details FROM workouts WHERE username = %s", (username,))
        workouts = cursor.fetchall()

        cursor.execute("SELECT measurements FROM measurements WHERE username = %s", (username,))
        measurements = cursor.fetchall()

        diet_recommendations = self.get_diet_recommendations(username)

        return {
            "workouts": [workout[0] for workout in workouts],
            "measurements": [measurement[0] for measurement in measurements],
            "diet_recommendations": diet_recommendations
        }

    def verify_user(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        stored_hashed_password = cursor.fetchone()
        if not stored_hashed_password:
            return "User not found."
        stored_hashed_password_bytes = stored_hashed_password[0]
        if bcrypt.checkpw(password.encode(), stored_hashed_password_bytes):
            return "Login successful."
        else:
            return "Incorrect password."
