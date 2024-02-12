import os
from flask import Blueprint, jsonify, request
from openai import OpenAI

api_key=os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# Define your OpenAI API key

# Check if the API key is set
if not client.api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

ai_api = Blueprint('ai_api', __name__, url_prefix='/api/ai')

@ai_api.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    
    # Check if all required parameters are provided
    if 'model' not in data or 'prompt' not in data:
        return jsonify({'error': 'Missing required parameters. Expected "model" and "prompt".'}), 400
    
    model = data['model']
    user_prompt = data['prompt']
    temperature = data.get('temperature', 0.7)  # default value of 0.7 if not provided
    max_tokens = data.get('max_tokens', 100)    # default value of 100 if not provided
    
    system_prompt='answer the question in at most 30 words'
    prompt=f"""
    system prompt: {system_prompt}
    user prompt={user_prompt}
    """

    messages=[
        {'role':'system', 'content':system_prompt},
        {'role':'user', 'content':user_prompt}
    ]

    # Send the question to the OpenAI API
    response = client.chat.completions.create(
        model=model,
        # prompt=prompt,
        messages= messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    #answer = response.choices[0].text.strip()
    answer = 'no response'
    if (response and 
        response.choices and
        len(response.choices) > 0 and 
        response.choices[0].message and 
        response.choices[0].message.content):
        
        answer = response.choices[0].message.content.strip()
    
    return jsonify({'answer': answer})