from db import MyFlashcards


class Flashcards:
    def __init__(self):
        self.main_menu_text = "1. Add flashcards\n2. Practice flashcards\n3. Exit"
        self.add_menu_text = "1. Add a new flashcard\n2. Exit"
        self.current_data_list = list()

    def get_current_data(self):
        return MyFlashcards.find_all()

    @staticmethod
    def add_question_answer():
        question, answer = "", ""
        while not question.strip():
            question = input("Question:\n")
        while not answer.strip():
            answer = input("Answer:\n\n")
        MyFlashcards.add_new_row(question, answer)


    def menu(self):
        while True:
            print(self.main_menu_text)
            choice = input()
            if choice == '1':
                self.add_menu()
            elif choice == '2':
                self.practice_menu()
            elif choice == '3':
                print("Bye!")
                exit()
            else:
                print(f"{choice} is not an option")

    def add_menu(self):
        while True:
            print(self.add_menu_text)
            choice = input()
            if choice == '1':
                self.add_question_answer()
            elif choice == '2':
                self.menu()
            else:
                print(f"{choice} is not an option")

    def edit_menu(self, row_id):
        while True:
            choice = input('press "d" to delete the flashcard:\npress "e" to edit the flashcard:\n\n')
            if choice == 'd':
                MyFlashcards.delete_flashcard(row_id)
                break
            elif choice == 'e':
                MyFlashcards.edit_flashcard(row_id)
                break
            else:
                print(f"{choice} is not an option")

    def learning_menu(self, row_id):
        while True:
            choice = input('press "y" if your answer is correct:\npress "n" if your answer is wrong:\n')
            if choice == 'y':
                MyFlashcards.update_box_value(row_id, +1)
                break
            elif choice == 'n':
                MyFlashcards.update_box_value(row_id, -1)
                break
            else:
                print(f"{choice} is not an option")

    def practice_menu(self):
        self.current_data_list = self.get_current_data()
        if not self.get_current_data():
            print("\nThere is no flashcard to practice!\n")
            self.menu()

        for row in self.current_data_list:
            print(f'Question: {row.question}')
            while True:
                choice = input('press "y" to see the answer:\npress "n" to skip:\npress "u" to update:\n\n')
                if choice == 'y':
                    print(f'Answer: {row.answer}')
                    self.learning_menu(row.id)
                    break
                elif choice == 'n':
                    break
                elif choice == 'u':
                    self.edit_menu(row.id)
                    break
                else:
                    print(f"{choice} is not an option")
            MyFlashcards.delete_learnt()
        self.menu()
