import openai

# Set your OpenAI GPT-3 Turbo API key
openai.api_key = 'YOUR_API_KEY'

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

def main():
    # Get user input
    character_count = 5  # Maximum 5 characters
    main_character = input("Enter the main character's name (up to 5 characters): ")[:5]
    side_character = input("Enter the side character's name (up to 5 characters): ")[:5]
    villain = input("Enter the villain's name (if present, else leave blank): ")[:5]

    scene_description = input("Describe the scene in under 30 words: ")
    while len(scene_description.split()) > 30:
        print("Error: The scene description must be under 30 words.")
        scene_description = input("Describe the scene in under 30 words: ")

    scene_type = input("Enter the type of the scene (happy, sad, angry, horror, normal, romantic): ").lower()
    while scene_type not in ['happy', 'sad', 'angry', 'horror', 'normal', 'romantic']:
        print("Error: Invalid scene type. Please enter a valid scene type.")
        scene_type = input("Enter the type of the scene (happy, sad, angry, horror, normal, romantic): ").lower()

    output_length = 800  # Set the desired output length to 800 tokens

    # Generate the script
    script = generate_script(character_count, main_character, side_character, villain, scene_description, scene_type, output_length)

    # Display the generated script
    print("\nGenerated Script:")
    print(script)

if __name__ == "__main__":
    main()
