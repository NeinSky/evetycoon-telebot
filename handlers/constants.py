MESSAGE_UNKNOWN_COMMAND = """
I'm sorry, I can't understand you. Please use /help to see the list of available commands.
"""


MESSAGE_START = """
Hello, {user}!\n

I am EveTycoon API bot - an (almost) perfect tool for miners and industrialists alike!\n
I can provide market statistics, best buy and sell orders for basic minerals in empire space.\n
You can start by typing or selecting /help command, which (hopefully) will provide all information necessary.\n\n
Available commands:\n
/stats
/wtb
/wts
/history
"""

MESSAGE_MINERAL_CHOICE = """
Please select mineral type.
"""

MESSAGE_FILTER_CHOICE = """
Please select scope. Top 5 regions will be chosen.\n\n
Amarr - empire regions statistic.\n
Caldari - state regions statistic.\n
Gallente - federation regions statistic.\n
Minmatar - republic regions statistic.\n
All - top 5 regions among all.
"""

MESSAGE_SYSTEM_FILTER = """
Please select security level of systems you want to see orders:\n

HIGHSEC - only high security space (sec. status >= 0.5).\n
LOWSEC - high and low security space (0.5 > sec. status > 0).\n
All - high, low and null security space.
"""


MESSAGE_MAY_TAKE_SOME_TIME = """
Request accepted! It may take few seconds, please standby, pilot!
"""

MESSAGE_NO_REQUESTS_FOUND = """
No requests found. Please do more requests to see history.
"""

MESSAGE_HISTORY_WRONG_REQUEST = """
Cannot repeat this request. Please use /history command again and click one of the button bellow.
"""