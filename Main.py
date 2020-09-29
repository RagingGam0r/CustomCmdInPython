 # only wrote this since cmd handler is blocked
 import subprocess
import os
import inspect
import time
import colorama

class CmdHandler:
    def __init__(self):
        self.CustomCmds = {

        }
        self.ExecuteType = "sub"

    def RegisterCommand(self, CMDName, Desc, Function, Restrict, Aliases=None, ControllerDontTouch=True):
        self.CustomCmds[str(CMDName)] = {
            "Desc": Desc,
            "Func": Function,
            "Rest": Restrict,
            "Show": ControllerDontTouch
        }
        if Aliases != None:
            for i,v in enumerate(Aliases):
                self.RegisterCommand(str(v), Desc, Function, Restrict, Aliases=None, ControllerDontTouch=False)

    def RunCommand(self, cmd, Arguments):
        if cmd in self.CustomCmds:
            RequiredArguments = int(len(inspect.getfullargspec(self.CustomCmds[str(cmd)]["Func"]).args)-1)
            if RequiredArguments == 0:
                result = self.CustomCmds[str(cmd)]["Func"](self)
                return result
            else:
                if self.CustomCmds[str(cmd)]["Rest"]:
                    del Arguments[RequiredArguments:len(Arguments)]

                result = self.CustomCmds[str(cmd)]["Func"](self, *Arguments)
                return result
        else:
            args = ""
            for i,v in enumerate(Arguments):
                if i != len(Arguments)-1:
                    args = args + str(v) + " "
                else:
                    args = args + str(v)

            out = "ERROR IN HANDLER"
            cmd = cmd + " " + str(args)

            if self.ExecuteType == "sub":
                result = subprocess.Popen(cmd, shell=True)
                out = result.communicate()[0]
            elif self.ExecuteType == "os":
                result = os.system(cmd)
                out = None
                #return "RUN YOURSELF"
            return out


Handler = CmdHandler()

def ListAll(Hndlr):
    for _, (i,v) in enumerate(Hndlr.CustomCmds.items()):
        CmdName = str(i)
        CmdTbl = v
        Desc = CmdTbl['Desc']
        RestrictArgs = CmdTbl['Rest']
        CanShow = CmdTbl['Show']
        if CanShow:
            print(f"{CmdName}")
            print(f" {Desc}")
            #print(f" R: {RestrictArgs}")

def CTO(Hndlr):
    Hndlr.ExecuteType = "os"

def CTS(Hndlr):
    Hndlr.ExecuteType = "sub"

def ls(Hndlr, bypass=None, *args):
    NewArgs2 = []
    if bypass:
        NewArgs = [bypass] + [*args]
        NewArgs2 = []
        for i,v in enumerate(NewArgs):
            if v.lower() == "-all":
                (drive, path) = os.path.splitdrive(os.getcwd())
                NewArgs2.append(drive)
            else:
                NewArgs2.append(v)
    Hndlr.RunCommand('dir', NewArgs2)

def cdhandler(Handlr, bypass=None, *args):
    args = ""
    if bypass:
        NewArgs = [bypass] + [*args]
        NewArgs2 = []
        for i, v in enumerate(NewArgs):
            if v.lower() == "-all":
                (drive, path) = os.path.splitdrive(os.getcwd())
                NewArgs2.append(drive)
            else:
                NewArgs2.append(v)

        for i, v in enumerate(NewArgs2):
            if i != len(NewArgs2)-1:
                args = args + str(v) + " "
            else:
                args = args + str(v)

    os.chdir(str(args))

def pwd(Hndlr):
    print(os.getcwd())

Handler.RegisterCommand("CUSTOM", "Custom help menu", ListAll, True, {"CHELP", "HELPC", })
Handler.RegisterCommand("OS", "Sets execution type to os.popen", CTO, True)
Handler.RegisterCommand("SUB", "Sets execution type to subprocess.Popen", CTS, True)
Handler.RegisterCommand("ls", "ls but is dir", ls, False)
Handler.RegisterCommand("pwd", "prints working directory", pwd, True)
Handler.RegisterCommand("cd", "overwrote cd to fix", cdhandler, False)


while True:
    try:
        OCmd = str(input(os.getcwd() + ">"))

        Args = OCmd.split(' ')
        Cmd = Args[0]
        del Args[0]

        Result = Handler.RunCommand(Cmd, Args)
        time.sleep(0.1)

        if Result != None:
            print(Result)
    except Exception as e:
        print(e)

