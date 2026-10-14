from pysat.card import CardEnc, EncType

def encode_alo(lits, top_id=0):
    if not lits:
        return [], 0
    return [lits], 0

def encode_amo(lits, top_id):
    """At-Most-One using PySAT Modular Totalizer"""
    formula = CardEnc.atmost(lits, bound=1, top_id=top_id, encoding=EncType.mtotalizer)
    return formula.clauses, formula.nv - top_id

def encode_exactly_one(lits, top_id):
    """Exactly-One using PySAT Modular Totalizer"""
    formula = CardEnc.equals(lits, bound=1, top_id=top_id, encoding=EncType.mtotalizer)
    return formula.clauses, formula.nv - top_id
