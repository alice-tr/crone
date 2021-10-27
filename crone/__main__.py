"""Crone.

Usage:
  crone foretell [--cronexp]
  crone foretell <timing> <command> [--cronexp]
  crone (-h | --help)
  crone --version

Options:
  --cronexp     Output as CRON expression.
  -h --help     Show this screen.
  --version     Show version.

Examples:
  $ crone foretell "under the full moon" "echo 'BOO'"
"""

from docopt import docopt

from .cmd import run_from_docopt

if __name__ == '__main__':
	arguments = docopt(__doc__, version='Crone 0.0.1')
	run_from_docopt(arguments)
