"""Define all available cuts"""

# columnar analysis
import awkward as ak
# local
from sidm.definitions.objects import derived_objs
from sidm.tools.utilities import dR, lxy


obj_cut_defs = {
    "pvs": {
        "ndof > 4": lambda objs: objs["pvs"].ndof > 4,
        "|z| < 24 cm": lambda objs: abs(objs["pvs"].z) < 24,
        "|rho| < 0.2 mm": lambda objs: abs(objs["pvs"].rho) < 0.2,
    },
    "ljs": {
        "pT > 30 GeV": lambda objs: objs["ljs"].pt > 30,
        "|eta| < 2.4": lambda objs: abs(objs["ljs"].eta) < 2.4,
        "dR(LJ, A) < 0.2": lambda objs: dR(objs["ljs"], objs["genAs"]) < 0.2,
    },
    "genAs": {
        "dR(A, LJ) < 0.2": lambda objs: dR(objs["genAs"], objs["ljs"]) < 0.2,
        "lxy < 10 cm": lambda objs: lxy(objs["genAs"]) < 10,
        "10 cm <= lxy < 100 cm": lambda objs: (lxy(objs["genAs"]) >= 10) & (lxy(objs["genAs"]) < 100),
        "lxy >= 100 cm": lambda objs: lxy(objs["genAs"]) >= 100,
    }
}

evt_cut_defs = {
    "PV filter": lambda objs: ak.num(objs["pvs"]) >= 1,
    "Cosmic veto": lambda objs: objs["cosmicveto"].result,
    ">=2 LJs": lambda objs: ak.num(objs["ljs"]) >= 2,
    ">=2 matched As": lambda objs: ak.num(derived_objs["matched_genAs"](objs, 0.2)) >= 2,
    # 4mu: leading two LJs are both mu-type
    "4mu": lambda objs: ak.count_nonzero(objs["ljs"][:, :2].muon_n >= 2, axis=-1) == 2,
    # 2mu2e: leading two LJs contain exactly 1 mu-type and exactly 1 egm-type
    "2mu2e": lambda objs: ((ak.count_nonzero(objs["ljs"][:, :2].muon_n >= 2, axis=-1) == 1)
                           & (ak.count_nonzero(objs["ljs"][:, :2].muon_n == 0, axis=-1) == 1)),
}
