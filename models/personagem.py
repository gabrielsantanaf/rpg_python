"""
Módulo que define a classe Personagem e suas funcionalidades.
"""

from models.base import Atributos
from models.inventario import Item


class Personagem(Atributos):
    """
    Classe que representa o personagem do jogador.
    Herda de Atributos e adiciona funcionalidades específicas do jogador.
    """
    
    def __init__(self, nome, classe, hp=100, nivel=1, xp=0):
        """
        Inicializa um personagem.
        
        Args:
            nome (str): Nome do personagem
            classe (str): Classe do personagem (Guerreiro, Mago, etc.)
            hp (int): Pontos de vida iniciais
            nivel (int): Nível inicial do personagem
            xp (int): Experiência inicial
        """
        super().__init__(nome, hp, hp)
        self.classe = classe
        self.nivel = nivel
        self.xp = xp
        self.xp_proximo_nivel = 100
        self.inventario = []
        self.mana = 50
        self.mana_maxima = 50
        self.dano_base = 10
        self.defesa = 5
    
    def atacar(self):
        """
        Realiza um ataque básico.
        
        Returns:
            int: Dano causado pelo ataque
        """
        import random
        # Dano varia entre 80% e 120% do dano base
        dano = int(self.dano_base * random.uniform(0.8, 1.2))
        return max(1, dano)
    
    def habilidade_especial(self):
        """
        Habilidade especial genérica (deve ser sobrescrita nas subclasses).
        
        Returns:
            int: Dano causado pela habilidade especial (0 se não tiver mana)
        """
        # Implementação básica para personagens genéricos
        if self.mana >= 20:
            import random
            self.mana -= 20
            dano = int(self.dano_base * random.uniform(1.3, 1.7))
            return max(1, dano)
        return 0
    
    def usar_item(self, item):
        """
        Usa um item do inventário.
        
        Args:
            item (str): Nome do item a ser usado
            
        Returns:
            bool: True se o item foi usado com sucesso, False caso contrário
        """
        # Suporta receber tanto um objeto Item quanto uma string com o nome
        nome_item = item.nome if hasattr(item, "nome") else str(item)

        # Procura o item no inventário (padronizamos a lista para conter objetos Item)
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
                else:
                    return False
        return False
    
    def adicionar_item(self, item):
        """
        Adiciona um item ao inventário.
        
        Args:
            item (str): Nome do item a ser adicionado
        """
        # Se receber uma string, cria um Item simples; se já for Item, adiciona diretamente
        if isinstance(item, str):
            self.inventario.append(Item(item, ""))
        elif isinstance(item, Item):
            self.inventario.append(item)
        else:
            # Tenta converter para string como fallback
            self.inventario.append(Item(str(item), ""))
    
    def ganhar_xp(self, quantidade):
        """
        Adiciona experiência ao personagem e verifica se subiu de nível.
        
        Args:
            quantidade (int): Quantidade de XP a ser adicionada
            
        Returns:
            bool: True se o personagem subiu de nível, False caso contrário
        """
        self.xp += quantidade
        subiu_nivel = False
        
        while self.xp >= self.xp_proximo_nivel:
            self.xp -= self.xp_proximo_nivel
            self.nivel += 1
            self.xp_proximo_nivel = int(self.xp_proximo_nivel * 1.5)
            self.hp_maximo += 20
            self.hp = self.hp_maximo  # Restaura HP ao subir de nível
            self.dano_base += 2
            self.defesa += 1
            subiu_nivel = True
        
        return subiu_nivel
    
    def to_dict(self):
        """
        Converte o personagem para um dicionário (para salvar em JSON).
        
        Returns:
            dict: Dicionário com os dados do personagem
        """
        return {
            "nome": self.nome,
            "classe": self.classe,
            "hp": self.hp,
            "hp_maximo": self.hp_maximo,
            "nivel": self.nivel,
            "xp": self.xp,
            "xp_proximo_nivel": self.xp_proximo_nivel,
            "inventario": [it.nome if hasattr(it, "nome") else str(it) for it in self.inventario],
            "mana": self.mana,
            "mana_maxima": self.mana_maxima,
            "dano_base": self.dano_base,
            "defesa": self.defesa
        }
    
    @classmethod
    def from_dict(cls, dados):
        """
        Cria um personagem a partir de um dicionário (para carregar de JSON).
        
        Args:
            dados (dict): Dicionário com os dados do personagem
            
        Returns:
            Personagem: Instância do personagem criada
        """
        personagem = cls(
            dados["nome"],
            dados["classe"],
            dados.get("hp", 100),
            dados.get("nivel", 1),
            dados.get("xp", 0)
        )
        personagem.hp_maximo = dados.get("hp_maximo", personagem.hp)
        personagem.xp_proximo_nivel = dados.get("xp_proximo_nivel", 100)
        # Converte inventário (lista de nomes) para objetos Item
        inventario_dados = dados.get("inventario", [])
        personagem.inventario = [Item(nome, "") for nome in inventario_dados]
        personagem.mana = dados.get("mana", 50)
        personagem.mana_maxima = dados.get("mana_maxima", 50)
        personagem.dano_base = dados.get("dano_base", 10)
        personagem.defesa = dados.get("defesa", 5)
        return personagem
