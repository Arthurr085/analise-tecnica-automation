"""Utilitários para manipulação de arquivos e pastas."""

import os


def garantir_pastas(pastas: list[str]) -> None:
    """Cria as pastas necessárias caso não existam."""
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)
