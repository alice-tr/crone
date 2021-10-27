# :mage_woman: Crone :crescent_moon:


Auspicious command scheduling.


## CLI Mode
```console
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
  $ crone foretell "under the full moon" "echo BOO"
```

### Example
```console
$ python -m crone foretell "under the full moon" "echo BOO"
```

```console
under the full moon ,
   echo BOO

    Next Chance: in 3 weeks (08:57 on 11-19-21, UTC+00:00)
CRON Expression: 57 8 19 11 * echo BOO
```


## Notes
- you can invoke some commands (e.g. `foretell`) with no arguments to start an interactive prompt
- limited geolocation, timezone support (i.e. assumes Greenwich/UTC)
- limited to information output only (does not interact with `cron`)


## Thanks to
- astrological calculations handled by [flatlib](https://github.com/flatangle/flatlib)
- date utilities handled by [pendulum](https://github.com/sdispater/pendulum)
- command line invocation handled by [docopt](https://github.com/docopt/docopt)
- interactive prompt handled by [python-inquirer](https://github.com/magmax/python-inquirer)
