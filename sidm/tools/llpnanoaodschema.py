from coffea.nanoevents import NanoAODSchema


class LLPNanoAODSchema(NanoAODSchema):
    """LLPNano schema builder

    LLPNano is an extended NanoAOD format that includes DSA Muons and improved displacement info
    """

    mixins = {
        **NanoAODSchema.mixins,
        "DSAMuon": "Muon",
    }
    all_cross_references = {
        **NanoAODSchema.all_cross_references,
        "DSAMuon_muonMatch1idx": "Muon",
    }

    @property
    def behavior(cls):
        """Behaviors necessary to implement this schema (dict)"""
        from coffea.nanoevents.methods import nanoaod

        return nanoaod.behavior
