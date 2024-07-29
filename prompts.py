import openai
import os
import time
from langchain_core.prompts import PromptTemplate

api_key = os.getenv('OPENAI_API_KEY') 
azure_endpoint = "https://hv-openai-lab47.openai.azure.com/"
api_version = "2024-02-15-preview"
deployment_name = "gpt-4o"

openai.api_type = "azure"
openai.api_base = azure_endpoint
openai.api_version = api_version
openai.api_key = api_key

registration_prompt = PromptTemplate(
    input_variables=["username", "training_type"],
    template="Register user with username: {username}, training type: {training_type}."
)

workout_logging_prompt = PromptTemplate(
    input_variables=["username", "workout_details"],
    template="Log workout for user {username}: {workout_details}."
)

progress_tracking_prompt = PromptTemplate(
    input_variables=["username", "measurements"],
    template="Track progress for user {username}. Current measurements: {measurements}."
)

diet_recommendation_prompt = PromptTemplate(
    input_variables=["username", "training_type", "measurements"],
    template="Provide specific meal recommendations for breakfast, lunch, and dinner for user {username} based on their training type: {training_type} and current measurements: {measurements}. Include nutritional information and portion sizes."
)

def run_prompt(prompt_template, **kwargs):
    prompt = prompt_template.format(**kwargs)
    max_retries = 5
    wait_time = 4
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                deployment_id=deployment_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            return response.choices[0].message['content'].strip()
        except openai.error.RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(wait_time)
                wait_time *= 2 
            else:
                return "Rate limit exceeded. Please try again later."
        except Exception as e:
            return f"Error during API request: {str(e)}"
