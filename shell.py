import os
import signal

def directory(file , args):
    if file == 'pwd':
        print(os.getcwd())
    elif file == 'cd':
        os.chdir(args[1])

def execBackground(args , bglist):
    if len(bglist) < 5:
        id = os.fork()
        bglist.append([id , os.getcwd() , args])
        file = args[0]
        if id == 0 :
            os.execvp(file , args)
            os.execvp('bg' , ['bg'] + args)
        if id > 0:
            pid , sts = os.waitpid(id , os.WNOHANG)
            if pid == id:
                bglist.remove(item)
    else:
        print("5 Jobs are in the list already!")

def bgTerminationChecker(bglist):
    for item in bglist:
        id = int(item[0])
        pid , sts = os.waitpid(id , os.WNOHANG)
        if pid == id:
            bglist.remove(item)

def printbglist(bglist):
    i = 1
    for item in bglist:
        string = "(" + str(i) + ") "
        string += str(item[1]) + "/"
        for element in item[2]:
            string += str(element)
        print(string)
        i += 1

def execute(file , args):
    id = os.fork()
    if id == 0:
        os.execvp(file , args)
    if id > 0:
        os.waitpid(id , 0)

def sendsignal(file , args , bglist):
    # check here
    temp = bglist[int(args[1])-1]
    pid = temp[0]
    if file == 'bgkill':
        os.kill(pid , signal.SIGKILL )
    if file == 'bgstop':
        os.kill(pid , signal.SIGSTOP )
    if file == 'bgstart':
        os.kill(pid , signal.SIGCONT )

def getinput(val):
    command = []
    temp = ""
    flagQ = 0
    # zero means no " has been seen
    # one means one has been seen
    flagBS = 0
    # zero means no \ has been seen
    # one means one has been seen
    for char in val:
        if char == ' ' and flagQ == 0 and flagBS == 0:
            command.append(temp)
            temp = ""
        elif char == '"' and flagQ == 0:
            flagQ = 1
            temp += char
        elif char == '"' and flagQ == 1:
            flagQ = 0
            temp += char
        elif char == "\\" and flagBS == 0:
            flagBS = 1
            temp += char
        elif char != ' ' and flagBS == 1:
            flagBS = 0
            temp += char
        else:
            temp += char

    if temp != "":
        command.append(temp)

    return command

def getConfig():
    f = open(".bashrc", "r")
    dict = {}
    config = f.read()
    config = config.split('\n')
    for line in config:
        if len(line) > 0:
            line = line.split("=")
            left = line[0].split()
            if left[0] == 'alias':
                key = left[1].replace('"' , '')
                value = line[1].replace('"' , '')
                dict[key] = value
    return dict

if __name__ == "__main__":
    val = " "
    bglist = []
    # in bglist : [ pid , directory , name ]
    dict = getConfig()
    #test
    while val != "Exit" :
        print("\033[32;40m" + str(os.getcwd()) , end = " ")
        val = input("\033[37;40m")
        command = getinput(val)

        if len(command)>0:
            if command[0] in dict:
                command = dict[command[0]].split() + command[1:]

            file = command[0]
            args = command
        bgTerminationChecker(bglist)
        if len(command) == 0:
            continue
        elif file in ['cd' , 'pwd']:
            directory(file , args)
        elif file == 'bg':
            execBackground(args[1:] , bglist)
        elif file == 'bglist':
            printbglist(bglist)
        elif file in ['bgkill' , 'bgstop' , 'bgstart']:
            sendsignal(file , args , bglist)
        elif file in ['Exit' , 'exit' , 'q']:
            break
        else:
            execute(file , args)
