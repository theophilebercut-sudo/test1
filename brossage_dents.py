import sqlite3
from datetime import datetime

DB_PATH = "brossage_dents.db"


def init_db(db_path: str = DB_PATH) -> None:
    """Crée la base et la table si elles n'existent pas."""
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS suivi_brossage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_reponse TEXT NOT NULL,
                brossages INTEGER NOT NULL CHECK (brossages IN (0, 1, 2))
            )
            """
        )
        conn.commit()


def demander_brossage() -> int:
    """Demande à l'utilisateur une valeur valide (0, 1 ou 2)."""
    while True:
        reponse = input(
            "Combien de fois vous êtes-vous brossé les dents aujourd'hui ? (0, 1 ou 2) : "
        ).strip()

        if reponse in {"0", "1", "2"}:
            return int(reponse)

        print("Entrée invalide. Merci de saisir uniquement 0, 1 ou 2.")


def enregistrer_reponse(brossages: int, db_path: str = DB_PATH) -> None:
    """Enregistre la réponse de l'utilisateur dans la base SQLite."""
    maintenant = datetime.now().isoformat(timespec="seconds")
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT INTO suivi_brossage (date_reponse, brossages) VALUES (?, ?)",
            (maintenant, brossages),
        )
        conn.commit()


def main() -> None:
    init_db()
    brossages = demander_brossage()
    enregistrer_reponse(brossages)
    print("Merci ! Votre réponse a bien été enregistrée dans la base de données.")


if __name__ == "__main__":
    main()
