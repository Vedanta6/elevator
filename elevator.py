#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import sys
from threading import Thread, Event


class Elevator:
    def __init__(self, n_stories, story_height, elevator_rate, doors_delay):
        self.elevator_story = 1
        self.movement_up = True
        self.number_of_stories = int(n_stories) if n_stories in range(5, 21) else 5
        self.pressed_buttons_in_elevator = []
        self.pressed_buttons_on_stories = []
        self.doors_time_delay = doors_delay
        self.time_between_stories = round(float(story_height)/elevator_rate, 3) if elevator_rate > 0 else 0

    def get_number_of_stories(self):
        """ Get number of stories in the building """
        n_stories = self.number_of_stories
        return n_stories

    def get_pressed_buttons(self):
        """ Debug function """
        print("Inside: ", self.pressed_buttons_in_elevator)
        print("Outside: ", self.pressed_buttons_on_stories)

    def change_story(self):
        """ Cross one story """
        time.sleep(self.time_between_stories)
        if self.movement_up:
            self.elevator_story += 1
        else:
            self.elevator_story -= 1
        print("Elevator is on the ", self.elevator_story, " story")

    @staticmethod
    def open_doors():
        print("Doors were opened")

    @staticmethod
    def close_doors():
        print("Doors were closed")

    def button_in_elevator_was_pressed(self, n_of_button):
        """ Passenger pressed the button inside the elevator """
        if n_of_button in range(1, self.number_of_stories + 1):
            if n_of_button not in self.pressed_buttons_in_elevator:
                self.pressed_buttons_in_elevator.append(n_of_button)
                self.pressed_buttons_in_elevator.sort()

    def button_on_story_was_pressed(self, n_of_story):
        """ Passenger pressed the button on the story """
        if n_of_story in range(1, self.number_of_stories + 1):
            if n_of_story not in self.pressed_buttons_in_elevator:
                self.pressed_buttons_on_stories.append(n_of_story)
                self.pressed_buttons_on_stories.sort()

    def stop_on_story(self):
        """ Open doors, unlock the buttons and close doors"""
        self.open_doors()
        time.sleep(self.doors_time_delay)
        story = self.elevator_story
        if story in self.pressed_buttons_in_elevator:
            self.pressed_buttons_in_elevator.remove(story)
        if story in self.pressed_buttons_on_stories:
            self.pressed_buttons_on_stories.remove(story)
        if story == self.number_of_stories and self.movement_up or story == 1 and not self.movement_up:
            self.movement_up = not self.movement_up
        self.close_doors()

    def go_to_story(self, n_of_story_to_go):
        """ Send the elevator on the adjusted story """
        distance_between_stories = abs(self.elevator_story - n_of_story_to_go)
        if distance_between_stories != 0:
            for _ in range(distance_between_stories):
                self.change_story()
        self.stop_on_story()

    def send_elevator(self):
        """ Main algorithm """
        inside = len(self.pressed_buttons_in_elevator) > 0
        outside = len(self.pressed_buttons_on_stories) > 0
        inside_buttons = self.pressed_buttons_in_elevator
        outside_buttons = self.pressed_buttons_on_stories
        if self.movement_up:
            if inside:
                change_direction = True
                for button in inside_buttons:
                    if button >= self.elevator_story:
                        next_move = button
                        change_direction = False
                        self.go_to_story(next_move)
                        break
                if change_direction:
                    self.movement_up = not self.movement_up
            elif outside:
                next_move = outside_buttons[-1]
                self.go_to_story(next_move)
        else:
            if outside or inside:
                buttons = inside_buttons + outside_buttons
                buttons.sort(reverse=True)
                change_direction = True
                for button in buttons:
                    if button <= self.elevator_story:
                        next_move = button
                        change_direction = False
                        self.go_to_story(next_move)
                        break
                if change_direction:
                    self.movement_up = not self.movement_up


"""
Параметры:
- кол-во этажей в подъезде — N (от 5 до 20);
- высота одного этажа;
- скорость лифта при движении в метрах в секунду;
- время между открытием и закрытием дверей.
Управление лифтом:
- вызов лифта на этаж из подъезда;      - outside_call
- нажать на кнопку этажа внутри лифта.  - inside_call
Выводимые действия:
- лифт проезжает некоторый этаж;
- лифт открыл двери;
- лифт закрыл двери.
"""


def get_arguments_from_cmd():
    """ Get arguments from cmd running the *.py or use default values """
    args = []
    defaults = [2.5, 1.6, 10.]
    ranges = [0., 10000]
    try:
        args.append(int(sys.argv[1]) if int(sys.argv[1]) in range(5, 21) else 5)
        for index, arg in enumerate(sys.argv[2:]):
            try:
                if ranges[0] < float(arg) <= ranges[1]:
                    args.append(float(arg))
                else:
                    raise ValueError
            except ValueError:
                args.append(defaults[index])
    except IndexError:
        args = [5.] + defaults
    return args


def cmd_reader(e, event_name):
    """ Process the commands from user """
    n_of_elevator_stories = e.get_number_of_stories()
    while 1:
        try:
            command = input()
            try:
                cmd_io = command[0]
                story = int(command[1:])
                check_story = story in range(1, n_of_elevator_stories + 1)
                if cmd_io == 'i' and check_story:
                    e.button_in_elevator_was_pressed(story)
                    event_name.set()
                elif cmd_io == 'o' and check_story:
                    e.button_on_story_was_pressed(story)
                    event_name.set()
            except ValueError or IndexError:
                pass
            except KeyboardInterrupt:
                break
        except EOFError:
            pass
        except KeyboardInterrupt:
            break


def run_elevator(e, event_name):
    """ Run elevator algorithm """
    while 1:
        try:
            event_name.wait()
            event_name.clear()
            e.send_elevator()
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    number_of_stories, s_height, e_rate, doors_dt = get_arguments_from_cmd()
    elevator = Elevator(n_stories=number_of_stories, story_height=s_height,
                        elevator_rate=e_rate, doors_delay=doors_dt)
    print('Enter \"i<story>\" to press the button with the number of a story inside the elevator',
          ' or \"o<story>\" to press the button on a story')
    event = Event()
    t_cmd = Thread(target=cmd_reader, args=(elevator, event))
    t_elevator = Thread(target=run_elevator, args=(elevator, event))
    t_cmd.start()
    t_elevator.start()
