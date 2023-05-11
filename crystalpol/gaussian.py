from crystalpol.shared.utils.ptable import atom_symbol
from crystalpol.shared.system.crystal import Crystal
from crystalpol.shared.config import Config

from pathlib import Path, PosixPath
from typing import TextIO, Union, List
import subprocess
import textwrap
import shutil
import sys
import os


class Gaussian:
    __slots__ = ('qmprog', 'config', 'keywords')

    def __init__(self, config: Config) -> None:
        self.qmprog = "g16"
        self.config = config

        self.check_keyword()

    def check_keyword(self):
        if self.config.pop not in ["chelpg", "mk", "nbo"]:
            self.config.pop = "chelpg"

    def run(self, cycle: int, crystal: Crystal) -> List[float]:

        file = Path(
            self.config.simulation_dir,
            f"crystal-{str(cycle).zfill(2)}",
            f"crystal-{str(cycle).zfill(2)}.gjf"
        )
        self.create_step_dir(cycle)
        self.make_gaussian_input(cycle, file, crystal)

        if shutil.which("bash") is not None:
            exit_status = subprocess.call(
                [
                    "bash",
                    "-c",
                    "exec -a {}-step{} {} {}".format(
                        self.qmprog, cycle, self.qmprog, str(file)
                    ),
                ]
            )
        else:
            exit_status = subprocess.call([self.qmprog, file.name])

        if exit_status != 0:
            raise RuntimeError("Gaussian process did not exit properly")

        return self.read_charges_from_gaussian_output(
            cycle,
            crystal.get_number_of_charges()
        )

    def create_step_dir(self, cycle):
        step_dir = Path(
            self.config.simulation_dir,
            f"crystal-{str(cycle).zfill(2)}"
        )
        if not os.path.exists(step_dir):
            os.makedirs(step_dir)
        else:
            raise RuntimeError(
                f"Step directory '{str(step_dir)}' already exists. "
                f"Please remove it before proceeding."
            )

    def create_simulation_dir(self):
        if not os.path.exists(self.config.simulation_dir):
            os.makedirs(self.config.simulation_dir)
        else:
            raise RuntimeError(
                f"Simulation directory '{self.config.simulation_dir}' already exists. "
                f"Please remove it before proceeding."
            )

    def make_gaussian_input(self, cycle: int, file: Union[PosixPath, Path], crystal: Crystal) -> str:

        with open(file, 'w+') as fh:

            fh.write(f"%Mem={self.config.mem}Gb\n")

            fh.write(f"%Nprocs={self.config.n_procs}\n")

            kwords_line = f"#P {self.config.level} " \
                          f"Pop={self.config.pop} " \
                          f"Density=Current " \
                          f"NoSymm "

            if cycle > 1:
                kwords_line += f"charge"

            fh.write(textwrap.fill(kwords_line, 90))
            fh.write("\n")

            fh.write(f"\n{self.config.comment} - Cycle number {cycle}\n")
            fh.write("\n")
            fh.write(f"{self.config.mult[0]} {self.config.mult[1]}\n")

            for atom in crystal[0][0]:
                symbol = atom_symbol[atom.na]
                fh.write(
                    f"{symbol:<2s}    "
                    f"{float(atom.rx):>10.5f}    "
                    f"{float(atom.ry):>10.5f}    "
                    f"{float(atom.rz):>10.5f}\n"
                )

            fh.write("\n")

            if cycle > 1:
                self.make_gaussian_charges(fh, crystal)

            fh.seek(0)
            return fh.read()

    @staticmethod
    def make_gaussian_charges(fh: TextIO, crystal: Crystal) -> None:

        for index_cell, cell in enumerate(crystal):
            for index_mol, molecule in enumerate(cell):
                if (index_cell == 0 and index_mol != 0) or (index_cell != 0):
                    for atom in molecule:
                        fh.write(
                            f"{float(atom.rx):>10.5f}    "
                            f"{float(atom.ry):>10.5f}    "
                            f"{float(atom.rz):>10.5f}    "
                            f"{float(atom.chg):>10.5f}\n"
                        )

    def read_charges_from_gaussian_output(self, cycle, number_of_charges: int) -> List[float]:
        step_dir = Path(
            self.config.simulation_dir,
            f"crystal-{str(cycle).zfill(2)}"
        )
        filename = f"crystal-{str(cycle).zfill(2)}.log"

        file = Path(step_dir, filename)
        try:
            with open(file) as data:
                lines = data.readlines()
        except FileNotFoundError:
            sys.exit("Error: cannot open file {}".format(file))

        start = lines.pop(0).strip()
        while start != "Fitting point charges to electrostatic potential":
            start = lines.pop(0).strip()

        lines = lines[3:]  # Consume 3 more lines

        return list(
            map(
                lambda x: float(x.split()[2]),
                lines[:number_of_charges]
            )
        )
