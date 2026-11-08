"""CosmoSIS module for S8-WL Part 2 (Spiral pairs): load a model's P(k, z), distances and growth from the file written by
axiclass_pk.py, in place of a Boltzmann code. Option:  pk_file = path to pk_<run>.npz"""
import numpy as np
from cosmosis.datablock import names, option_section


def setup(options):
    return dict(np.load(options.get_string(option_section, "pk_file")))


def execute(block, d):
    zb = d["z_bg"]
    block[names.cosmological_parameters, "h0"] = float(d["h0"])
    block[names.cosmological_parameters, "omega_m"] = float(d["omega_m"])
    block[names.cosmological_parameters, "sigma_8"] = float(d["sigma_8"][0])
    dm = d["d_m"]
    block[names.distances, "z"] = zb
    block[names.distances, "a"] = 1 / (1 + zb)
    block[names.distances, "d_c"] = dm
    block[names.distances, "d_m"] = dm
    block[names.distances, "d_a"] = dm / (1 + zb)
    block[names.distances, "d_l"] = dm * (1 + zb)
    block[names.distances, "h"] = d["h"]
    block[names.distances, "nz"] = len(zb)
    for tag, sec in (("lin", names.matter_power_lin), ("nl", names.matter_power_nl)):
        block.put_grid(sec, "z", d["z_pk"], "k_h", d["k_h"], "p_k", d[f"p_k_{tag}"])
    zg = d["z_growth"]
    block[names.growth_parameters, "z"] = zg
    block[names.growth_parameters, "a"] = 1 / (1 + zg)
    block[names.growth_parameters, "d_z"] = d["d_z"]
    block[names.growth_parameters, "f_z"] = d["f_z"]
    block[names.growth_parameters, "sigma_8"] = d["sigma_8"]
    return 0
