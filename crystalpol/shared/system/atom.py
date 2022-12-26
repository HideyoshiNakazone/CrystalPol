from crystalpol.shared.utils.ptable import atom_mass, atom_symbol


class Atom:
    """
    Atom class declaration. This class is used throughout the DicePlayer program to represent atoms.
    Attributes:
        na (int): Atomic number of the represented atom.
        symbol (str): Atomic symbol of the represented atom.
        rx (float): x cartesian coordinates of the represented atom.
        ry (float): y cartesian coordinates of the represented atom.
        rz (float): z cartesian coordinates of the represented atom.
    """

    def __init__(
            self,
            rx: float,
            ry: float,
            rz: float,
            na: int = None,
            symbol: str = None,

    ) -> None:
        """
        The constructor function __init__ is used to create new instances of the Atom class.
        Args:
            na (int): Atomic number of the represented atom.
            symbol (str): Atomic symbol of the represented atom.
            rx (float): x cartesian coordinates of the represented atom.
            ry (float): y cartesian coordinates of the represented atom.
            rz (float): z cartesian coordinates of the represented atom.
        """

        if na is not None:
            self.na = na
            self.symbol = atom_symbol[self.na]

        if symbol is not None and symbol in atom_symbol:
            self.symbol = symbol
            self.na = atom_symbol.index(self.symbol)

        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.chg = None
        self.mass = atom_mass[self.na]
