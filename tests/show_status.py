from jogo import Jogo
from models.classes import Guerreiro

j = Jogo()
# Cria um guerreiro e simula escolha de sub-classe Berserker
g = Guerreiro('lula')
g.nivel = 4
# aplica efeitos de Berserker
g.sub_classe = 'Berserker'
g.dano_base += 10
g.hp_maximo -= 20
if g.hp > g.hp_maximo:
    g.hp = g.hp_maximo
g.crit_chance += 0.10

j.personagem = g
j.ver_status()
