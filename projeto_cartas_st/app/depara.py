import json
from pathlib import Path
from typing import Any, Dict, Optional

DATA_FILE = Path(__file__).parents[1] / "data" / "depara_cartas.json"

def load_depara() -> list[Dict[str, Any]]:
    """Carrega o JSON de mapeamento (retorna lista vazia se não existir)."""
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

def _digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(int(n))))

def normalize_number(n: int) -> Optional[int]:
    """
    Normaliza número:
    - trata 0 como 1 (O Louco).
    - reduz somando dígitos repetidamente até obter <= 21.
    Retorna None se entrada inválida.
    """
    try:
        n = int(n)
    except Exception:
        return None
    if n == 0:
        return 1
    while n > 21:
        n = _digit_sum(n)
    return n

def get_arcano_by_number(n: int) -> Dict[str, Any]:
    """
    Retorna o item do depara_cartas.json correspondente ao número normalizado.
    Ex.: se n == 0 -> buscar número 1; se n > 21 -> reduz para <=21 antes de buscar.
    Retorna {} se não encontrar.
    """
    num = normalize_number(n)
    if num is None:
        return {}
    data = load_depara()
    for item in data:
        try:
            if int(item.get("numero")) == num:
                return item
        except Exception:
            continue
    return {}