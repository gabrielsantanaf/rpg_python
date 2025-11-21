import random
import time

def calcular_critico(dano_base):
    """
    Calcula se o ataque será crítico.
    Chance padrão: 20%
    Efeito: Multiplica o dano final (Opção B)
    """

    chance_critico = 1.0
    multiplicador = 1.8  # aumenta o dano final

    if random.random() <= chance_critico:
        _animacao_critico()
        dano_final = int(dano_base * multiplicador)
        print(f"\n🔥 **ATAQUE CRÍTICO!** 🔥")
        print(f"💥 Dano amplificado de {dano_base} → {dano_final}!")
        return dano_final

    return dano_base


def _animacao_critico():
    """
    Pequena animação estética só pra ficar estiloso.
    """

    efeitos = ["⚡", "✨", "💥", "🔥", "⚔️"]
    linha = ""

    for _ in range(8):
        linha += random.choice(efetos := efeitos)
        print(f"\r{linha}", end="")
        time.sleep(0.05)

    print()
