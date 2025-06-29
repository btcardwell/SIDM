from coffea.nanoevents import NanoAODSchema


class LLPNanoAODSchema(NanoAODSchema):
    """LLPNano schema builder

    LLPNano is an extended NanoAOD format that includes DSA Muons and improved displacement info
    """

    mixins = {
        **NanoAODSchema.mixins,
        "DSAMuon": "DSAMuon",
    }
    all_cross_references = {
        **NanoAODSchema.all_cross_references,
        "Muon_dsaMatch1idx": "DSAMuon",
        "Muon_dsaMatch2idx": "DSAMuon",
        "Muon_dsaMatch3idx": "DSAMuon",
        "Muon_dsaMatch4idx": "DSAMuon",
        "Muon_dsaMatch5idx": "DSAMuon",
        "DSAMuon_muonMatch1idx": "Muon",
        "DSAMuon_muonMatch2idx": "Muon",
        "DSAMuon_muonMatch3idx": "Muon",
        "DSAMuon_muonMatch4idx": "Muon",
        "DSAMuon_muonMatch5idx": "Muon",
    }
    nested_items = {
        **NanoAODSchema.nested_items,
        "Muon_dsaIdxG": [
            "Muon_dsaMatch1idxG",
            "Muon_dsaMatch2idxG",
            "Muon_dsaMatch3idxG",
            "Muon_dsaMatch4idxG",
            "Muon_dsaMatch5idxG",
        ],
        "DSAMuon_muonIdxG": [
            "DSAMuon_muonMatch1idxG",
            "DSAMuon_muonMatch2idxG",
            "DSAMuon_muonMatch3idxG",
            "DSAMuon_muonMatch4idxG",
            "DSAMuon_muonMatch5idxG",
        ],
    }

    @property
    def behavior(cls):
        """Behaviors necessary to implement this schema (dict)"""
        import awkward
        from coffea.nanoevents.methods import nanoaod, base, candidate
        
        @awkward.mixin_class(nanoaod.behavior)
        class DSAMuon(candidate.PtEtaPhiMCandidate, base.NanoCollection, base.Systematic):
            """LLPNanoAOD DSA muon object"""
 
            @property
            def matched_muons(self):
                return self._events().Muon._apply_global_index(self.muonIdxG)

        nanoaod._set_repr_name("DSAMuon")

        return nanoaod.behavior
