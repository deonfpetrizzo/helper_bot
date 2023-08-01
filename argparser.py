import sys

class ArgParser:
	def __init__(self):
		self.prog_name = self.__parse_prog_name()
		self.cmd = self.__parse_cmd()
		self.opts = self.__parse_opts()
		self.args = self.__parse_args()

	def __parse_prog_name(self):
		return sys.argv[0]

	def __parse_cmd(self):
		return sys.argv[1]

	def __parse_opts(self):
		options = []
		for i in range(2, len(sys.argv)):
			if sys.argv[i][0] == "-":
				options.append(sys.argv[i])
		return options

	def __parse_args(self):
		args = []
		for i in range(2, len(sys.argv)):
			if sys.argv[i][0] != "-":
				args.append(sys.argv[i])
		return args