import random


def get_random_challenge():

    # Randomly choose a challenge
    challenge_type = random.choice([
        "math",
        "color"
    ])

    # -------------------------
    # MATH CHALLENGE
    # -------------------------

    if challenge_type == "math":

        num1 = random.randint(2, 10)
        num2 = random.randint(2, 10)

        answer = num1 + num2

        return {
            "type": "math",
            "question": f"What is {num1} + {num2}?",
            "answer": answer
        }

    # -------------------------
    # COLOR CHALLENGE
    # -------------------------

    else:

        colors = ["RED", "BLUE", "GREEN", "YELLOW"]

        correct_color = random.choice(colors)

        return {
            "type": "color",
            "question": f"Type the color: {correct_color}",
            "answer": correct_color
        }


# Test the challenge engine
if __name__ == "__main__":

    challenge = get_random_challenge()

    print("Challenge:")
    print(challenge["question"])

    print("Answer:")
    print(challenge["answer"])