import statInterpreter
class Commands:

    def __init__(self):
        self.currentOpen = statInterpreter.StatInterpreter
        pass
    def load(self, path):
        self.currentOpen.load(path)
    def init_commands(self):
        command = ""
        while command != 'q':
            command = input("->")
            command = command.split(' ')
            if command == ';pad'
                    self.load(command[1])
                case 'print':
                    if len(command) == 2:
                        print(self.currentOpen.print_LeaderBoard(command[1]))
                    elif len(command) >= 3:
                        i = 1
                        while i < len(command)-1:
                            print(self.currentOpen.print_LeaderBoard(command[i]))
                            i += 1
                case 'post':
                    channel = command[1]
                    if len(command) == 2:
                        print(self.currentOpen.print_LeaderBoard(command[1]))
                    elif len(command) >= 3:
                        i = 1
                        while i < len(command)-1:
                            print(self.currentOpen.print_LeaderBoard(command[i]))
                            i += 1
commands = Commands
Commands.init_commands()