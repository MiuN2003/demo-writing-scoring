from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

# Define the homepage route
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        api_key = request.form.get('api_key')
        prompt = request.form.get('prompt')
        essay = request.form.get('essay')

        # Initialize OpenAI client with the provided API key
        client = OpenAI(api_key=api_key)

        system = '''You are an expert IELTS Writing examiner with years of experience. Your task is to evaluate IELTS Writing essays and provide band scores for the four criteria: Task Response (TR), Coherence and Cohesion (CC), Lexical Resource (LR), and Grammatical Range and Accuracy (GRA). Strictly follow the band desciptors to give the accurate estimated band score for each criterion. Don't hesitate to penalize any mistakes related to Task Response and Coherence & Cohesion criteria.'''

        # Make the request to OpenAI API
        try:
            completion = client.chat.completions.create(
            model="ft:gpt-4o-2024-08-06:personal::A8L7YujV",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": f"""Please rely on the criteria and scoring method of an IELTS writing test to give a predicted score for my writing.
                Prompt: {prompt}
                Essay: {essay}"""}]
            )
            result = completion.choices[0].message.content
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
