from crystalpol.polarization import Polarization
from crystalpol.shared.config import Config

from yaml.loader import SafeLoader
import yaml

from pathlib import Path
import setproctitle
import argparse
import logging
import sys
import os

from crystalpol.shared.utils import weekday_date_time
from crystalpol.shared.utils.log import Log

__VERSION = "v0.0.1"
os.nice(+19)
setproctitle.setproctitle("crystalpol-{}".format(__VERSION))


def main():
    """
    Read and store the arguments passed to the program
    and set the usage and help messages.
    """

    parser = argparse.ArgumentParser(prog="CrystalPol")
    parser.add_argument(
        "-v", "--version", action="version", version=f"crystalpol-{__VERSION}"
    )
    parser.add_argument(
        "-c", "--config",
        dest="config",
        default="config.yml",
        metavar="INFILE",
        help="Config file of crystalpol [default = config.yml]"
    )
    parser.add_argument(
        "-i", "--input",
        dest="infile",
        default="crystal.xyz",
        metavar="INFILE",
        help="Input file of crystalpol [default = crystal.xyz]"
    )
    parser.add_argument(
        "-o", "--output",
        dest="outfile",
        default="run.log",
        metavar="OUTFILE",
        help="Output file of crystalpol [default = run.log]"
    )
    args = parser.parse_args()

    log_file = Path("run.log")
    if log_file.exists():
        log_file.rename(log_file.with_suffix(".log.backup"))

    logging.basicConfig(
        filename=args.outfile,
        format='%(message)s',
        level=logging.INFO
    )

    try:
        with open(args.config) as file:
            data = yaml.load(file, Loader=SafeLoader)
            config = Config(**data.get('crystal_pol'))
    except IOError:
        raise RuntimeError('Invalid or Missing Config File.')

    Log.make_header(__VERSION, config.to_dict())

    pol = Polarization(args.infile, args.outfile, config)
    pol.run()


if __name__ == "__main__":
    main()
