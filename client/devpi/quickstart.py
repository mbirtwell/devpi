"""
perform a quickstart initialization of devpi-server and devpi-client.
"""
import os
import time
import py

def main(hub, args):
    clientdir = py.path.local(args.clientdir)
    if clientdir.check() or clientdir.dirpath("server").check():
        hub.fatal("client or server dir exists, cannot perform quickstart. "
                  "If you have a server running, please kill it and "
                  "afterwards remove %s" %(clientdir.dirpath()))

    hub.popen(["devpi", "server", "--start"])
    try:
        hub.popen(["devpi", "use", "http://localhost:3141"])
        hub.popen(["devpi", "user", "-c", args.user,
                                   "password=%s" % args.password])
        hub.popen(["devpi", "login", args.user,
                                   "--password=%s" % args.password])
        hub.popen(["devpi", "index", "-c", args.index,])
        hub.popen(["devpi", "use", args.index,])
    except SystemExit:
        hub.info("stopping server because of failure")
        hub.popen(["devpi", "server", "--stop"])
        raise SystemExit(1)

    hub.info("COMPLETED!  you can now work with your %r index" %(args.index))
    hub.info("  devpi install PKG   # install a pkg from pypi")
    hub.info("  devpi upload        # upload a setup.py based project")
    hub.info("  devpi test PKG      # download and test a tox-based project ")
    hub.info("  devpi PUSH ...      # to copy releases between indexes")
    hub.info("  devpi index ...     # to manipulate/create indexes")
    hub.info("  devpi user ...      # to manipulate/create users")
    hub.info("  devpi server ...    # to control the background server")
    hub.info("for options see 'devpi -h', for docs http://doc.devpi.net")