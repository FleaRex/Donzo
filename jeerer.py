from __future__ import print_function, unicode_literals
from PyInquirer import prompt, Separator

from jeerer.card import Card
from jeerer.board import Board

def main():
    board = Board([])

    while True:
        print(board)

        questions = [
            {
                'type': 'rawlist',
                'name': 'action',
                'message': 'What would you like to do',
                'choices': [
                    'Add a card',
                    'Split a card',
                    'Mark a card as done',
                ]
            }
        ]

        action = prompt(questions)['action']

        if action == "Add a card":
            board.add_card(Card("Test"))
        elif action == "Split a card":
            card_split(board)
        elif action == "Mark a card as done":
            mark_card_done(board)
        else:
            pass


def card_split(board: Board):
    questions = [
        {
            'type': 'input',
            'name': 'number',
            'message': 'Which card would you like to split?',
            'filter': lambda answer: int(answer)
        }
    ]

    card_to_split = prompt(questions)['number']

    board.get_unfinished_cards()[card_to_split].split(["X", "Y"])


def mark_card_done(board: Board):
    questions = [
        {
            'type': 'input',
            'name': 'number',
            'message': 'Which card would you like mark done?',
            'filter': lambda answer: int(answer)
        }
    ]

    card_to_mark_done = prompt(questions)['number']

    board.get_unfinished_cards()[card_to_mark_done].mark_done()


if __name__ == "__main__":
    main()