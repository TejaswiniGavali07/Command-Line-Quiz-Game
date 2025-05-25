import json
import random

QUE_FILE = 'questions.json'
GUESS_LIMIT = 2
scoreboard = []  

def load_questions():
    try:
        with open(QUE_FILE, 'r') as f:
            content = f.read().strip()
            if content:
                return json.loads(content)
    except:
        pass
    return []

def save_questions(questions):
    with open(QUE_FILE, 'w') as f:
        json.dump(questions, f, indent=4)

def add_question():
    q = input("Enter the question: ")
    options = []
    for i in range(4):
        options.append(input(f"Option {i + 1}: "))
    ans = input("Enter the correct option number (1-4): ")
    score = input("Assign a score for this question: ")

    if ans in ['1', '2', '3', '4'] and score.isdigit():
        question = {
            "question": q,
            "options": options,
            "answer": ans,
            "score": int(score)
        }
        questions = load_questions()
        questions.append(question)
        save_questions(questions)
        print("✅ Question added successfully.")
    else:
        print("❌ Invalid input. Question not added.")

def get_score(entry):
    return entry['score']

def view_scoreboard():
    if scoreboard:
        print("==== Scoreboard ====")
        sorted_scores = sorted(scoreboard, key=get_score, reverse=True)
        for i, entry in enumerate(sorted_scores, start=1):
            print(f"{i}. {entry['name']} - {entry['score']} points")
        print("====================")
    else:
        print("⚠️ No scores yet.")

def start_quiz():
    questions = load_questions()
    if not questions:
        print("No questions available.")
        return

    score = 0
    combo = 0

    random.shuffle(questions)  

    for q in questions:
        print("\n" + q["question"])
        for idx, opt in enumerate(q["options"], 1):
            print(f"{idx}. {opt}")
        
        guesses_left = GUESS_LIMIT
        answered_correctly = False
        question_score = q.get("score", 1)  

        while guesses_left > 0 and not answered_correctly:
            ans = input("Your answer (1-4): ")
            if ans not in ['1', '2', '3', '4']:
                print("❗Invalid option. Please enter a number between 1 and 4.")
                continue
            if ans == q["answer"]:
                combo += 1
                earned = question_score * combo
                print(f"✅ Correct! (+{earned} points, combo x{combo})")
                score += earned
                answered_correctly = True
            else:
                guesses_left -= 1
                combo = 0
                if guesses_left > 0:
                    print(f"❌ Wrong! Try again ({guesses_left} guesses left).")
                else:
                    print("❌ No attempts left. Moving to next question.")

    print(f"\n 🎉 Total score: {score} points")
    name = input("Enter your name to record your score: ")
    scoreboard.append({"name": name, "score": score})

def main():
    while True:
        print("""
===== Quiz App Menu =====
1. Start Quiz
2. Add a Question
3. View Scoreboard
4. Exit
===========================
""")
        option = input("Enter your choice (1-4): ")
        if option  == '1':
            start_quiz()
        elif option  == '2':
            add_question()
        elif option  == '3':
            view_scoreboard()
            print("Goodbye!")
        elif option == '4':
            print("👋 Thanks for playing!")
            break
        else:
            print(" ⚠️ Invalid choice. Please select from 1 to 4.")

if __name__ == "__main__":
    main()
