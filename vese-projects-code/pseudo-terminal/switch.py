import requests
import os

from vars import MENU, STATUS_ERROR, STATUS_ALIVE, STATUS_EXIT
from dotenv import load_dotenv

load_dotenv()
api_port= os.getenv("API_PORT")
api_addr= os.getenv("API_ADDR")

# K e y  ---> IUt0zFZKcPsLo2yek7OgSpockEd80LOA 

class SwitcherCommands(object):
    banner_text = "VeSe-Term"

    def arg_parser(self, cmd):
        """
            Commands are like help -h
            So we can split by '-'
            and pass everything to the command
        """
        full_cmd = str(cmd).split('-')
        command = full_cmd[0].strip()
        arguments = full_cmd[1:] if len(full_cmd) > 1 else []
        return command, arguments

    def get_command(self, arg):
        cmd, args = self.arg_parser(arg)
        method_name = 'cmd_' + str(cmd)
        # Get the method from 'self'. Default to a lambda
        method = getattr(self, method_name, lambda args=[]: ("Command not found.\nEnter \'help\' to display available commands\n".encode('utf-8'), True))
    
        # Call the method as we return it
        return method(args=args)

    def cmd_help(self, args=[]):
        s =  "".join("Commands available in the Virtual Terminal:\n")
        for cmd in MENU.keys():
            s += "{}: {}\n".format(cmd, MENU[cmd]["desc"])
            s +=  "\t{}\n".format(MENU[cmd]["help"]) if MENU[cmd]["help"] else ""
            for flag_arg in MENU[cmd]["usage"].keys():
                flag_desc = MENU[cmd]["usage"][flag_arg]
                s += "\t\t{}: {}\n".format(flag_arg, flag_desc) 
        return s.encode('utf-8'), STATUS_ALIVE

    def cmd_sensors(self, args=[]):
        url = "http://" + api_addr + ":" + api_port + "/sensors"
        s = ""
        try:
            r =requests.get(url)
            for sensor in r.json()["Sensors"]:
                s += "Sensor name: {}".format(sensor[0])
                s += "\nSensor min: {}".format(sensor[1])
                s += "|Sensor max: {}".format(sensor[2])
                s += "\nSensor min_safe: {}".format(sensor[3])
                s += "| Sensor max_safe: {}\n".format(sensor[4])
        except Exception as e:
            return str(e).encode('utf-8'), STATUS_ERROR
        return s.encode('utf-8'), STATUS_ALIVE
    
    def cmd_records(self, args=[]):
        url = "http://" + api_addr + ":" + api_port + "/records"
        s = ""
        try:
            r =requests.get(url)
            for record in r.json()["Records"]:
                s += "Record TOPIC: {}".format(record[1])
                s += "| Record VALUE: {}".format(record[2])
                s += "| DATE: {}\n".format(record[3])
        except Exception as e:
            return str(e).encode('utf-8'), STATUS_ERROR
        return s.encode('utf-8'), STATUS_ALIVE 

    def cmd_banner(self, args=[]):
        # 73b0c826e8be11fa266896bb1150d1844f88fc5458de5a0546b1a2344e9a57b8
        if len(args) > 0: 
            if args[0][0] == "s":
                str_args = "".join(args[0][1:])
                self.banner_text = str_args
                return "Banner set to {} correctly. Run `banner` again to display.\n".format(self.banner_text).encode('utf-8'), STATUS_ALIVE
            return "Args {}\nLen Args {}\n".format(args, len(args)).encode('utf-8'), STATUS_ALIVE
        else:
            cmd = "figlet {}".format(self.banner_text)
            return str(os.popen(cmd).read()).encode('utf-8'), STATUS_ALIVE

    def cmd_exit(self, args=[]):
        return "".encode('utf-8'), STATUS_EXIT
