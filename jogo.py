"""
Módulo principal que orquestra o fluxo do jogo.
Gerencia o menu, combate, salvamento e carregamento.
"""

import random
from models.personagem import Personagem
from models.classes import Guerreiro, Mago, Arqueiro
from models.missão import Missao
from utils.repositorio import Repositorio
from utils.logger import Logger
from models.inventario import Item, Inventario



class Jogo:
    """
    Classe principal que gerencia o fluxo do jogo RPG.
    """
    
    # Lista de nomes de missões disponíveis
    NOMES_MISSOES = [
        "Encontro na Floresta",
        "Caverna Sombria",
        "Ruínas Antigas",
        "Torre do Mago",
        "Covil do Dragão",
        "Templo Perdido",
        "Floresta Proibida",
        "Montanha Gélida"
    ]
    
    def __init__(self):
        """Inicializa o jogo."""
        self.personagem = None
        self.repositorio = Repositorio()
        self.logger = Logger()
        self.logger.registrar("Jogo iniciado")
    
    def exibir_menu(self):
        """Exibe o menu principal do jogo."""
        print("\n" + "=" * 30)
        print("=== RPG OO ===")
        print("=" * 30)
        print("[1] Criar personagem")
        print("[2] Encarar missão")
        print("[3] Ver status")
        print("[4] Salvar")
        print("[5] Carregar")
        print("[0] Sair")
        print("=" * 30)
    
    def criar_personagem(self):
        """
        Cria um novo personagem com nome e classe escolhidos pelo jogador.
        """
        print("\n=== Criar Personagem ===")
        nome = input("Nome do personagem: ").strip()
        
        if not nome:
            print("Nome inválido!")
            return
        
        print("\nEscolha a classe:")
        print("[1] Guerreiro (Alto HP, Alta Defesa, Baixa Mana)")
        print("[2] Mago (Baixo HP, Baixa Defesa, Alta Mana)")
        print("[3] Arqueiro (HP Médio, Equilibrado)")
        
        escolha = input("> ").strip()
        
        if escolha == "1":
            self.personagem = Guerreiro(nome)
        elif escolha == "2":
            self.personagem = Mago(nome)
        elif escolha == "3":
            self.personagem = Arqueiro(nome)
        else:
            print("Opção inválida! Criando Guerreiro por padrão.")
            self.personagem = Guerreiro(nome)
        
        print(f"\nPersonagem criado: {self.personagem.nome} ({self.personagem.classe})")
        print(f"HP: {self.personagem.hp}/{self.personagem.hp_maximo}")
        print(f"Mana: {self.personagem.mana}/{self.personagem.mana_maxima}")
        print(f"Nível: {self.personagem.nivel}")
        
        self.logger.registrar(f"Personagem criado: {self.personagem.nome} ({self.personagem.classe})")
    
    def encarar_missao(self):
        """
        Inicia uma missão aleatória para o personagem.
        """
        if not self.personagem:
            print("\nVocê precisa criar um personagem primeiro!")
            return
        
        if not self.personagem.esta_vivo():
            print("\nSeu personagem está sem HP! Use itens para curar ou recrie o personagem.")
            return
        
        # Escolhe dificuldade baseada no nível
        if self.personagem.nivel <= 2:
            dificuldade = "fácil"
        elif self.personagem.nivel <= 5:
            dificuldade = random.choice(["fácil", "médio"])
        else:
            dificuldade = random.choice(["médio", "difícil"])
        
        nome_missao = random.choice(self.NOMES_MISSOES)
        missao = Missao(nome_missao, dificuldade)
        
        resultado = missao.executar_combate(self.personagem, self.logger)
        
        if resultado["vitoria"]:
            print(f"\nXP atual: {self.personagem.xp}/{self.personagem.xp_proximo_nivel}")
            print(f"Próximo nível em: {self.personagem.xp_proximo_nivel - self.personagem.xp} XP")
    
    def ver_status(self):
        """
        Exibe o status completo do personagem.
        """
        if not self.personagem:
            print("\nVocê precisa criar um personagem primeiro!")
            return
        
        print("\n" + "=" * 40)
        print(f"=== Status de {self.personagem.nome} ===")
        print("=" * 40)
        print(f"Classe: {self.personagem.classe}")
        print(f"Nível: {self.personagem.nivel}")
        print(f"XP: {self.personagem.xp}/{self.personagem.xp_proximo_nivel}")
        print(f"HP: {self.personagem.hp}/{self.personagem.hp_maximo}")
        print(f"Barra de Vida: [{self.personagem.get_barra_vida()}]")
        print(f"Mana: {self.personagem.mana}/{self.personagem.mana_maxima}")
        print(f"Dano Base: {self.personagem.dano_base}")
        print(f"Defesa: {self.personagem.defesa}")
        print(f"\nInventário ({len(self.personagem.inventario)} itens):")
        if self.personagem.inventario:
            for item in self.personagem.inventario:
                print(f"  - {item}")
        else:
            print("  (vazio)")
        print("=" * 40)
    
    def salvar(self):
        """
        Salva o progresso do jogo.
        """
        if not self.personagem:
            print("\nVocê precisa criar um personagem primeiro!")
            return
        
        if self.repositorio.salvar(self.personagem):
            print("\nJogo salvo com sucesso!")
            self.logger.registrar(f"Jogo salvo: {self.personagem.nome}")
        else:
            print("\nErro ao salvar o jogo!")
    
    def carregar(self):
        """
        Carrega o progresso do jogo salvo.
        """
        if not self.repositorio.existe_save():
            print("\nNenhum save encontrado!")
            return
        
        personagem_carregado = self.repositorio.carregar()
        
        if personagem_carregado:
            self.personagem = personagem_carregado
            print(f"\nJogo carregado com sucesso!")
            print(f"Personagem: {self.personagem.nome} ({self.personagem.classe})")
            print(f"Nível: {self.personagem.nivel}")
            self.logger.registrar(f"Jogo carregado: {self.personagem.nome}")
        else:
            print("\nErro ao carregar o jogo!")
    
    def executar(self):
        """
        Loop principal do jogo.
        """
        print("\nBem-vindo ao RPG OO!")
        
        while True:
            self.exibir_menu()
            escolha = input("\n> ").strip()
            
            if escolha == "1":
                self.criar_personagem()
            elif escolha == "2":
                self.encarar_missao()
            elif escolha == "3":
                self.ver_status()
            elif escolha == "4":
                self.salvar()
            elif escolha == "5":
                self.carregar()
            elif escolha == "0":
                print("\nObrigado por jogar! Até logo!")
                self.logger.registrar("Jogo encerrado")
                break
            else:
                print("\nOpção inválida! Tente novamente.")

