"""
Módulo que implementa o sistema de persistência de dados.
Salva e carrega o progresso do jogo em arquivos JSON.
"""

import json
import os
from models.personagem import Personagem
from models.inventario import Item
from models.classes import Guerreiro, Mago, Arqueiro


class Repositorio:
    """
    Classe responsável por salvar e carregar dados do jogo em formato JSON.
    """
    
    def __init__(self, arquivo_save="save.json"):
        """
        Inicializa o repositório.
        
        Args:
            arquivo_save (str): Nome do arquivo de save
        """
        self.arquivo_save = arquivo_save
    
    def salvar(self, personagem):
        """
        Salva o estado do personagem em um arquivo JSON.
        
        Args:
            personagem: Instância do personagem a ser salva
            
        Returns:
            bool: True se salvou com sucesso, False caso contrário
        """
        try:
            dados = personagem.to_dict()
            
            with open(self.arquivo_save, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Erro ao salvar o jogo: {e}")
            return False
    
    def carregar(self):
        """
        Carrega o estado do personagem de um arquivo JSON.
        
        Returns:
            Personagem: Instância do personagem carregada, ou None se houver erro
        """
        try:
            if not os.path.exists(self.arquivo_save):
                return None
            
            with open(self.arquivo_save, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            # Cria o personagem baseado na classe
            classe = dados.get("classe", "Guerreiro")
            
            if classe == "Guerreiro":
                personagem = Guerreiro(dados["nome"])
            elif classe == "Mago":
                personagem = Mago(dados["nome"])
            elif classe == "Arqueiro":
                personagem = Arqueiro(dados["nome"])
            else:
                # Fallback para Personagem genérico
                personagem = Personagem(dados["nome"], classe)
            
            # Restaura os atributos do dicionário
            personagem.hp = dados.get("hp", personagem.hp)
            personagem.hp_maximo = dados.get("hp_maximo", personagem.hp_maximo)
            # Garante que o HP atual não exceda o máximo (caso o save esteja inconsistente)
            if personagem.hp > personagem.hp_maximo:
                personagem.hp = personagem.hp_maximo
            personagem.nivel = dados.get("nivel", 1)
            personagem.xp = dados.get("xp", 0)
            personagem.xp_proximo_nivel = dados.get("xp_proximo_nivel", 100)
            # Converte inventário salvo (lista de nomes) para objetos Item
            personagem.inventario = [Item(nome, "") for nome in dados.get("inventario", [])]
            personagem.mana = dados.get("mana", personagem.mana_maxima)
            personagem.mana_maxima = dados.get("mana_maxima", personagem.mana_maxima)
            personagem.dano_base = dados.get("dano_base", personagem.dano_base)
            personagem.defesa = dados.get("defesa", personagem.defesa)
            # Restaura sub-classe e atributos específicos de subclasses, se presentes
            personagem.sub_classe = dados.get("sub_classe", personagem.sub_classe if hasattr(personagem, 'sub_classe') else None)
            personagem.crit_chance = dados.get("crit_chance", getattr(personagem, 'crit_chance', 0.05))
            personagem.stun_chance = dados.get("stun_chance", getattr(personagem, 'stun_chance', 0.0))
            personagem.dot_sangramento = dados.get("dot_sangramento", getattr(personagem, 'dot_sangramento', 0.0))
            personagem.buff_dano = dados.get("buff_dano", getattr(personagem, 'buff_dano', 1.0))
            personagem.chance_queimadura = dados.get("chance_queimadura", getattr(personagem, 'chance_queimadura', 0.0))
            personagem.cura_base = dados.get("cura_base", getattr(personagem, 'cura_base', 0))
            
            return personagem
        except Exception as e:
            print(f"Erro ao carregar o jogo: {e}")
            return None
    
    def existe_save(self):
        """
        Verifica se existe um arquivo de save.
        
        Returns:
            bool: True se existe save, False caso contrário
        """
        return os.path.exists(self.arquivo_save)

