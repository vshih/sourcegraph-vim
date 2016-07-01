import os
import sys
import vim
from threading import Thread
sys.path.append(os.path.dirname(vim.eval("s:path")))
import sourcegraph_lib
import socket
import json
import base64
import logging


def get_vim_variable(variable_name):
	var_exists = vim.eval("exists('%s')" % variable_name)
	if var_exists is not '0':
		return vim.eval(variable_name)
	return None

log_file = get_vim_variable("g:SOURCEGRAPH_LOG_FILE")
if log_file is None:
    log_file = "/tmp/sourcegraph-vim.log"

class Logger:

    def __init__(self, log_file):
        self.log_file = log_file
        self._setup_logging()
        return

    def _setup_logging(self):
        root = logging.getLogger()
        if root.handlers:
            for handler in root.handlers:
                root.removeHandler(handler)
                logging.basicConfig(filename=self.log_file, filemode='w', level=logging.DEBUG)
            self.log_output('logging', 'setup logging @ %s' % self.log_file)

    def log_output(self, log_category, log_message, log_console=False):
        output_string = '[%s] %s' % (log_category, log_message)
        logging.debug(output_string)
        if log_console:
            vim.eval("echoerr %s" % log_message)

    def log_error(self, log_category, log_message, log_console=False):
        output_string = '[%s] %s' % (log_category, log_message)
        logging.error(output_string)
        if log_console == True:
            vim.eval("echoerr %s" % log_message)

logger = Logger(log_file)



_SOCKET_FILE = "/tmp/app.sourcegraph"

def send_request_to_socket(vim_variables):
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        message = {"type": "sourcegraph-editor", "data": vim_variables}
        message_json = json.dumps(message)
        logger.log_output("editor", message)
	try:
		sock.connect(_SOCKET_FILE)
		sock.send(bytes(message_json))
		sock.send(bytes("\f"))
	except Exception as error:
                logger.log_output("network", error)
	finally:
		sock.close()

def get_file_buffer(filename, curr_word, curr_offset, numlines):
	lines = []
	for i in range(1, numlines + 1):
		currline = vim.eval("getline('%s')" % str(i))
		lines.append(currline)
        return "\n".join(lines)


VIM_VARS = ["is_dirty", "filename", "selected_token", "cursor_offset", "numlines"]

def get_vim_variables():
    variables = {}
    for variable in VIM_VARS:
        variables[variable] = vim.eval("s:%s" %variable)
    variables["numlines"] = int(variables["numlines"])
    variables["file_buffer"]  = get_file_buffer(variables["filename"], variables["selected_token"], variables["cursor_offset"], variables["numlines"])
    variables["file_buffer"]  = base64.b64encode(variables["file_buffer"]).decode("utf-8")
    variables["is_dirty"] = True if int(variables["is_dirty"]) == 1 else False
    return variables

vim_variables = get_vim_variables()
logger.log_output("editor ",  str(vim_variables))
send_request_to_socket(vim_variables)
