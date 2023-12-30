import json
from difflib import get_close_matches

# load the knowledge base from a JSON file

# Function to load the knowledge base from a JSON file
def load_knowledge_base(file_path: str):
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# Function to save the knowledge base to a JSON file
def save_knowledge_base(file_path:str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Function to find the best match for a user's question from a list of existing questions
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Function to get the answer for a given question from the knowledge base
def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

# Main chatbot function
def chat_bot():
    # Load the knowledge base initially
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        # Get user input
        user_input: str = input('You: ')

        # Check if the user wants to quit
        if user_input.lower() == 'quit':
            break

        # Find the best match for the user's input in the knowledge base questions
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            # If there's a match, get the answer from the knowledge base
            answer: str | None = get_answer_for_question(best_match, knowledge_base)
            if answer:
                print(f'Bot: {answer}')
            else:
                # If there's no answer, ask the user to provide one and add it to the knowledge base
                print('Bot: I don\'t know the answer. Can you teach me?')
                new_answer: str = input('Type the answer or "skip" to skip: ')

                if new_answer.lower() != 'skip':
                    knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    print('Bot: Thank you! I learned a new response!')
                else:
                    print('Bot: Skipped adding the response.')

        else:
            # If there's no match, ask the user to provide an answer and add it to the knowledge base
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learned a new response!')
            else:
                print('Bot: Skipped adding the response.')

# Start the chatbot
chat_bot()
