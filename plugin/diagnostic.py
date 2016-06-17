import sys
import os
import getopt
sys.path.append(os.path.dirname(__file__))
import sourcegraph_lib

def validate_settings(settings):
	# Validate that we have access to a working shell
	print("%sChecking if shell is supported." % ("-" * 8))
	if not sourcegraph_lib.is_windows() and 'SHELL' not in settings.ENV:
		return sourcegraph_lib.ERR_UNRECOGNIZED_SHELL

	print("%sChecking if `pwd` works on the shell." % ("-" * 8))
	if not sourcegraph_lib.is_windows():
		out, err, return_code = sourcegraph_lib.run_shell_command(['pwd'], settings.ENV)
		if return_code != 0:
			return sourcegraph_lib.ERR_UNRECOGNIZED_SHELL

	print("%sChecking GOPATH settings." % ("-" * 8))
	gopath_err = sourcegraph_lib.check_gopath(settings.ENV)
	if gopath_err:
		return gopath_err

	print("%sRunning go binary and checking version." % ("-" * 8))
	go_err = sourcegraph_lib.check_go(settings)
	if go_err:
		return go_err

	# Check that godefinfo is available
	print("%sChecking if godefinfo binary is in $GOPATH/bin, and running godefinfo -v." % ("-" * 8))
	godefinfo_command = ['godefinfo', '-v']
	out, err, return_code = sourcegraph_lib.run_shell_command(godefinfo_command, settings.ENV)
	if return_code != 0:
		return sourcegraph_lib.ERR_GODEFINFO_INSTALL

def main(argv=None):
	if argv is None:
		argv = sys.argv

	try:
		opts, args = getopt.getopt(argv[1:], 'g:b:')
	except getopt.error:
		print("Error retrieving arguments.")

	gopath = None
	gobin = None
	for o, a in opts:
		if o == "-g":
			gopath = a
		elif o == "-b":
			gobin = a

	print("-" * 25)
	print("Running diagnostic for Sourcegraph for your editor. If you need to override values, pass them in as arugments as such:")
	print("python diagnostic.py -g /path/to/gopath -b /path/to/go/binary")
	print("-" * 25)
	print("%sPrinting settings object with default values." % ("-" * 4))
	settings = sourcegraph_lib.Settings()
	print(settings)
	if gopath or gobin:
		print("%sPrinting settings object with overidden values." % ("-" * 4))
		if gobin:
			settings.GOBIN = gobin.strip()
		if gopath:
			settings.ENV['GOPATH'] = str(gopath.rstrip(os.sep)).strip()
		print(settings)
	print("%sVERIFY GOPATH and PATH settings, to ensure that the go binary is in the PATH, and GOPATH is correctly set." % ("-" * 4))
	print("%sValidating settings object. If value is not none, Sourcegraph for your editor is not configured properly." % ("-" * 4))
	validate_response = validate_settings(settings)
	print("%sVERIFY output of validate settings is None: %s" % ("-" * 4, validate_response))
	if validate_response is not None:
		print("Exiting diagnostic because settings validation returned non-None value.")
		sys.exit(1)
	print("%sAssembling Sourcegraph object." % ("-" * 4))
	sourcegraph_object = sourcegraph_lib.Sourcegraph(settings)
	print("%sVERIFY that $GOPATH/bin is in the path. PATH = %s" % ("-" * 4, settings.ENV['PATH']))
	sourcegraph_object.post_load(godefinfo_update=True)
	print("%sTesting browser settings." % ("-" * 4))
	sourcegraph_object.open_channel_os()
	print("%sVERIFY browser opens." % ("-" * 4))
	print("\n\n\n")
	print("-" * 25)
	print("Diagnostic completed.")
	print("-" * 25)
if __name__ == "__main__":
	sys.exit(main())
