from __future__ import print_function, unicode_literals
from PyInquirer import prompt, Separator
import os
import pickle

from jeerer.card import Card
from jeerer.board import Board


def main():
    if os.path.exists('jeerer_board.pickle'):
        with open('jeerer_board.pickle', 'rb') as file:
            board = pickle.load(file)
    else:
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
                    'Quit'
                ]
            }
        ]

        action = prompt(questions)['action']

        if action == "Add a card":
            add_card(board)
        elif action == "Split a card":
            card_split(board)
        elif action == "Mark a card as done":
            mark_card_done(board)
        elif action == "Quit":
            save_and_quit(board)
        else:
            pass


def add_card(board: Board):
    questions = [
        {
            'type': 'input',
            'name': 'task',
            'message': 'What task do you want to add?',
        }
    ]

    board.add_card(Card(prompt(questions)['task']))


def card_split(board: Board):
    questions = [
        {
            'type': 'input',
            'name': 'number',
            'message': 'Which card would you like to split?',
            'filter': lambda answer: int(answer),
            'validate': lambda answer: 0 <= int(answer) < len(board.get_unfinished_cards())
        },
        {
            'type': 'input',
            'name': 'subtasks',
            'message': 'How would you like to split this task? Separate your new tasks with |',
            'filter': lambda answer: answer.split('|')
        }
    ]
    answers = prompt(questions)

    card_to_split = answers['number']
    board.get_unfinished_cards()[card_to_split].split(answers['subtasks'])


def mark_card_done(board: Board):
    questions = [
        {
            'type': 'input',
            'name': 'number',
            'message': 'Which card would you like mark done?',
            'filter': lambda answer: int(answer),
            'validate': lambda answer: 0 <= int(answer) < len(board.get_unfinished_cards())
        }
    ]

    card_to_mark_done = prompt(questions)['number']

    board.get_unfinished_cards()[card_to_mark_done].mark_done()


def save_and_quit(board: Board):
    with open('jeerer_board.pickle', 'wb+') as file:
        pickle.dump(board, file)
        exit(0)

if __name__ == "__main__":
    main()
