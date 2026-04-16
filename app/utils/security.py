from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hasher_mot_de_passe(mot_de_passe: str) -> str:
    # Limite à 72 bytes maximum (limite bcrypt)
    mot_de_passe_tronque = mot_de_passe[:72]
    return pwd_context.hash(mot_de_passe_tronque)


def verifier_mot_de_passe(mot_de_passe: str, hash: str) -> bool:
    mot_de_passe_tronque = mot_de_passe[:72]
    return pwd_context.verify(mot_de_passe_tronque, hash)
