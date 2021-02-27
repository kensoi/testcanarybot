import argparse
import importlib
import typing
import threading
import os
import sys
import time
import string
from .framework._application import _app as app

"""
testcanarybot Packaet (pocket manager) PREVIEW
Copyright 2021 andprokofieff
"""
packaet_root_raw = """'''

This is raw created root file for testcanarybot project.
fill all important info and try to run with python -m testcanarybot --run {packaet_project}

'''

community_name = '' # optional
community_token = ''
community_id = 0


community_service = '' # optional
apiVersion = '5.126' # optional
countThread = 5 # optional

bot_mentions = []
"""

packaet_manager_name = 'Packaet'
packaet_project_assets = 'assets'
packaet_project_library = 'library'
module_clear = "from testcanarybot import objects\nfrom testcanarybot import exceptions #handling and raising errors\n\"\"\"\n(c) kensoi.github.io, since 2020\n\"\"\"\nclass Main(objects.libraryModule):\n\tasync def start(self, tools: objects.tools):\n\t\tpass # create task at start\n\n\t@objects.ContextManager(commands = [\"check\"])\n\tasync def ContextManagerHandler(self, tools: objects.tools, package: objects.package):\n\t\tawait tools.api.message.send(random_id = tools.random_id, peer_id = package.peer_id, message = \"handler is working!\")"


def system_message(*args):
    print(packaet_manager_name, '>>', *args)

def gen_str(test = None):
    result, num = "", random.randint(5, 25)

    if isinstance(test, int):
        num = test

    while num != 0:
        result += random.choice([
                *string.ascii_lowercase,
                *string.digits]
        )
        num -= 1
    return result

def parsename(name: str):
    name = name.lower()
    test, i = len(name), 0
    while i< test:
        if name[i] not in [
                *string.ascii_lowercase,
                *string.digits]:
            name = name[:i] + name[i+1:]
            test -= 1

        else:
            i+= 1

    if name == '': name = 'module_' + gen_str()
    
    return name

class threadBot(threading.Thread):
    def __init__(self, data, botname):
        threading.Thread.__init__(self)
        self.botname = botname
        self.accessToken = data.community_token + ""
        self.groupId = data.community_id + 0
        self.serviceToken = "" if not hasattr(data, 'community_service') else data.community_service + ""
        self.apiVersion = "5.126" if not hasattr(data, 'apiVersion') else data.apiVersion + ""
        self.countThread = 5 if not hasattr(data, 'countThread') else data.countThread + 0


        if hasattr(testApp, 'mentions'):
            self.mentions = testApp.mentions[:]
        else:
            self.mentions = []

        self.start()

    def exception_handler(self, loop, context):
        print(traceback.format_exc())
        quit()


    def run(self):
        self.bot = app(
            self.accessToken, 
            self.groupId, 
            self.serviceToken, 
            self.apiVersion, 
            self.countThread, 
            os.getcwd() + '\\' + self.botname + '\\' + packaet_project_assets, 
            self.botname + '\\')
        if len(self.mentions) != 0: self.bot.setMentions(self.mentions)
        system_message(self.botname, "initialised, started")
        self.bot.start_polling()


packaet_parser = argparse.ArgumentParser(description = "TestCanaryBot Packaet [preview 00.09.111 dev]")

packaet_parser.add_argument("--run", type = str, default = "", help='Quick run')
packaet_parser.add_argument("--create", type = str, default = "", help='Create project')
packaet_parser.add_argument("--project", type = str, default = "", help='setting project')

packaet_parser.add_argument("--cm", type = str, default = "", help='[--project PROJECT] create module testcanarybot')
packaet_parser.add_argument("-f", dest = "folder", action = 'store_true', help='[--project PROJECT] create module in a folder')
args = packaet_parser.parse_args()
packaet_project_directory = args.run + args.create + args.project

if packaet_project_directory == '':
    system_message('Try to run command \"python testcanarybot -h\"')
    quit()

elif packaet_project_directory not in [args.run, args.create, args.project]:
    raise RuntimeError('2 or more args! \nTry to run command \"python testcanarybot -h\"')

projects = os.listdir(os.getcwd())
projects = [i for i in projects if i.count(".") == 0 and i not in ['testcanarybot', 'packaet', 'all', 'info']]

if args.run != '':
    sys.path.append(os.getcwd() + '\\')
    if packaet_project_directory == 'info':
        system_message('Projects at this directory:\n\t- ' + '\n\t- '.join(projects))

    elif packaet_project_directory == 'all':
        for i in projects:
            testApp = importlib.import_module(i + '.root')
            threadBot(testApp, i)
            time.sleep(1)

    elif packaet_project_directory in projects:
        testApp = importlib.import_module(packaet_project_directory + '.root')
        threadBot(testApp, packaet_project_directory)

    else:
        raise ValueError(f"Incorrect project name. Run \"python testcanarybot --create {packaet_project_directory}\" to create project, and try again")

elif args.create != '':
    system_message('Creating project <<', packaet_project_directory, '>>')
    
    if packaet_project_directory not in projects:
        system_message("Creating directories")

        os.mkdir(os.getcwd() + '\\' + packaet_project_directory)
        os.mkdir(os.getcwd() + '\\' + packaet_project_directory + '\\' + packaet_project_assets)
        os.mkdir(os.getcwd() + '\\' + packaet_project_directory + '\\' + packaet_project_library)

        system_message("Creating << root >>")

        with open(os.getcwd() + '\\' + packaet_project_directory + '\\' + 'root.py', 'w+') as root:
            root.write(packaet_root_raw)

        system_message("Creating << readme >>")

        with open(os.getcwd() + '\\' + packaet_project_directory + '\\' + packaet_project_library + '\\readme.txt', 'w+') as readme:
            readme.write("""testcanarybot library
Copyright 2021 andprokofieff

Create project: python testcanarybot --project """ + packaet_project_directory + """ --cm MODULENAME"""
                )
        
        with open(os.getcwd() + '\\' + packaet_project_directory + '\\' + packaet_project_assets + '\\readme.txt', 'w+') as readme:
            readme.write("""testcanarybot assets
Copyright 2021 andprokofieff

Usage: with tools.assets(*args) as file: #like open(*args, **kwargs)
    #file usage
            """
            )
        system_message(f"Done! \n\tDirectory: ./{packaet_project_directory}/ \n\tUsage: python testcanarybot --run {packaet_project_directory}")
    
    else:
        raise RuntimeError("Folder exists! Try another name")

elif args.project != '':
    system_message("manager for <<", packaet_project_directory, ">>")

    if args.cm != '':
        packaet_module_name = parsename(args.cm) # if args.cm != '' else 'handler_' + gen_str(15)
        packaet_module_inFolder = args.folder

        if packaet_module_inFolder:
            os.mkdir(os.getcwd() + '\\' + packaet_project_directory + '\\library\\' + packaet_module_name)
            
            system_message("created folder <<", packaet_module_name, ">>")
            
            with open(os.getcwd() + '\\' + packaet_project_directory + '\\library\\' + packaet_module_name + "\\main.py") as module:
                module.write(module_clear)
            
            system_message("Done! Results at ./" + packaet_project_directory + "/library/")

        else:
            system_message("created file <<", packaet_module_name, ">>")
            
            with open(os.getcwd() + '\\' + packaet_project_directory + '\\library\\' + packaet_module_name + ".py") as module:
                module.write(module_clear)
            
            system_message("Done! Results at ./" + packaet_project_directory + "/library/")