MENU={
    "help": {
        "desc": "It displays all commands available and how to use them",
        "help": "",
        "usage": {}
    },
    "sensors": {
        "desc": "Shows information about sensors",
        "help": "Command `sensors` does not accept arguments.",
        "usage": {
           
        }
    },
    "records": {
        "desc": "Shows last 10 records",
        "help": "Command `records` does not accept arguments",
        "usage":{}
        
    },
    "banner": {
        "desc": "Banner configuration. By default it displays the current banner.",
        "help": "banner [[-s]]",
        "usage": {
            "-s": "Allows to set a text as banner"
        }
    },
    "exit": {
        "desc": "Exit program. It does not save current state (IN PROGRESS)",
        "help": "Command `exit` does not accept arguments",
        "usage": {}
    }
}


# Status Code 

STATUS_ERROR = 1
STATUS_ALIVE = 2
STATUS_EXIT  = 3
