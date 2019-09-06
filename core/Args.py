# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import sys, os, argparse
from core.Colors import *
from core.Logs import *


class SpraykatzParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        print("\n%sError: %s\n" % (warningRed, message))
        sys.exit(2)

def parseArgs(parser):
    args = parser.parse_args()

    if args.methods:
        args.methods = args.methods.split(',')

    if os.path.isfile(args.targets):
        args.targets = [line.rstrip('\n') for line in open(args.targets)]
    else:
        args.targets = args.targets.split(',')

    setLogging(args.verbosity)

    return args

def menu():
    parser = SpraykatzParser(prog="spraykatz.py", description="A tool to spray love around the world!", epilog="Example : ./spraykatz.py -d domain.local -u localadmin -p L0c4l4dm1n -t 192.168.0.0/24")

    mandatoryArgs = parser.add_argument_group('Mandatory Arguments')
    mandatoryArgs.add_argument("-d", "--domain", help="User's domain. If he is not member of a domain, simply use -d . instead.", required=True, default=".")
    mandatoryArgs.add_argument("-u", "--username", help="User to spray with. He must have admin rights on targeted systems in order to gain remote code execution.", required=True)
    mandatoryArgs.add_argument("-p", "--password", help="User's password or NTLM hash in the LM:NT format.", required=True)
    mandatoryArgs.add_argument("-t", "--targets", help="IP addresses and/or IP address ranges. You can submit them via a file of targets (one target per line), or inline (separated by commas).", required=True)

    optionalArgs = parser.add_argument_group('Optional Arguments')
    optionalArgs.add_argument("-k", "--keep", help="Keep dumps into misc/dumps (no deletion when spraykatz ends).", action="store_true") 
    optionalArgs.add_argument("-m", "--methods", help="Methods used for spraying. Can be wmiexec, atexec or smbexec. Default: wmiexec.", choices=['wmiexec', 'atexec', 'smbexec'], default=None)
    optionalArgs.add_argument("-s", "--server", help="Specify the type of server to use. (default: smb).", choices=['smb'],  default="smb")
    optionalArgs.add_argument("-v", "--verbosity", help="Verbosity mode.", choices=['warning', 'info', 'debug'], default="info")
    optionalArgs.add_argument("-w", "--wait", help="Timeout for each procdump thread. Default: 60 seconds. A low timeout may gives bad dumps. Do not hesitate to increase timeout in case of bad dumps.", default=60)

    return parser
