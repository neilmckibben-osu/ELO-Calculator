import tkinter
import operator
from tkinter import *
from tkinter import ttk
from tkinter import *
import os
import ast
import re
ten = 10.00


list = dict()
logs = dict()
if os.stat("logs.txt").st_size != 2:
    log_file = open("logs.txt", "r").read()
    list_file = open('list.txt', 'r').read()
    with open('logs.txt', 'r') as f:
        s = f.read()
        logs = ast.literal_eval(s)
    with open('list.txt', 'r') as f:
        s = f.read()
        list = ast.literal_eval(s)


class App:

    def __init__(self, master):
        main_container = Frame(master)
        list_one = Frame(main_container)
        buttons = Frame(main_container)
        label_container = Frame(master)
        main_container.pack(side='top', fill='both', expand=True)
        list_one.pack(side='left', fill='both', expand=True)
        buttons.pack(side='right', fill='both', expand=True)
        label_container.pack(side='bottom', fill='both', expand=True)
        middle_frame = Frame(main_container)
        middle_frame.pack(side='top', fill='both', expand=True)
        left_frame = Frame(list_one)
        left_frame.pack(side='top', fill='both', expand=True)
        button_frame = Frame(buttons)
        button_frame.pack(side='right', fill='both', expand=True)
        bottom_frame = LabelFrame(label_container)
        bottom_frame.pack(side='bottom', fill='both', expand=True)

        master.title('ELO Calculator')
        buttons = []
        label_button = []
        App.add_listbox(self, middle_frame, left_frame)
        App.add_buttons(self, button_frame, buttons, bottom_frame, label_button)
        App.enable_buttons(self, buttons)
        self.list_rank_one.bind('<Button-1>', lambda event: App.re_enable_buttons(event, self, buttons))
        self.list_rank_two.bind('<Button-1>', lambda event: App.re_enable_buttons(event, self, buttons))
        buttons[0].bind('<Button-1>', lambda event: Commands.add_player(event, self))
        buttons[1].bind('<Button-1>', lambda event: Commands.remove_player(event, self))
        buttons[2].bind('<Button-1>', lambda event: Commands.odds(event, self, label_button))
        buttons[3].bind('<Button-1>', lambda event: Commands.match(event, self, list, logs, buttons))
        buttons[4].bind('<Button-1>', lambda event: Commands.clear_stats_confirm(event, self, list, logs))
        buttons[5].bind('<Button-1>', lambda event: Commands.stats_event(event, list, logs, label_button))

    def add_listbox(self, middle_frame, left_frame):
        self.list_rank_one = Listbox(middle_frame, exportselection=0)
        self.list_rank_two = Listbox(left_frame, exportselection=0)
        count = 1
        for names in list:
            self.list_rank_one.insert(count, str(
                count) + ') ' + names + ': ' + str((list[names])))
            self.list_rank_two.insert(count, str(
                count) + ') ' + names + ': ' + str((list[names])))
            count += 1
        self.list_rank_one.configure(bg='white', fg='black')
        self.list_rank_two.configure(bg='white', fg='black')
        self.list_rank_one.pack(expand=1, fill='both')
        self.list_rank_two.pack(expand=1, fill='both')

    def add_buttons(self, button_frame, buttons, bottom_frame, label_button):
        counter = 0
        button_names = ['Add Player', 'Delete Player', 'Odds', 'Match', 'Clear All Stats', 'Display Stats']
        for index in range(len(button_names)):
            name = button_names[index]
            button = Button(button_frame, text=name)
            button.grid(column=2, row=counter, sticky=N + S + E + W)
            counter += 1
            buttons.append(button)
        label = Label(bottom_frame)
        label.pack(fill=BOTH, expand=True, side='top')
        label_button.append((label))

    def enable_event(event, self, buttons):
        App.enable_buttons(self, buttons)

    def enable_buttons(self, buttons):
        counter = 2
        for index in range(len(buttons) - 2):
            buttons[counter].configure(state='disable')
            counter += 1
        buttons[0].configure(state='active')
        buttons[1].configure(state='active')
        buttons[4].configure(state='active')

        if(self.list_rank_one.size() > 1):
            buttons[5].configure(state='active')

    def re_enable_buttons(event, self, buttons):

        if ((len(self.list_rank_one.curselection())) and (
                len(self.list_rank_two.curselection())) != 0):
            if(self.list_rank_one.curselection() != self.list_rank_two.curselection()):
                counter = 2
                for index in range(len(buttons) - 2):
                    buttons[counter].configure(state='active')
                    counter += 1
            else:
                buttons[2].configure(state='disabled')
                buttons[3].configure(state='disabled')
        elif((len(self.list_rank_one.curselection()) or len(self.list_rank_two.curselection())) != 0):
            counter = 0
            for index in range(len(buttons) - 3):
                buttons[counter].configure(state='active')
                counter += 1

        if(self.list_rank_one.size() > 1):
            buttons[5].configure(state='active')


class Commands:

    def clear_stats_confirm(event, self, list, logs):
        top = Toplevel()
        top.geometry('450x200')
        top.title('Clear Stats')
        msg = Message(
            top,
            text='Are you sure you want to clear all stats?',
            width='450')
        msg.pack()
        confirm = Button(top, text="Yeah I'm sure")
        confirm.bind('<Button-1>', lambda event: Commands.clear_stats(self, top, list, logs))
        confirm.pack(side='left', fill='x', expand=True)
        deny = Button(top, text="No thanks")
        deny.bind('<Button-1>', lambda event: Commands.dont_clear_stats(self, top))
        deny.pack(side='right', fill='x', expand=True)

    def clear_stats(self, top, list, logs):
        self.list_rank_one.delete(0, END)
        self.list_rank_two.delete(0, END)
        Commands.clear_logs(logs, list)
        top.destroy()

    def dont_clear_stats(self, top):
        top.destroy()

    def add_player(event, self):
        top = Toplevel()
        top.geometry("450x200")
        top.title('Add Player')
        msg = Message(top, text='Please enter the name of the new player', width='450')
        msg.pack()
        input = StringVar()
        name = Entry(top, textvariable=input)
        input.get()
        name.pack()
        confirm = Button(top, text='Add Player')
        confirm.bind('<Button-1>', lambda event: Commands.add_player_event(event, list, logs, input.get(), top, self))
        confirm.pack()

    def add_player_event(event, list, logs, name, top, self):
        text_var = StringVar()
        display = Label(top, text=text_var.get())
        display.pack()
        if name in list:
            text_var.set('That name is already used!')
            display.configure(text=text_var.get())

        else:
            list[name] = 1500.00
            logs[name] = [0, 0, 0, 32]
            Commands.update_logs(logs, list)
            self.list_rank_one.delete(0, END)
            self.list_rank_two.delete(0, END)
            count = 1
            for names in list:
                self.list_rank_one.insert(count, str(
                    count) + ') ' + names + ': ' + str((list[names])))
                self.list_rank_two.insert(count, str(
                    count) + ') ' + names + ': ' + str((list[names])))
                count += 1
            top.destroy()

    def remove_player(event, self):
        top = Toplevel()
        top.geometry("450x200")
        top.title('Delete Player')
        msg = Message(
            top,
            text='Please enter the name of the player to delete',
            width='450')
        msg.pack()
        input = StringVar()
        name = Entry(top, textvariable=input)
        input.get()
        name.pack()
        confirm = Button(top, text='Delete Player')
        confirm.bind(
            '<Button-1>',
            lambda event: Commands.remove_player_event(event, list, logs, input.get(), top, self))
        confirm.pack()

    def remove_player_event(event, list, logs, name, top, self):
        text_var = StringVar()
        display = Label(top, text=text_var.get())
        display.pack()
        if name not in list:
            text_var.set('That name is not used!')
            display.configure(text=text_var.get())

        else:
            del list[name]
            del logs[name]
            Commands.update_logs(logs, list)
            self.list_rank_one.size()
            for index in range(self.list_rank_one.size()):
                string_iterate = self.list_rank_one.get(index)
                player_one = string_iterate[string_iterate.find(
                    ' ') + 1: string_iterate.find(':')]
                if player_one == name:
                    self.list_rank_one.delete(index)
                    self.list_rank_two.delete(index)

            top.destroy()

    def odds(event, self, label_button):
        index_one = self.list_rank_one.curselection()
        index_two = self.list_rank_two.curselection()
        string_one = str(self.list_rank_one.get((index_one)))
        string_two = str(self.list_rank_two.get(index_two))
        player_one = string_one[string_one.find(' ') + 1: string_one.find(':')]
        player_two = string_two[string_two.find(' ') + 1: string_two.find(':')]
        elo_one = list[player_one]
        elo_two = list[player_two]
        difference = (elo_two - elo_one)
        probability = (1.00 / (1.00 + (ten ** ((difference) / 400))) * 100)
        decimal_probability = float('{0:.2f}'.format(probability))
        text_var = StringVar()
        text_var.set('There is a ' + str(decimal_probability) + '% chance that ' + player_one + ' will ' + 
                     'win against ' + player_two)
        label_button[0].configure(text=text_var.get())

    def match(event, self, list, logs, buttons):
        index_one = self.list_rank_one.curselection()
        index_two = self.list_rank_two.curselection()
        string_one = str(self.list_rank_one.get((index_one)))
        string_two = str(self.list_rank_two.get(index_two))
        player_one = string_one[string_one.find(' ') + 1: string_one.find(':')]
        player_two = string_two[string_two.find(' ') + 1: string_two.find(':')]
        top = Toplevel()
        top.geometry('450x200')
        top.title('Match')
        msg = Message(top, text='Please select the winner', width='450')
        msg.pack()
        confirm = Button(top, text=player_one)
        confirm.bind('<Button-1>', lambda event: Commands.calc(event, self, 1, list, logs, player_one, player_two, top))
        confirm.pack(side='right', fill='x', expand=True)
        deny = Button(top, text=player_two)
        deny.bind('<Button-1>', lambda event: Commands.calc(event, self, 1, list, logs, player_two, player_one, top))
        deny.pack(side='left', fill='x', expand=True)
        App.enable_buttons(self, buttons)

    def calc(event, self, win, list, logs, player_one, player_two, top):
        top.destroy()
        elo_one = list[player_one]
        elo_two = list[player_two]

        trans_one = ten ** (elo_one / 400)
        trans_two = ten ** (elo_two / 400)
        expected_one = (trans_one / (trans_one + trans_two))
        expected_two = (trans_two / (trans_one + trans_two))
        # if win is 1, player_one wins, 1/2 is a tie, 1 player2 wins
        result_one = float(win)
        result_two = float(0)

        k_value_one = float(logs[player_one][3])
        k_value_two = float(logs[player_two][3])
        (new_elo_one) = (elo_one + k_value_one * (result_one - expected_one))
        new_elo_two = (elo_two + k_value_two * (result_two - expected_two))
        decimal_new_elo_one = float("{0:.2f}".format(new_elo_one))
        decimal_new_elo_two = float("{0:.2f}".format(new_elo_two))
        # update list
        list[player_one] = float(decimal_new_elo_one)
        list[player_two] = float(decimal_new_elo_two)

        # update listBox
        self.list_rank_one.delete(0, END)
        self.list_rank_two.delete(0, END)
        count = 1
        for names in list:
            self.list_rank_one.insert(count, str(
                count) + ') ' + names + ': ' + str((list[names])))
            self.list_rank_two.insert(count, str(
                count) + ') ' + names + ': ' + str((list[names])))
            count += 1

        # updates logs
        if result_one == 1:
            record_one = logs[player_one]
            record_one[0] = record_one[0] + 1
            logs[player_one] = record_one
            record_two = logs[player_two]
            record_two[2] = record_two[2] + 1
            logs[player_two] = record_two
        elif result_one == 0:
            record_one = logs[player_one]
            record_one[2] = record_one[2] + 1
            logs[player_one] = record_one
            record_two = logs[player_two]
            record_two[0] = record_two[0] + 1
            logs[player_one] = record_two
        else:
            record_one = logs[player_one]
            record_one[1] = record_one[1] + 1
            logs[player_one] = record_one
            record_two = logs[player_two]
            record_two[1] = record_two[1] + 1
            logs[player_one] = record_two

        elo_check = [elo_one, elo_two]

        # updates k-values
        for x in elo_check:
            if x > 2400:
                if elo_check[0] > 2400:
                    record_one = logs[player_one]
                    record_one[3] = 16
                    logs[player_one] = record_one
                else:
                    record_two = logs[player_two]
                    record_two[3] = 16
                    logs[player_two] = record_two
            elif 2400 > x > 2100:
                if 2400 > elo_check[0] > 2100:
                    record_one = logs[player_one]
                    record_one[3] = 24
                    logs[player_one] = record_one
                else:
                    record_two = logs[player_two]
                    record_two[3] = 24
                    logs[player_two] = record_two

            else:
                if elo_check[0] < 2100:
                    record_one = logs[player_one]
                    record_one[3] = 32
                    logs[player_one] = record_one
                else:
                    record_two = logs[player_two]
                    record_two[3] = 32
                    logs[player_two] = record_two
        Commands.update_logs(logs, list)

    def stats_event(event, list, logs, label_button):
        top = Toplevel()
        top.geometry("450x200")
        top.title('Stats')
        msg = Message(
            top,
            text='Please enter the name of the player to display stats',
            width='450')
        msg.pack()
        input = StringVar()
        gui_name = Entry(top, textvariable=input)
        name = input.get()
        gui_name.pack()
        confirm = Button(top, text='Display stats')
        confirm.pack()
        confirm.bind('<Button-1>', lambda event: Commands.stats_button_press(event, list, logs, name, top, label_button,
                     confirm, input))

    def stats_button_press(event, list, logs, name, top, label_button, confirm, input):
        text_var = StringVar()
        display = Label(top, text=text_var.get())
        name_str = input.get()
        display.pack()
        if name_str in list:
            confirm.bind('<Button-1>', lambda event: Commands.stats(event, list, logs, name_str, top, label_button))
        else:
            text_var.set('That name is not used!')
            display.configure(text=text_var.get())

    def stats(event, list, logs, name, top, label_button):

        top.destroy()
        text_var = StringVar()
        text_var.set(name +
                     ' has an ELO of ' +
                     str(list[name]) +
                     ', and a record of ' +
                     str(logs[name][0]) +
                     ' wins, ' +
                     str(logs[name][1]) +
                     ' ties, and ' +
                     str(logs[name][2]) +
                     ' losses.')
        label_button[0].configure(text=text_var.get())

    def update_logs(logs, list):
        list = Commands.sort_values(list)
        log_file = open("logs.txt", "w")
        list_file = open("list.txt", "w")
        log_file.write(str(logs))
        list_file.write(str(list))
        log_file.close()
        list_file.close()

    def sort_values(list):
        sorted_list = reversed(
            sorted(
                list.items(),
                key=operator.itemgetter(1)))
        new_list = dict()
        for name in sorted_list:
            new_list[name[0]] = name[1]
        print(new_list)
        return new_list

    def clear_logs(logs, list):
        log_file = open('logs.txt', 'r+')
        list_file = open('list.txt', 'r+')
        log_file.close()
        list_file.close()
        logs.clear()
        list.clear()
        Commands.update_logs(logs, list)


root = Tk()
App(root)
root.geometry('450x300')
root.update()
root.mainloop()
