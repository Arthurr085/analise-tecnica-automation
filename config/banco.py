import os
import oracledb
from dotenv import load_dotenv

load_dotenv()


def get_connection() -> oracledb.Connection:
    """Retorna uma conexão Oracle usando as variáveis do .env."""
    return oracledb.connect(
        user=os.getenv("DB_USER", ""),
        password=os.getenv("DB_PASSWORD", ""),
        dsn=f"{os.getenv('DB_HOST', '')}:{os.getenv('DB_PORT', '1521')}/{os.getenv('DB_SERVICE_NAME', '')}",
    )
