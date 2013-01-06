import argparse
import sys
from wsgiref.simple_server import make_server

from trouvailles import __version__, logger
from trouvailles.server import main as webapp
from trouvailles.util import LOG_LEVELS, configure_logger
from trouvailles.db import Database


def main():
    parser = argparse.ArgumentParser(description='Indexation Service')
    parser.add_argument('--database', help='Xapian Database path',
                        default='/tmp/trouvailles')
    parser.add_argument('--version', action='store_true',
                        default=False,
                        help='Displays Marteau version and exits.')
    parser.add_argument('--log-level', dest='loglevel', default='info',
                        choices=LOG_LEVELS.keys() + [key.upper() for key in
                                                     LOG_LEVELS.keys()],
                        help="log level")
    parser.add_argument('--log-output', dest='logoutput', default='-',
                        help="log output")
    parser.add_argument('--host', help='Host', default='0.0.0.0')
    parser.add_argument('--port', help='Port', type=int, default=8080)
    args = parser.parse_args()

    if args.version:
        print(__version__)
        sys.exit(0)

    # configure the logger
    configure_logger(logger, args.loglevel, args.logoutput)

    # loading the app & the queue
    global_config = {}
    settings = {'database': Database(args.database, create=True)}

    app = webapp(global_config, **settings)

    try:
        httpd = make_server(args.host, args.port, app)
        logger.info('Trouvailles Server running at http://%s:%s.' %
                    (args.host, args.port))
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        logger.info('Bye!')


if __name__ == '__main__':
    sys.exit(main())
