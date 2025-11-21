"""
Módulo que define a classe Missao e o sistema de combate detalhado.
"""

import random
from models.inimigo import Inimigo, Goblin, Lobo, Orc, Chefao


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
        
        Args:
            nome (str): Nome da missão
            dificuldade (str): Nível de dificuldade ("fácil", "médio", "difícil")
        """
        self.nome = nome
        self.dificuldade = dificuldade
        self.inimigo = self._gerar_inimigo()
        self.xp_recompensa = self.inimigo.xp_recompensa
        self.itens_recompensa = self._gerar_recompensas()
    
    def _gerar_inimigo(self):
        """
        Gera um inimigo aleatório baseado na dificuldade.
        
        Returns:
            Inimigo: Instância de um inimigo
        """
        tipos = self.TIPOS_INIMIGOS.get(self.dificuldade, self.TIPOS_INIMIGOS["médio"])
        classe_inimigo = random.choice(tipos)
        return classe_inimigo()
    
    def _gerar_recompensas(self):
        """
        Gera itens de recompensa aleatórios.
        
        Returns:
            list: Lista de itens obtidos
        """
        itens = []
        # Chance de obter 1-2 itens
        num_itens = random.randint(1, 2)
        for _ in range(num_itens):
            item = random.choice(self.ITENS_POSSIVEIS)
            itens.append(item)
        return itens
    
    def executar_combate(self, personagem, logger=None):
        """
        Executa o combate detalhado entre o personagem e o inimigo.
        
        Args:
            personagem: Instância do personagem do jogador
            logger: Instância do logger para registrar eventos (opcional)
            
        Returns:
            dict: Resultado do combate com informações sobre vitória/derrota
        """
        print(f"\n=== Missão: {self.nome} ===")
        print(f"Você encontrou um {self.inimigo.nome}!")
        print(f"HP do inimigo: {self.inimigo.hp}")
        
        if logger:
            logger.registrar(f"Iniciou missão: {self.nome} contra {self.inimigo.nome}")
        
        turno = 1
        hp_inicial_personagem = personagem.hp
        
        while personagem.esta_vivo() and self.inimigo.esta_vivo():
            print(f"\n--- Turno {turno} ---")
            
            # Turno do jogador
            acao = self._escolher_acao(personagem)
            
            if acao == "atacar":
                dano = personagem.atacar()
                dano_aplicado = self.inimigo.receber_dano_com_defesa(dano)
                print(f"{personagem.nome} causa {dano_aplicado} de dano em {self.inimigo.nome}!")
                print(f"{self.inimigo.nome} agora tem {self.inimigo.hp} HP.")
                
                if logger:
                    logger.registrar(f"Turno {turno}: {personagem.nome} causou {dano_aplicado} de dano")
            
            elif acao == "habilidade":
                dano = personagem.habilidade_especial()
                if dano > 0:
                    print(f"{personagem.nome} usa habilidade especial!")
                    dano_aplicado = self.inimigo.receber_dano_com_defesa(dano)
                    print(f"{personagem.nome} causa {dano_aplicado} de dano em {self.inimigo.nome}!")
                    print(f"{self.inimigo.nome} agora tem {self.inimigo.hp} HP.")
                    
                    if logger:
                        logger.registrar(f"Turno {turno}: {personagem.nome} usou habilidade especial causando {dano_aplicado} de dano")
                else:
                    print(f"{personagem.nome} não tem mana suficiente para usar habilidade especial!")
                    # Se não tem mana, ataca normalmente
                    dano = personagem.atacar()
                    dano_aplicado = self.inimigo.receber_dano_com_defesa(dano)
                    print(f"{personagem.nome} causa {dano_aplicado} de dano em {self.inimigo.nome}!")
                    print(f"{self.inimigo.nome} agora tem {self.inimigo.hp} HP.")
            
            elif acao == "item":
                if personagem.inventario:
                    # Lista itens e permite escolher qual usar
                    while True:
                        print("\nItens disponíveis:")
                        for i, it in enumerate(personagem.inventario, start=1):
                            print(f"[{i}] {it}")
                        escolha_item = input("Digite o número do item que deseja usar (0 para cancelar): ").strip()
                        if not escolha_item.isdigit():
                            print("Entrada inválida! Digite um número.")
                            continue
                        escolha_num = int(escolha_item)
                        if escolha_num == 0:
                            print("Ação de item cancelada. Realizando ataque normal.")
                            dano = personagem.atacar()
                            dano_aplicado = self.inimigo.receber_dano_com_defesa(dano)
                            print(f"{personagem.nome} causa {dano_aplicado} de dano em {self.inimigo.nome}!")
                            print(f"{self.inimigo.nome} agora tem {self.inimigo.hp} HP.")
                            break
                        if escolha_num < 1 or escolha_num > len(personagem.inventario):
                            print("Índice inválido! Tente novamente.")
                            continue
                        item = personagem.inventario[escolha_num - 1]
                        if personagem.usar_item(item):
                            print(f"{personagem.nome} usou {item}!")
                            print(f"{personagem.nome} agora tem {personagem.hp} HP.")
                        else:
                            print(f"Não foi possível usar {item}.")
                        break
                else:
                    print(f"{personagem.nome} não tem itens no inventário!")
                    # Se não tem itens, ataca normalmente
                    dano = personagem.atacar()
                    dano_aplicado = self.inimigo.receber_dano_com_defesa(dano)
                    print(f"{personagem.nome} causa {dano_aplicado} de dano em {self.inimigo.nome}!")
                    print(f"{self.inimigo.nome} agora tem {self.inimigo.hp} HP.")
            
            # Verifica se o inimigo foi derrotado
            if not self.inimigo.esta_vivo():
                break
            
            # Regeneração do chefão (se aplicável)
            if hasattr(self.inimigo, 'regenerar'):
                self.inimigo.regenerar()
            
            # Turno do inimigo
            dano_inimigo = self.inimigo.atacar()
            dano_aplicado = personagem.receber_dano(max(1, dano_inimigo - personagem.defesa))
            print(f"{self.inimigo.nome} causa {dano_aplicado} de dano em {personagem.nome}!")
            print(f"{personagem.nome} agora tem {personagem.hp} HP.")
            
            if logger:
                logger.registrar(f"Turno {turno}: {self.inimigo.nome} causou {dano_aplicado} de dano")
            
            turno += 1
        
        # Resultado final
        print(f"\n=== Resultado da Missão ===")
        
        if personagem.esta_vivo():
            print(f"{personagem.nome} venceu o combate!")
            print(f"XP ganho: {self.xp_recompensa}")
            
            subiu_nivel = personagem.ganhar_xp(self.xp_recompensa)
            if subiu_nivel:
                print(f"\n🎉 {personagem.nome} subiu para o nível {personagem.nivel}!")
                print(f"HP máximo aumentou para {personagem.hp_maximo}!")
            
            if self.itens_recompensa:
                print(f"Itens obtidos: {', '.join(self.itens_recompensa)}")
                for item in self.itens_recompensa:
                    personagem.adicionar_item(item)
            
            if logger:
                logger.registrar(f"Missão concluída: {personagem.nome} venceu {self.inimigo.nome}")
                logger.registrar(f"XP ganho: {self.xp_recompensa}, Itens: {', '.join(self.itens_recompensa)}")
            
            return {
                "vitoria": True,
                "xp": self.xp_recompensa,
                "itens": self.itens_recompensa,
                "subiu_nivel": subiu_nivel
            }
        else:
            print(f"{personagem.nome} foi derrotado!")
            print(f"Você perdeu a missão.")
            
            # Restaura HP inicial em caso de derrota (opcional - pode remover)
            personagem.hp = hp_inicial_personagem
            
            if logger:
                logger.registrar(f"Missão falhou: {personagem.nome} foi derrotado por {self.inimigo.nome}")
            
            return {
                "vitoria": False,
                "xp": 0,
                "itens": [],
                "subiu_nivel": False
            }
    
    def _escolher_acao(self, personagem):
        """
        Permite ao jogador escolher uma ação durante o combate.
        
        Args:
            personagem: Instância do personagem
            
        Returns:
            str: Ação escolhida ("atacar", "habilidade", "item")
        """
        while True:
            print(f"\nEscolha sua ação:")
            print(f"[1] Atacar")
            print(f"[2] Habilidade Especial (Mana: {personagem.mana}/{personagem.mana_maxima})")
            if personagem.inventario:
                inventario_str = ', '.join(it.nome if hasattr(it, 'nome') else str(it) for it in personagem.inventario)
                print(f"[3] Usar Item (Inventário: {inventario_str})")
            
            escolha = input("> ").strip()
            
            if escolha == "1":
                return "atacar"
            elif escolha == "2":
                return "habilidade"
            elif escolha == "3" and personagem.inventario:
                return "item"
            else:
                print("Opção inválida! Tente novamente.")

