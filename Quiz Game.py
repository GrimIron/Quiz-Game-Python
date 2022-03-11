import datetime


# Class for opening the quiz files and getting the question data
class Quizzes:
    # Uses quiz_choice() to generate the which question set to use and what number it would be. e.g 1 or 2
    def __init__(self):
        self.txt, self.choice = self.quiz_choice()  # Gets which question set the user wants
        self.question_number = 0                    # what question the user is on

    # Asks the user to input which question set they would like to play either 1 or 2, and returns the file and what
    # number was chosen.
    def quiz_choice(self):
        print("Which quiz would you like to play? \n"
              "---------------1 or 2----------------\n")
        while True:
            try:
                question_set = int(input("Please enter the number 1 or 2: "))
            except ValueError:
                print("Enter the digit 1 or 2")
                continue

            if question_set == 1:
                file = open("quiz.txt.txt")
                self.txt = file.readlines()
                self.choice = 1
                return self.txt, self.choice

            elif question_set == 2:
                file = open("quiz2.txt")
                self.txt = file.readlines()
                self.choice = 2
                return self.txt, self.choice

            else:
                print("Enter the digit 1 or 2")
                continue

    # Generates the question, answers and correct answer number and returns them
    def generate_question(self):
        # Opens the txt chosen and reads the line that equals to the question number that is being asked.
        # e.g if it was question 1 the line one of the question file would be read.
        whole_question = self.txt[self.question_number]

        # separates the line into question, answers and collects the correct answer number from the end of the line
        question_split = whole_question.split(",")
        question = str(question_split[0:1]).strip("[]" "'")
        answers = str(question_split[1:5]).strip("[]").replace("'", "")
        correct_num = list(question_split).pop(5)
        correct_num = int(correct_num) - 1

        # Adds one to the question counter
        self.question_number += 1
        return question, answers, correct_num


# Class for creating a txt leaderboard and displaying results
class Leaderboard:
    def __init__(self):
        # Uses import datatime to generate the time and date at which the quiz was completed
        self.date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generates the Results.txt
    def results(self, user_name, score):
        end_result = ("Your total score is " + str(score) + " out of 10! \n")
        result = open("Results.txt", "w")
        result.write(str(user_name) + " == " + str(self.date_time) + " == " + end_result)
        print(end_result)

    # Appends the leaderboard with the users information, user name, score and what quiz set.
    def leaderboard_append(self, user_name, score, quiz_choice):
        score = (str(score) + " / 10")
        if quiz_choice == 1:
            leaderboard = open("leaderboard.txt", "a+")
        else:
            leaderboard = open("leaderboard2.txt", "a+")

        leaderboard.write(score + " == " + str(user_name) + " == " + str(self.date_time) + "\n")
        leaderboard.close()

    # Takes the data from the leaderboard file and sorts it from highest score the lowest, and writes it to the
    # leaderboard file.
    def leaderboard_sorted(self, quiz_choice):
        if quiz_choice == 1:
            leaderboard = open("leaderboard.txt")
        else:
            leaderboard = open("leaderboard2.txt")

        leaderboard_string = leaderboard.readlines()

        scores = []     # Creates a array to store the new leaderboard lines where the score is separated from the rest
                        # of the users data.

        # Splits the score from the rest of the data and adds to scores
        for line in leaderboard_string:
            score, name = line.split("/")
            scores.append((int(score), name))

        scores.sort(reverse=True)  # Sorts the data in scores and reverses it
        leaderboard.close()

        # Writes the sorted data to the leaderboard file
        if quiz_choice == 1:
            leaderboard = open("leaderboard.txt", "w")
        else:
            leaderboard = open("leaderboard2.txt", "w")

        # Takes the data line by line in scores and adds the first element and the second e.g. (3, / 10 bob 2019)
        # and prints them to the leaderboard overwriting the old data.
        for line in scores:
            line = str(line[0]) + " /" + str(line[1])
            leaderboard.write(str(line))
        leaderboard.close()

    # Writes the top ten lines from the leaderboard file.
    def leaderboard_write(self, quiz_choice):
        if quiz_choice == 1:
            leaderboard = open("leaderboard.txt", "r")
        else:
            leaderboard = open("leaderboard2.txt", "r")

        print("===Leaderboard===")
        for i in range(10):
            lb = leaderboard.readline()
            print(str(lb))

    # Runs the functions leaderboard_append ,leaderboard_sorted, results and leaderboard_write
    def leaderboard(self, user_name, score, quiz_choice):
        self.leaderboard_append(user_name, score, quiz_choice)
        self.leaderboard_sorted(quiz_choice)
        self.results(user_name, score)
        self.leaderboard_write(quiz_choice)


# Class for the main game code.
class QuizGame:
    def __init__(self):
        self.user_name = self.user_name()   # Gets the users name
        self.question = 0                   # Tally for the question the user is on
        self.q = Quizzes()                  # Initialises Quizzes
        self.leaderboard = Leaderboard()    # Initialises Leaderboard
        self.score = 0                      # The users score

    # Asks the user for there user name
    def user_name(self):
        self.user_name = input("Please enter your name: ")
        return self.user_name

    # Determines whether the users guess is correct or not
    def guess(self, user_guess, answers, correct_num):
        # Splits the answers up and selects the correct on using the correct number that was generated with the question
        # and formats it.
        answers = answers.split(",")
        correct_answers = answers[correct_num]
        correct_answers = str(correct_answers).lower().strip()

        # Formats the user guess and checks it verses the correct answer, and give a output depending on whether it
        # matches or not.
        user_guess = user_guess.lower().strip()
        if user_guess == correct_answers:
            response = "Correct!"
            self.score += 1

            return response
        elif user_guess != correct_answers:
            response = "Incorrect!"
            return response

    # Run the main part of the game.
    def game(self):
        quiz_choice = self.q.choice  # Gets what question set the user has chosen in Class Quizzes()

        # While it is less then ten (as each question set has 10 questions) it will use Class Quizzes to gain
        while self.question < 10:
            # Gets the question, answers and correct answer number from a function in Class Quizzes
            question, answers, correct_num = self.q.generate_question()
            print()
            print("Question " + str(self.question + 1) + ":")  # Adds one to the question as in CS numbers start a 0
            print(question + "\n")                             # Displays the Question
            print("Your options are: ")
            print(answers + "\n")                              # Displays the Answers

            # Asks the user for there answer and checks it using the Guess() function and displays whether they are
            # right or wrong.
            user_guess = input("Please enter one of the above: ")
            user_correct = self.guess(user_guess, answers, correct_num)
            print(user_correct + "\n")
            self.question += 1                                 # Adds 1 to the question counter

        # Generates a leaderboard file and results file using Class leaderboard
        self.leaderboard.leaderboard(self.user_name, self.score, quiz_choice)


# Function for initializing the game.
def main():
    quiz_game = QuizGame()  # Initialises QuizGame()
    quiz_game.game()        # Runs the function game() in QuizGame
    print()


main()

# Stops the window from closing upon finishing
print("")
input("Press any button to exit!")
