"""
Migración: agrega columnas de tokens a call_logs y crea token_usage_daily.
Ejecutar UNA sola vez sobre una base de datos existente.
"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import get_settings

def migrate():
    db_path = get_settings().db_path
    print(f"Migrando: {db_path}")
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    existing = {r[1] for r in cur.execute("PRAGMA table_info(call_logs)")}
    new_cols = {
        "tokens_input":  "INTEGER DEFAULT 0",
        "tokens_output": "INTEGER DEFAULT 0",
        "tokens_total":  "INTEGER DEFAULT 0",
        "cost_usd":      "REAL DEFAULT 0.0",
    }
    for col, defn in new_cols.items():
        if col not in existing:
            cur.execute(f"ALTER TABLE call_logs ADD COLUMN {col} {defn}")
            print(f"  + call_logs.{col}")
        else:
            print(f"  ~ call_logs.{col} ya existe")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS token_usage_daily (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            total_calls INTEGER DEFAULT 0,
            tokens_input INTEGER DEFAULT 0,
            tokens_output INTEGER DEFAULT 0,
            tokens_total INTEGER DEFAULT 0,
            cost_usd REAL DEFAULT 0.0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(date)
        )
    """)
    print("  + token_usage_daily OK")

    con.commit()
    con.close()
    print("Migración completada.")

if __name__ == "__main__":
    migrate()
