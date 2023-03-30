# CrystalPol

## Arquivo de Configuração - **config.yml**

No arquivo de Configuração temos as sequintes keywords:

```yaml
crystal_pol:
    mem: *obrigatorio*
    level: *obrigatorio*
    n_atoms: *obrigatorio*
    n_procs: 1
    pop: "chelpg"
    mult: [ 0, 1 ]
    charge_tolerance: 0.02
    simulation_dir: "simfiles"
    comment: "Crystal"
```

Estas keywords são utilizadas para controlar o comportamento do programa CrystalPol e de sua dependência Gaussian.

## Arquivo de input - **crystal.xyz**

O arquivo de input deve ter o formato

```
H   1.0000  1.0000  1.0000
```
Sendo que as primeiras **N** (valor derivado da keyword _**n_atoms**_) átomos devem ser da molécula da celula unitária a ser otimizada. 

Este arquivo pode ser obtido também retirando o header de um arquivo .gjf e o renomeando para .xyz