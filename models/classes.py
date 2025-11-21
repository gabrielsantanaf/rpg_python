"""
Módulo que define as classes de personagem (Guerreiro, Mago, etc.)
com habilidades especiais únicas.
"""

from models.personagem import Personagem


class Guerreiro(Personagem):
    """
    Classe Guerreiro: especializada em combate corpo a corpo.
    Possui mais HP e defesa, mas menos mana.
    """
    
    def __init__(self, nome):
        """
        Inicializa um Guerreiro.
        
        Args:
            nome (str): Nome do guerreiro
        """
        super().__init__(nome, "Guerreiro", hp=150, nivel=1, xp=0)
        self.mana = 30
        self.mana_maxima = 30
        self.dano_base = 12
        self.defesa = 8
    
    def habilidade_especial(self):
        """
        Ataque devastador: causa muito dano, mas consome mana.
        
        Returns:
            int: Dano causado pela habilidade especial
        """
        if self.mana >= 15:
            import random
            from utils import calcular_critico

            self.mana -= 15
            # Ataque devastador causa 150% a 200% do dano base
            dano = int(self.dano_base * random.uniform(1.5, 2.0))

            # Aplicar crítico com chance um pouco menor para ataques pesados
            dano_final, _ = calcular_critico(dano, chance=0.15, multiplicador=1.8, animacao=False, verbose=False)
            return max(1, dano_final)
        return 0
    
    def atacar(self):
        """
        Sobrescreve o método atacar para causar mais dano.
        
        Returns:
            int: Dano causado pelo ataque
        """
        import random
        from utils import calcular_critico

        # Guerreiros causam mais dano físico
        dano = int(self.dano_base * random.uniform(0.9, 1.3))

        # Chance de crítico ligeiramente reduzida para ataques físicos
        dano_final, _ = calcular_critico(dano, chance=0.18, multiplicador=1.9, animacao=False, verbose=False)
        return max(1, dano_final)


class Mago(Personagem):
    """
    Classe Mago: especializada em magia e ataques à distância.
    Possui menos HP, mas mais mana e dano mágico.
    """
    
    def __init__(self, nome):
        """
        Inicializa um Mago.
        
        Args:
            nome (str): Nome do mago
        """
        super().__init__(nome, "Mago", hp=80, nivel=1, xp=0)
        self.mana = 100
        self.mana_maxima = 100
        self.dano_base = 8
        self.defesa = 3
    
    def habilidade_especial(self):
        """
        Bola de fogo: causa dano mágico significativo.
        
        Returns:
            int: Dano causado pela habilidade especial
        """
        if self.mana >= 20:
            import random
            from utils import calcular_critico

            self.mana -= 20
            # Bola de fogo causa 200% a 250% do dano base
            dano = int(self.dano_base * random.uniform(2.0, 2.5))

            # Magia tem a mesma chance padrão de crítico
            dano_final, _ = calcular_critico(dano, chance=0.20, multiplicador=2.0, animacao=False, verbose=False)
            return max(1, dano_final)
        return 0
    
    def atacar(self):
        """
        Sobrescreve o método atacar para usar magia básica.
        
        Returns:
            int: Dano causado pelo ataque
        """
        import random
        from utils import calcular_critico

        # Magos causam dano mágico consistente
        dano = int(self.dano_base * random.uniform(0.85, 1.15))

        dano_final, _ = calcular_critico(dano, chance=0.22, multiplicador=1.75, animacao=False, verbose=False)
        return max(1, dano_final)


class Arqueiro(Personagem):
    """
    Classe Arqueiro: especializada em ataques à distância.
    Possui equilíbrio entre HP, mana e dano.
    """
    
    def __init__(self, nome):
        """
        Inicializa um Arqueiro.
        
        Args:
            nome (str): Nome do arqueiro
        """
        super().__init__(nome, "Arqueiro", hp=100, nivel=1, xp=0)
        self.mana = 60
        self.mana_maxima = 60
        self.dano_base = 11
        self.defesa = 5
    
    def habilidade_especial(self):
        """
        Chuva de flechas: ataque múltiplo com chance de crítico.
        
        Returns:
            int: Dano causado pela habilidade especial
        """
        if self.mana >= 18:
            import random
            from utils import calcular_critico

            self.mana -= 18
            # Chuva de flechas causa 140% a 180% do dano base
            dano = int(self.dano_base * random.uniform(1.4, 1.8))

            # Usa calcular_critico com chance 30% e multiplicador 1.5
            dano_final, _ = calcular_critico(dano, chance=0.30, multiplicador=1.5, animacao=False, verbose=False)
            return max(1, dano_final)
        return 0

