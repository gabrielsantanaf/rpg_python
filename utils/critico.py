import random
import time
from typing import Optional, Tuple


def is_critico(chance: float, rng: Optional[random.Random] = None) -> bool:
    """
    Retorna True se ocorrer um crítico com a probabilidade `chance`.

    - `chance` deve estar entre 0.0 e 1.0.
    - `rng` pode ser um objeto `random.Random` para testar de forma determinística.
    """

    if not 0.0 <= chance <= 1.0:
        raise ValueError("chance deve estar entre 0.0 e 1.0")

    rng = rng or random
    return rng.random() <= chance


def _animacao_critico(speed: float = 0.05, length: int = 8) -> None:
    """
    Pequena animação estética. `speed` controla a velocidade entre frames.
    """

    efeitos = ["⚡", "✨", "💥", "🔥", "⚔️", "💫"]
    linha = ""

    for _ in range(length):
        linha += random.choice(efeitos)
        print(f"\r{linha}", end="", flush=True)
        time.sleep(speed)

    print()


def calcular_critico(
    dano_base: int,
    chance: float = 0.20,
    multiplicador: float = 1.8,
    mode: str = "multiply",
    rng: Optional[random.Random] = None,
    animacao: bool = True,
    anim_speed: float = 0.05,
    verbose: bool = True,
) -> Tuple[int, bool]:
    """
    Calcula o dano final considerando possibilidade de crítico.

    Parâmetros:
    - `dano_base`: dano antes de crit.
    - `chance`: probabilidade de acerto crítico (0.0 - 1.0). Padrão 0.20 (20%).
    - `multiplicador`: se `mode` == "multiply", multiplica o dano final por esse valor.
      se `mode` == "add", adiciona esse valor ao dano base (usa int).
    - `mode`: "multiply" ou "add". "multiply" é o comportamento padrão.
    - `rng`: objeto `random.Random` para testes determinísticos.
    - `animacao`: se True, mostra uma pequena animação em caso de crítico.
    - `anim_speed`: velocidade da animação (segundos por frame).
    - `verbose`: se True, exibe mensagens informativas no console.

    Retorna uma tupla `(dano_final, foi_critico)`.
    """

    if dano_base < 0:
        raise ValueError("dano_base deve ser >= 0")

    if mode not in ("multiply", "add"):
        raise ValueError("mode deve ser 'multiply' ou 'add'")

    crit = is_critico(chance, rng=rng)

    if not crit:
        if verbose:
            print(f"Dano: {dano_base} (não crítico)")
        return dano_base, False

    # crítico
    if animacao:
        _animacao_critico(speed=anim_speed)

    if mode == "multiply":
        dano_final = int(dano_base * multiplicador)
    else:  # add
        dano_final = dano_base + int(multiplicador)

    if verbose:
        print(f"\n🔥 ATAQUE CRÍTICO! 🔥")
        print(f"💥 Dano amplificado de {dano_base} → {dano_final}!")

    return dano_final, True


if __name__ == "__main__":
    # Demo rápido quando executado diretamente
    print("Demo: calcular_critico")
    for i in range(5):
        dano, foi = calcular_critico(10, chance=0.35, multiplicador=2.0, animacao=True)
        time.sleep(0.2)
