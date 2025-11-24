from typing import Tuple

LETTER_MAP = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
}

def clean_name(name: str) -> str:
    """Remove espaços e caracteres especiais, mantém apenas letras."""
    if not name:
        return ""
    return ''.join(c.upper() for c in name if c.isalpha())

def digit_sum(n: int) -> int:
    """Soma os dígitos de um inteiro."""
    return sum(int(d) for d in str(abs(int(n))))

def reduce_to_limit(n: int, limit: int = 22) -> int:
    """Reduz somando dígitos repetidamente até que o resultado seja <= limit."""
    r = digit_sum(n)
    while r > limit:
        r = digit_sum(r)
    return r

def calcula_energia_nome(full_name: str) -> Tuple[int, int]:
    """
    Calcula a energia do nome somando os valores das letras (A=1, B=2, ..., Z=8, etc).
    Remove espaços e caracteres especiais.
    Retorna (raw_sum, reduced_value) onde reduced_value <= 22.
    Ex.: "João Silva" -> "JOAOSILVA" -> 1+6+1+6+1+9+3+4+1 = 32 -> 3+2 = 5
    """
    clean = clean_name(full_name)
    if not clean:
        return 0, 0
    
    raw = sum(LETTER_MAP.get(c, 0) for c in clean)
    reduced = reduce_to_limit(raw, limit=22)
    return raw, reduced