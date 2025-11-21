"""Smoke test for critico integration.
Runs several attacks and abilities to ensure no exceptions and outputs sensible values.
"""
from models.personagem import Personagem
from models.classes import Guerreiro, Mago, Arqueiro
from utils import calcular_critico, is_critico
import random

random.seed(42)

p = Personagem('Jogador', 'Vagabundo')
g = Guerreiro('Conan')
m = Mago('Gandalf')
a = Arqueiro('Legolas')

print('--- Teste rápido de ataques (10 iterações) ---')
for i in range(10):
    print(f'[{i}] Personagem ataca →', p.atacar())
    print(f'[{i}] Guerreiro ataca  →', g.atacar())
    print(f'[{i}] Mago ataca     →', m.atacar())
    print(f'[{i}] Arqueiro ataca →', a.atacar())

print('\n--- Teste de habilidades especiais ---')
print('Guerreiro habilidade:', g.habilidade_especial())
print('Mago habilidade    :', m.habilidade_especial())
print('Arqueiro habilidade:', a.habilidade_especial())

print('\n--- Teste direto de calcular_critico com RNG determinístico ---')
rng = random.Random(123)
dano, foi = calcular_critico(20, chance=0.5, multiplicador=2.0, rng=rng, animacao=False, verbose=False)
print('Dano final:', dano, 'foi critico?', foi)

print('\nOK - script terminou sem exceções')
