from crystalpol.polarization import Polarization
from crystalpol.shared.config import Config

from yaml.loader import SafeLoader
import yaml

import setproctitle
import argparse
import os


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

    try:
        with open(args.config) as file:
            data = yaml.load(file, Loader=SafeLoader)
            config = Config(**data.get('crystal_pol'))
    except IOError:
        raise RuntimeError('Invalid or Missing Config File.')

    pol = Polarization(args.infile, args.outfile, config)
    pol.run()


if __name__ == "__main__":
    main()
