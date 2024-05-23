from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Set your OpenAI GPT-3 Turbo API key
openai.api_key = 'api key'

def generate_script(character_count, main_character, side_character, villain, scene_description, scene_type, output_length):
    prompt = f"Generate a {scene_type} story with a main character: {main_character}, side character: {side_character}, villain: {villain}. Scene: {scene_description}. Characters' roles: {main_character} is the main character, {side_character} is a side character, and {villain} is the villain. Limit characters to {character_count}. Length: {output_length} words."

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=output_length,
        temperature=0.7,
        n=1,
        stop=None
    )

    story = response.choices[0].text.strip()

    # Format the story into a script
    formatted_script = format_as_script(main_character, side_character, villain, scene_description, story)

    return formatted_script

def format_as_script(main_character, side_character, villain, scene_description, story):
    script = f'Title: "{scene_description}"\n\nINT. {scene_description.upper()} - DAY\n\n'
    characters = [main_character, side_character, villain]

    for paragraph in story.split('\n\n'):
        for line in paragraph.split('\n'):
            if any(character in line for character in characters):
                script += f"{line}\n\n"
            else:
                script += f"{main_character} (voiceover)\n\t{line}\n\n"

    script += "FADE OUT."

    return script

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        character_count = 5
        main_character = request.form['main_character'][:5]
        side_character = request.form['side_character'][:5]
        villain = request.form['villain'][:5]
        scene_description = request.form['scene_description']
        scene_type = request.form['scene_type'].lower()
        output_length = 800

        script = generate_script(character_count, main_character, side_character, villain, scene_description, scene_type, output_length)
        return render_template('index.html', script=script)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
