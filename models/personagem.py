"""
Módulo que define a classe Personagem e suas funcionalidades.
"""

from models.base import Atributos
import random


class Personagem(Atributos):
    """
    Classe que representa o personagem do jogador.
    Herda de Atributos e adiciona funcionalidades específicas do jogador.
    """

    def __init__(self, nome, classe, hp=100, nivel=1, xp=0):
        super().__init__(nome, hp, hp)
        self.classe = classe
        self.sub_classe = None
        self.nivel = nivel
        self.xp = xp
        self.xp_proximo_nivel = 100

        self.inventario = []
        self.mana = 50
        self.mana_maxima = 50
        self.dano_base = 10
        self.defesa = 5

        self.crit_chance = 0.05
        self.stun_chance = 0.0
        self.dot_sangramento = 0.0
        self.buff_dano = 1.0
        self.chance_queimadura = 0.0
        self.cura_base = 0

    def subclasse(self):
        if self.nivel < 4:
            print(f"Seu nível atual é {self.nivel}. É necessário ter nível 4 ou maior para escolher uma sub-classe.")
            return

        if self.sub_classe is not None:
            print(f"Você já escolheu a sub-classe: {self.sub_classe}")
            return

        print("\n==== Escolha de Sub-Classe ====\n")
        if self.classe == "Guerreiro":
            print("1 - Berserker")
            print("2 - Paladino")
            escolha = input("Escolha: ")
            if escolha == "1":
                self.sub_classe = "Berserker"
                self.dano_base += 10
                self.hp_maximo -= 20
                self.crit_chance += 0.10
                print("Agora você é um Berserker")
            elif escolha == "2":
                self.sub_classe = "Paladino"
                self.hp_maximo += 30
                self.defesa += 5
                self.dano_base -= 5
                print("Agora você é um Paladino")
            else:
                print("Escolha inválida.")
            return

        elif self.classe == "Arqueiro":
            print("1 - Caçador")
            print("2 - Patrulheiro")
            escolha = input("Escolha: ")
            if escolha == "1":
                self.sub_classe = "Caçador"
                self.dot_sangramento = 0.30
                self.stun_chance = 0.15
                print("Agora você é um Caçador")
            elif escolha == "2":
                self.sub_classe = "Patrulheiro"
                self.buff_dano = 1.20
                self.crit_chance += 0.10
                print("Agora você é um Patrulheiro")
            else:
                print("Escolha inválida.")
            return

        elif self.classe == "Mago":
            print("1 - Piromante")
            print("2 - Clérigo")
            escolha = input("Escolha: ")
            if escolha == "1":
                self.sub_classe = "Piromante"
                self.dano_base += 8
                self.chance_queimadura = 0.30
                print("Agora você é um Piromante")
            elif escolha == "2":
                self.sub_classe = "Clerigo"
                self.mana_maxima += 20
                self.cura_base = 20
                print("Agora você é um Clerigo")
            else:
                print("Escolha inválida.")
            return
        else:
            print("Classe inválida.")

    def atacar(self, alvo=None):
        """Realiza um ataque. `alvo` é opcional para permitir chamadas de smoke-tests
        que apenas verificam o cálculo de dano sem um alvo concreto.
        """

        dano = int(self.dano_base * random.uniform(0.8, 1.2))
        dano = int(dano * self.buff_dano)

        
        if random.random() < self.crit_chance:
            dano = int(dano * 1.8)
            print(f"**CRÍTICO**")

        # Redução pela defesa do alvo (se houver)
        defesa_alvo = getattr(alvo, "defesa", 0) if alvo is not None else 0
        dano_final = max(1, dano - defesa_alvo)
        if alvo is not None:
            print(f"{self.nome} causou {dano_final} de dano em {alvo.nome}!")
        else:
            print(f"{self.nome} causou {dano_final} de dano!")

        #chance de stun
        if alvo is not None and self.sub_classe == "Caçador":
            roll = random.random()
            if roll < self.stun_chance:
                setattr(alvo, "stunned_turns", 1)
                print(f"{alvo.nome} foi ATORDOADO por 1 rodada! (roll={roll:.2f})")

        #chance de sangramento
        if alvo is not None and self.sub_classe == "Caçador" and random.random() < self.dot_sangramento:
            setattr(alvo, "sangramento_turns", 2)
            print(f"{alvo.nome} está SANGRANDO!")

        #chance de queimadura
        if alvo is not None and self.sub_classe == "Piromante" and random.random() < self.chance_queimadura:
            setattr(alvo, "queimadura_turns", 2)
            print(f"{alvo.nome} está QUEIMANDO!")

        return dano_final

    def habilidade_especial(self):
        if self.mana >= 20:
            self.mana -= 20
            dano = int(self.dano_base * random.uniform(1.3, 1.7) * self.buff_dano)
            if random.random() < self.crit_chance:
                dano = int(dano * 2)
                print("**Habilidade especial CRÍTICA!**")
            return max(1, dano)
        print("Mana insuficiente para habilidade especial.")
        return 0

    def usar_item(self, item):
        # Suporta tanto string quanto objeto com atributo nome
        nome_item = item.nome if hasattr(item, "nome") else str(item)
        for inv_item in list(self.inventario):
            inv_nome = inv_item.nome if hasattr(inv_item, "nome") else str(inv_item)
            if inv_nome == nome_item:
                if nome_item == "poção":
                    self.curar(30)
                    self.inventario.remove(inv_item)
                    return True
                elif nome_item == "poção de mana":
                    self.mana = min(self.mana + 25, self.mana_maxima)
                    self.inventario.remove(inv_item)
                    return True
        return False

    def adicionar_item(self, item):
        self.inventario.append(item)

    def ganhar_xp(self, quantidade):
        self.xp += quantidade
        subiu_nivel = False
        while self.xp >= self.xp_proximo_nivel:
            self.xp -= self.xp_proximo_nivel
            self.nivel += 1
            self.xp_proximo_nivel = int(self.xp_proximo_nivel * 1.5)
            self.hp_maximo += 20
            self.hp = self.hp_maximo
            self.dano_base += 2
            self.defesa += 1
            subiu_nivel = True
            # Exibe opção de subclasse ao atingir nível 4
            if self.nivel == 4 and self.sub_classe is None:
                print("\nVocê atingiu o nível 4! Agora pode escolher uma sub-classe:")
                self.subclasse()
        return subiu_nivel

    def to_dict(self):
        return {
            "nome": self.nome,
            "classe": self.classe,
            "sub_classe": self.sub_classe,
            "hp": self.hp,
            "hp_maximo": self.hp_maximo,
            "nivel": self.nivel,
            "xp": self.xp,
            "xp_proximo_nivel": self.xp_proximo_nivel,
            "inventario": [it.nome if hasattr(it, "nome") else str(it) for it in self.inventario],
            "mana": self.mana,
            "mana_maxima": self.mana_maxima,
            "dano_base": self.dano_base,
            "defesa": self.defesa,
            "crit_chance": self.crit_chance,
            "stun_chance": self.stun_chance,
            "dot_sangramento": self.dot_sangramento,
            "buff_dano": self.buff_dano,
            "chance_queimadura": self.chance_queimadura,
            "cura_base": self.cura_base,
        }

    @classmethod
    def from_dict(cls, dados):
        personagem = cls(
            dados["nome"],
            dados["classe"],
            dados.get("hp", 100),
            dados.get("nivel", 1),
            dados.get("xp", 0)
        )
        personagem.sub_classe = dados.get("sub_classe")
        personagem.hp_maximo = dados.get("hp_maximo", personagem.hp)
        personagem.xp_proximo_nivel = dados.get("xp_proximo_nivel", 100)
        personagem.inventario = dados.get("inventario", [])
        personagem.mana = dados.get("mana", 50)
        personagem.mana_maxima = dados.get("mana_maxima", 50)
        personagem.dano_base = dados.get("dano_base", 10)
        personagem.defesa = dados.get("defesa", 5)
        personagem.crit_chance = dados.get("crit_chance", 0.05)
        personagem.stun_chance = dados.get("stun_chance", 0.0)
        personagem.dot_sangramento = dados.get("dot_sangramento", 0.0)
        personagem.buff_dano = dados.get("buff_dano", 1.0)
        personagem.chance_queimadura = dados.get("chance_queimadura", 0.0)
        personagem.cura_base = dados.get("cura_base", 0)
        return personagem