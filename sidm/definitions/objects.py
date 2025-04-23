"""Define all commonly used objects"""

import awkward as ak
from sidm.tools.utilities import matched

# define helper functions
def pid(part, val):
    return part[abs(part.pdgId) == val]

def toPid(part, val):
    return part[ak.all(abs(part.children.pdgId) == val, axis=-1)]

def yesMu(lj):
    return lj[lj.muon_n > 0]

def noMu(lj):
    return lj[lj.muon_n == 0]

def noDsa(lj):
    return lj[lj.dsaMu_n == 0]

def noPf(lj):
    return lj[lj.pfMu_n == 0]

def noE(lj):
    return lj[lj.electron_n == 0]

def noPhoton(lj):
    return lj[lj.photon_n == 0]

def nE(lj, n):
    return lj[lj.electron_n == n]

def nPhoton(lj, n):
    return lj[lj.photon_n == n]

def onePhotonJet(lj):
    noE = (lj.electron_n == 0)
    noMu = (lj.muon_n == 0)
    onePho = (lj.photon_n == 1)
    return lj[noE & noMu & onePho]

def twoPhotonJet(lj):
    noE = (lj.electron_n == 0)
    noMu = (lj.muon_n == 0)
    twoPho = (lj.photon_n == 2)
    return lj[noE & noMu & twoPho]

def oneElectronJet(lj):
    oneE = (lj.electron_n == 1)
    noMu = (lj.muon_n == 0)
    noPho = (lj.photon_n == 0)
    return lj[oneE & noMu & noPho]

def twoElectronJet(lj):
    twoE = (lj.electron_n == 2)
    noMu = (lj.muon_n == 0)
    noPho = (lj.photon_n == 0)
    return lj[twoE & noMu & noPho]

def oneEoneP(lj):
    oneE = (lj.electron_n == 1)
    noMu = (lj.muon_n == 0)
    onePho = (lj.photon_n == 1)
    return lj[oneE & noMu & onePho]





# define objects whose definitions don't depend on LJs
preLj_objs = {}
preLj_objs["pvs"]        = lambda evts: evts.PV
preLj_objs["bs"]         = lambda evts: evts.BS
preLj_objs["met"]        = lambda evts: evts.MET
preLj_objs["hlt"]        = lambda evts: evts.HLT
preLj_objs["electrons"]  = lambda evts: evts.Electron
preLj_objs["photons"]    = lambda evts: evts.Photon
preLj_objs["muons"]      = lambda evts: evts.Muon
preLj_objs["dsaMuons"]   = lambda evts: evts.DSAMuon
preLj_objs["weight"]     = lambda evts: evts.genWeight
preLj_objs["gens"]       = lambda evts: evts.GenPart
preLj_objs["genMus"]     = lambda evts: pid(preLj_objs["gens"](evts), 13)
preLj_objs["genEs"]      = lambda evts: pid(preLj_objs["gens"](evts), 11)
preLj_objs["genAs"]      = lambda evts: pid(preLj_objs["gens"](evts), 32)
preLj_objs["genAs_toMu"] = lambda evts: toPid(preLj_objs["genAs"](evts), 13)
preLj_objs["genAs_toE"]  = lambda evts: toPid(preLj_objs["genAs"](evts), 11)
preLj_objs["rho_PFIso"]  = lambda evts: evts.fixedGridRhoFastjetAll
preLj_objs["jets"]       = lambda evts: evts.Jet

# define objects whose that will be added to objs by the sidm_processor after LJs are clustered
# and LJ cuts are applied. postLj_obj cuts can be applied to these
postLj_objs = {}
postLj_objs["mu_ljs"]       = lambda objs: yesMu(objs["ljs"])
postLj_objs["egm_ljs"]      = lambda objs: noMu(objs["ljs"])
postLj_objs["pfmu_ljs"]     = lambda objs: noDsa(objs["mu_ljs"])
postLj_objs["dsamu_ljs"]    = lambda objs: noPf(objs["mu_ljs"])
postLj_objs["electron_ljs"] = lambda objs: noPhoton(objs["egm_ljs"])
postLj_objs["photon_ljs"]   = lambda objs: noE(objs["egm_ljs"])

## defining categories
## photon jets
postLj_objs["one_photon_ljs"] = lambda objs: onePhotonJet(objs["ljs"])
postLj_objs["two_photon_ljs"] = lambda objs: twoPhotonJet(objs["ljs"])
## electron jets
postLj_objs["one_electron_ljs"] = lambda objs: oneElectronJet(objs["ljs"])
postLj_objs["two_electron_ljs"] = lambda objs: twoElectronJet(objs["ljs"])
## mixed one pho one elec
postLj_objs["one_e_one_p_ljs"] = lambda objs: oneEoneP(objs["ljs"])


# define objects that depend on extra parameters determined in hist or cut definitions
derived_objs = {}
derived_objs["n_electron_ljs"] = lambda objs, n: nE(objs["electron_ljs"], n)
derived_objs["n_photon_ljs"]   = lambda objs, n: nPhoton(objs["photon_ljs"], n)
derived_objs["genAs_matched_lj"]        = lambda objs, r: matched(objs["genAs"], objs["ljs"], r)
derived_objs["genAs_toMu_matched_lj"]   = lambda objs, r: matched(objs["genAs_toMu"], objs["ljs"], r)
derived_objs["genAs_toE_matched_lj"]    = lambda objs, r: matched(objs["genAs_toE"], objs["ljs"], r)
derived_objs["genAs_matched_muLj"]      = lambda objs, r: matched(objs["genAs"], objs["mu_ljs"], r)
derived_objs["genAs_toMu_matched_muLj"] = lambda objs, r: matched(objs["genAs_toMu"], objs["mu_ljs"], r)
derived_objs["genAs_matched_egmLj"]     = lambda objs, r: matched(objs["genAs"], objs["egm_ljs"], r)
derived_objs["genAs_toE_matched_egmLj"] = lambda objs, r: matched(objs["genAs_toE"], objs["egm_ljs"], r)
## adding new derived object
derived_objs['recoElectrons_matched_egmLj'] = lambda objs, r: matched(objs['electrons'], objs['egm_ljs'], r)
derived_objs['genAs_toE_matched_one_photon_ljs'] = lambda objs, r: matched(objs["genAs_toE"], objs["one_photon_ljs"], r)
derived_objs['genAs_toE_matched_two_photon_ljs'] = lambda objs, r: matched(objs["genAs_toE"], objs["two_photon_ljs"], r)
derived_objs['genAs_toE_matched_one_electron_ljs'] = lambda objs, r: matched(objs["genAs_toE"], objs["one_electron_ljs"], r)
derived_objs['genAs_toE_matched_two_electron_ljs'] = lambda objs, r: matched(objs["genAs_toE"], objs["one_electron_ljs"], r)
derived_objs['genAs_toE_matched_one_e_one_p_ljs'] = lambda objs, r: matched(objs["genAs_toE"], objs["one_e_one_p_ljs"], r)
## used matched instead of nearest
#derived_objs['genA_egmLj_ptRatio_PS'] = lambda objs: objs["egm_ljs"].pt / objs["egm_ljs"].nearest(objs["genAs_toE"], threshold=0.4).pt
derived_objs['genA_egmLj_ptRatio_PS'] = lambda objs: objs["egm_ljs"].pt / objs["egm_ljs"].nearest(objs["genAs_toE"], threshold=0.4).pt

derived_objs['genA_egmLj_oneEoneP_ptRatio_PS'] = lambda objs: objs["one_e_one_p_ljs"].pt / objs["one_e_one_p_ljs"].nearest(objs["genAs_toE"], threshold=0.4).pt


derived_objs['oneEoneP_ljs_within_ptRatio_lowT'] = lambda objs: objs["one_e_one_p_ljs"][derived_objs['genA_egmLj_oneEoneP_ptRatio_PS'](objs) < 1.2]

derived_objs['oneEoneP_ljs_within_ptRatio_highT'] = lambda objs: objs["one_e_one_p_ljs"][derived_objs['genA_egmLj_oneEoneP_ptRatio_PS'](objs) > 1.8]

derived_objs['egm_ljs_within_ptRatio'] = lambda objs: objs["egm_ljs"][derived_objs['genA_egmLj_ptRatio_PS'](objs) < 1.5]
derived_objs['genAs_toE_matched_egmLj_ptRatio_lt_1p5'] = lambda objs, r: matched(objs['genAs_toE'], derived_objs['egm_ljs_within_ptRatio'](objs), r)

derived_objs['genA_onePhoton_ptRatio'] = lambda objs: objs["one_photon_ljs"].pt / objs["one_photon_ljs"].nearest(objs["genAs_toE"], threshold=0.4).pt
derived_objs['genA_twoPhoton_ptRatio'] = lambda objs: objs["two_photon_ljs"].pt / objs["two_photon_ljs"].nearest(objs["genAs_toE"], threshold=0.4).pt
derived_objs['genA_oneElectron_ptRatio'] = lambda objs: objs["one_electron_ljs"].pt / objs["one_electron_ljs"].nearest(objs["genAs_toE"], threshold=0.4).pt
derived_objs['genA_twoElectron_ptRatio'] = lambda objs: objs["two_electron_ljs"].pt / objs["two_electron_ljs"].nearest(objs["genAs_toE"], threshold=0.4).pt
derived_objs['genA_one_e_one_p_ptRatio'] = lambda objs: objs["one_e_one_p_ljs"].pt / objs["one_e_one_p_ljs"].nearest(objs["genAs_toE"], threshold=0.4).pt

##
derived_objs['photon_to_electron_pt_ratio_1p1eLJ'] = lambda objs: objs["one_e_one_p_ljs"].photons.pt/objs["one_e_one_p_ljs"].photons.pt
