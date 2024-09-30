from flask import Flask, render_template, request
from openai import OpenAI
import google.generativeai as genai

app = Flask(__name__)

# Define the homepage route
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        api_key = request.form.get('api_key')
        prompt = request.form.get('prompt')
        essay = request.form.get('essay')
        model_choice = request.form.get('model_choice')  # Get the chosen model

        if model_choice == "openai":
            # Initialize OpenAI client with the provided API key
            client = OpenAI(api_key=api_key)

            system = '''You are an expert IELTS Writing examiner with years of experience. Your task is to evaluate IELTS Writing essays and provide band scores for the four criteria: Task Response (TR), Coherence and Cohesion (CC), Lexical Resource (LR), and Grammatical Range and Accuracy (GRA). Strictly follow the band descriptors to give the accurate estimated band score for each criterion. Don't hesitate to penalize any mistakes related to Task Response and Coherence & Cohesion criteria.'''

            # Make the request to OpenAI API
            try:
                completion = client.chat.completions.create(
                model="ft:gpt-4o-2024-08-06:youpass::ABIsYLJc",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": f"""Please rely on the criteria and scoring method of an IELTS writing test to give a predicted score for my writing.
                    Prompt: {prompt}
                    Essay: {essay}"""}]
                )
                result = completion.choices[0].message.content
            except Exception as e:
                result = f"Error: {str(e)}"

        elif model_choice == "gemini":
            # Configure Google Gemini API
            genai.configure(api_key=api_key)
            # Set up Gemini model configuration
            generation_config = {
              "temperature": 0,
              "top_p": 0.0,
              "top_k": 10,
              "max_output_tokens": 8192,
              "response_mime_type": "text/plain",
            }

            # Create the Gemini model
            model = genai.GenerativeModel(
              model_name="tunedModels/datatraingeminiv2-gq8pcv0xyvi7",
              generation_config=generation_config,
            )

            system = 'You are an expert IELTS Writing examiner with years of experience. Your task is to evaluate IELTS Writing essays and provide band scores for the four criteria: Task Response (TR), Coherence and Cohesion (CC), Lexical Resource (LR), and Grammatical Range and Accuracy (GRA).'

            # Make the request to Gemini API
            try:
                chat_session = model.start_chat(
                  history=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": f"""Please rely on the criteria and scoring method of an IELTS writing test to give a predicted score for my writing.
                    Prompt: {prompt}
                    Essay: {essay}"""}]
                )
                result = chat_session.generate().message  # Assume it returns a 'message' field
            except Exception as e:
                result = f"Error: {str(e)}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
