from query import answer_question

def main():
    while True:
        question = input("\nAsk a question (or type exit): ")
        if question.lower() == "exit":
            break

        context, answer = answer_question(question)

        print("\n--- Retrieved Context ---")
        print(context)
        print("\n--- Answer ---")
        print(answer)

if __name__ == "__main__":
    main()
    