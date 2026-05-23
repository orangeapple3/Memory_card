# Exercise “VSC. PyQt. Memory Card”
# 1.1. Program text

from random import randint, shuffle
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QButtonGroup,
    QGroupBox,
    QHBoxLayout,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)


class Question:
    """Contains a question, a correct answer, and three incorrect ones."""

    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3


# -----------------------------
# Data
# -----------------------------
questions_list = [
    Question(
        "Official language of Brazil",
        "Portuguese",
        "English",
        "Spanish",
        "Brazilian",
    ),
    Question(
        "Which color does not appear on the American flag?",
        "Green",
        "Red",
        "White",
        "Blue",
    ),
    Question(
        "Yakut national house",
        "Urasa",
        "Yurta",
        "Igloo",
        "Khata",
    ),
]

# -----------------------------
# App + Widgets
# -----------------------------
app = QApplication([])

btn_OK = QPushButton("Reply")  # reply button
lb_Question = QLabel("The most difficult question in the world!")

# Answer options group
RadioGroupBox = QGroupBox("Answer options")
rbtn_1 = QRadioButton("Option 1")
rbtn_2 = QRadioButton("Option 2")
rbtn_3 = QRadioButton("Option 3")
rbtn_4 = QRadioButton("Option 4")

RadioGroup = QButtonGroup()
RadioGroup.addButton(rbtn_1)
RadioGroup.addButton(rbtn_2)
RadioGroup.addButton(rbtn_3)
RadioGroup.addButton(rbtn_4)

layout_ans1 = QHBoxLayout()
layout_ans2 = QVBoxLayout()
layout_ans3 = QVBoxLayout()

layout_ans2.addWidget(rbtn_1)
layout_ans2.addWidget(rbtn_2)
layout_ans3.addWidget(rbtn_3)
layout_ans3.addWidget(rbtn_4)

layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3)
RadioGroupBox.setLayout(layout_ans1)

# Results group
AnsGroupBox = QGroupBox("Test results")
lb_Result = QLabel("Are you right or not?")
lb_Correct = QLabel("Answer will be here!")

layout_res = QVBoxLayout()
layout_res.addWidget(lb_Result, alignment=Qt.AlignLeft | Qt.AlignTop)
layout_res.addWidget(lb_Correct, alignment=Qt.AlignHCenter, stretch=2)
AnsGroupBox.setLayout(layout_res)

# Main layout
layout_line1 = QHBoxLayout()
layout_line2 = QHBoxLayout()
layout_line3 = QHBoxLayout()

layout_line1.addWidget(
    lb_Question,
    alignment=Qt.AlignHCenter | Qt.AlignVCenter,
)

layout_line2.addWidget(RadioGroupBox)
layout_line2.addWidget(AnsGroupBox)
AnsGroupBox.hide()  # show question panel first

layout_line3.addStretch(1)
layout_line3.addWidget(btn_OK, stretch=2)
layout_line3.addStretch(1)

layout_card = QVBoxLayout()
layout_card.addLayout(layout_line1, stretch=2)
layout_card.addLayout(layout_line2, stretch=8)
layout_card.addStretch(1)
layout_card.addLayout(layout_line3, stretch=1)
layout_card.addStretch(1)
layout_card.setSpacing(5)

# -----------------------------
# Logic
# -----------------------------
def show_result():
    """Show answer panel."""
    RadioGroupBox.hide()
    AnsGroupBox.show()
    btn_OK.setText("Next")


def show_question():
    """Show question panel."""
    RadioGroupBox.show()
    AnsGroupBox.hide()
    btn_OK.setText("Reply")

    # reset selection
    RadioGroup.setExclusive(False)
    rbtn_1.setChecked(False)
    rbtn_2.setChecked(False)
    rbtn_3.setChecked(False)
    rbtn_4.setChecked(False)
    RadioGroup.setExclusive(True)


answers = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]


def ask(q: Question):
    """Write the question/answers into widgets; randomize placement."""
    shuffle(answers)
    answers[0].setText(q.right_answer)
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)

    lb_Question.setText(q.question)
    lb_Correct.setText(q.right_answer)
    show_question()


def show_correct(res: str):
    """Show the result text and switch panels."""
    lb_Result.setText(res)
    show_result()


def check_answer():
    """Check selected answer and show the results panel."""
    if answers[0].isChecked():
        show_correct("Right!")
        window.score += 1
    else:
        if (
            answers[1].isChecked()
            or answers[2].isChecked()
            or answers[3].isChecked()
        ):
            show_correct("Wrong answer!")

    print(
        "Statistics\n- Total questions:", window.total,
        "\n- Right answers:", window.score,
    )
    if window.total > 0:
        print("Rating:", window.score / window.total * 100, "%")


def next_question():
    """Ask a random question from the list."""
    window.total += 1
    cur_question = randint(0, len(questions_list) - 1)
    q = questions_list[cur_question]
    ask(q)


def click_OK():
    """Check the answer or load the next question."""
    if btn_OK.text() == "Reply":
        check_answer()
    else:
        next_question()


# -----------------------------
# Window
# -----------------------------
window = QWidget()
window.setLayout(layout_card)
window.setWindowTitle("Memo Card")

btn_OK.clicked.connect(click_OK)

window.score = 0
window.total = 0

next_question()
window.resize(400, 300)
window.show()

app.exec()