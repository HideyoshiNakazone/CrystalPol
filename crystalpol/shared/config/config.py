from dataclasses import dataclass, field, fields, asdict


@dataclass
class Config:
    mem: int
    level: str
    n_atoms: int

    n_procs: int = 1
    pop: str = "chelpg"
    charge_tolerance = 0.02
    comment: str = "crystalpol"
    simulation_dir = "simfiles"
    mult: list = \
        field(default_factory=lambda: [0, 1])

    def __post_init__(self):
        for field in fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, field.type):
                raise ValueError(
                    f'Expected {field.name} to be {field.type}, '
                    f'got {repr(value)}'
                )

        if self.mem is None or self.mem <= 0:
            raise ValueError(
                f'Invalid value for mem: {self.mem},'
                f'Memory must be a integer greater than 0.'
            )

        if self.n_atoms is None or self.n_atoms <= 0:
            raise ValueError(
                f'Invalid value for n_atoms: {self.mem},'
                f'Number of Atoms must be a integer greater than 0.'
            )

    def to_dict(self):
        return asdict(self)
