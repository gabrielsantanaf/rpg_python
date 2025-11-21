"""
Módulo que define a classe Missao e o sistema de combate detalhado.
"""

import random
from models.inimigo import Inimigo, Goblin, Lobo, Orc, Chefao
from models.critical import calcular_critico  # Importa a função de cálculo de crítico


class Missao:
    """
    Classe que representa uma missão do jogo.
    Contém um inimigo, recompensas e gerencia o combate detalhado.
    """

    # Dicionário de tipos de inimigos disponíveis
    TIPOS_INIMIGOS = {
        "fácil": [Goblin, Lobo],
        "médio": [Lobo, Orc],
        "difícil": [Orc, Chefao]
    }

    # Dicionário de itens possíveis como recompensa
    ITENS_POSSIVEIS = ["poção", "poção de mana", "elixir", "cristal"]

    def __init__(self, nome, dificuldade="médio"):
        """
        Inicializa uma missão.
        """
        self.nome = nome
        self.dificuldade = dificuldade
        self.inimigo = self._gerar_inimigo()
        self.xp_recompensa = self.inimigo.xp_recompensa
        self.itens_recompensa = self._gerar_recompensas()

    def _gerar_inimigo(self):
        tipos = self.TIPOS_INIMIGOS.get(self.dificuldade, self.TIPOS_INIMIGOS["médio"])
        classe_inimigo = random.choice(tipos)
        return classe_inimigo()

    def _gerar_recompensas(self):
        itens = []
        num_itens = random.randint(1, 2)
        for _ in range(num_itens):
            itens.append(random.choice(self.ITENS_POSSIVEIS))
        return itens

    def executar_combate(self, personagem, logger=None):
        print(f"\n=== Missão: {self.nome} ===")
        print(f"Você encontrou um {self.inimigo.nome}!")
        print(f"HP do inimigo: {self.inimigo.hp}")

        if logger:
            logger.registrar(f"Iniciou missão: {self.nome} contra {self.inimigo.nome}")

        turno = 1
        hp_inicial_personagem = personagem.hp

        while personagem.esta_vivo() and self.inimigo.esta_vivo():
            print(f"\n--- Turno {turno} ---")

            # --- TURNO DO JOGADOR ---
            acao = self._escolher_acao(personagem)

            if acao == "atacar":
                dano = personagem.atacar()
                dano = calcular_critico(dano)  # ← CRÍTICO APLICADO AQUI
                dano_aplicado = self.inimigo.receber_dano_com_defesa(dano)
                print(f"{personagem.nome} causa {dano_aplicado} de dano em {self.inimigo.nome}!")
                print(f"{self.inimigo.nome} agora tem {self.inimigo.hp} HP.")

                if logger:
                    logger.registrar(f"Turno {turno}: {personagem.nome} causou {dano_aplicado} de dano")

            elif acao == "habilidade":
                dano = personagem.habilidade_especial()
                if dano > 0:
                    dano = calcular_critico(dano)  # Crítico na habilidade também
                    print(f"{personagem.nome} usa habilidade especial!")
                    dano_aplicado = self.inimigo.receber_dano_com_defesa(dano)
                    print(f"{personagem.nome} causa {dano_aplicado} de dano!")
                    print(f"{self.inimigo.nome} agora tem {self.inimigo.hp} HP.")
                else:
                    print("Mana insuficiente! Atacando normalmente.")
                    dano = personagem.atacar()
                    dano = calcular_critico(dano)
                    dano_aplicado = self.inimigo.receber_dano_com_defesa(dano)
                    print(f"{personagem.nome} causa {dano_aplicado} de dano!")

            elif acao == "item":
                if personagem.inventario:
                    item = personagem.inventario[0]
                    if personagem.usar_item(item):
                        print(f"{personagem.nome} usou {item}!")
                        print(f"HP atual: {personagem.hp}")
                    else:
                        print("Não foi possível usar o item.")
                else:
                    print("Sem itens! Atacando normalmente.")
                    dano = personagem.atacar()
                    dano = calcular_critico(dano)
                    dano_aplicado = self.inimigo.receber_dano_com_defesa(dano)
                    print(f"{personagem.nome} causa {dano_aplicado} de dano!")

            if not self.inimigo.esta_vivo():
                break

            # Regeneração do Chefão
            if hasattr(self.inimigo, "regenerar"):
                self.inimigo.regenerar()

            # --- TURNO DO INIMIGO ---
            dano_enemy = self.inimigo.atacar()
            dano_aplicado = personagem.receber_dano(max(1, dano_enemy - personagem.defesa))
            print(f"{self.inimigo.nome} causa {dano_aplicado} de dano em {personagem.nome}!")
            print(f"{personagem.nome} agora tem {personagem.hp} HP.")

            turno += 1

        # --- RESULTADO FINAL ---
        print(f"\n=== Resultado da Missão ===")

        if personagem.esta_vivo():
            print(f"{personagem.nome} venceu o combate!")
            print(f"XP ganho: {self.xp_recompensa}")

            subiu_nivel = personagem.ganhar_xp(self.xp_recompensa)
            if subiu_nivel:
                print(f"\n🎉 {personagem.nome} subiu para o nível {personagem.nivel}!")

            if self.itens_recompensa:
                print(f"Itens obtidos: {', '.join(self.itens_recompensa)}")
                for item in self.itens_recompensa:
                    personagem.adicionar_item(item)

            return {
                "vitoria": True,
                "xp": self.xp_recompensa,
                "itens": self.itens_recompensa,
                "subiu_nivel": subiu_nivel
            }

        else:
            print("Você foi derrotado!")
            personagem.hp = hp_inicial_personagem

            return {
                "vitoria": False,
                "xp": 0,
                "itens": [],
                "subiu_nivel": False
            }

    def _escolher_acao(self, personagem):
        while True:
            print("\nEscolha sua ação:")
            print("[1] Atacar")
            print(f"[2] Habilidade Especial (Mana: {personagem.mana}/{personagem.mana_maxima})")
            if personagem.inventario:
                print(f"[3] Usar Item ({', '.join(personagem.inventario)})")

            escolha = input("> ").strip()

            if escolha == "1":
                return "atacar"
            elif escolha == "2":
                return "habilidade"
            elif escolha == "3" and personagem.inventario:
                return "item"
            else:
                print("Opção inválida!")
