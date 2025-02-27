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
        "DSAMuon_muonMatch2idx": "Muon",
        "DSAMuon_muonMatch3idx": "Muon",
        "DSAMuon_muonMatch4idx": "Muon",
        "DSAMuon_muonMatch5idx": "Muon",
    }
    nested_items = {
        **NanoAODSchema.nested_items,
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
            def matched_muon(self):
                return self._events().Muon._apply_global_index(self.muonIdxG)

        nanoaod._set_repr_name("DSAMuon")

        return nanoaod.behavior
