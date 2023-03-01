import os

from crystalpol.shared.system.molecule import Molecule
from crystalpol.shared.system.crystal import Crystal
from crystalpol.shared.system.atom import Atom
from crystalpol.shared.config import Config
from crystalpol.gaussian import Gaussian

from typing import List, Tuple

import sys

from crystalpol.shared.utils.log import Log


class Polarization:
    __slots__ = ('geom_file', 'outfile', 'config', 'gaussian', 'crystal')

    def __init__(self, geom_file: str, outfile: str, config: Config) -> None:
        self.crystal = None

        self.geom_file = geom_file
        self.outfile = outfile
        self.config = config

        self.gaussian = Gaussian(config)

    def run(self):

        self.gaussian.create_simulation_dir()

        self.read_crystal()

        cycle = 1
        max_charge_diff = sys.float_info.max
        while max_charge_diff >= self.config.charge_tolerance:

            max_charge_diff, charge_diff = self.update_crystal_charges(
                self.gaussian.run(cycle, self.crystal),
            )

            Log.make_run(
                cycle,
                max_charge_diff if cycle != 1 else 0,
                charge_diff,
                self.crystal
            )

            cycle += 1

    def read_crystal(self) -> None:
        with open(self.geom_file, 'r') as geom_file:
            lines = geom_file.readlines()

        molecules = self._get_molecules_from_lines(lines)
        structure = self._get_crystal_structure(molecules[0])

        self.crystal = Crystal([structure])
        for molecule in molecules:
            self.crystal.add_cell([molecule])

    def update_crystal_charges(self, charges: List[float]) -> Tuple[float, list]:

        charge_diff = []

        for cell in self.crystal:
            for molecule in cell:
                for index, atom in enumerate(molecule):
                    if atom.chg:
                        charge_diff.append(abs(atom.chg - charges[index]))
                    atom.chg = charges[index]

        max_charge_diff = abs(max(charge_diff, key=abs)) if charge_diff else sys.float_info.max

        return max_charge_diff, charge_diff

    def _get_molecules_from_lines(self, lines: List[str]) -> List[Molecule]:
        if (len(lines) % self.config.n_atoms) == 0:
            molecules: List[Molecule] = []

            for index, molecule in enumerate(self.split(lines, self.config.n_atoms)):
                mol = Molecule(f"Molecule-{index}")
                for atom_line in molecule:
                    symbol, rx, ry, rz = tuple(atom_line.split())
                    mol.add_atom(
                        Atom(
                            rx, ry, rz,
                            symbol=symbol.ljust(2),
                        )
                    )
                molecules.append(mol)

            return molecules

        else:
            raise RuntimeError(
                "Invalid Geom File, the number of atoms doesn't match the number of lines."
            )

    @staticmethod
    def _get_crystal_structure(molecule: Molecule) -> List[str]:
        structure: List[str] = []
        for atom in molecule:
            structure.append(atom.symbol)
        return structure

    @staticmethod
    def split(array: List, partitions: int):
        for i in range(0, len(array), partitions):
            yield array[i: i + partitions]
