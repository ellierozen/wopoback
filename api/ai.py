import os
from flask import Blueprint, jsonify, request
import openai

# Define your OpenAI API key
openai.api_key = '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'

# Check if the API key is set
if not openai.api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

ai_api = Blueprint('ai_api', __name__, url_prefix='/api/ai')

@ai_api.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data['question']
    
    # Send the question to the OpenAI API
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Question: {question}\nAnswer:",
        temperature=0.7,
        max_tokens=100
    )
    answer = response.choices[0].text.strip()
    
    return jsonify({'answer': answer})

