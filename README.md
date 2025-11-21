# Sistema de Gestão de Aventuras - RPG em Python

Um jogo RPG textual desenvolvido em Python utilizando Programação Orientada a Objetos (POO), com sistema de combate detalhado, persistência de dados e logging de eventos.

## 📋 Descrição

Este projeto é um RPG textual onde o jogador cria um personagem, enfrenta missões e inimigos, ganha experiência, coleta itens e evolui. O jogo foi desenvolvido seguindo os princípios de POO, explorando herança, encapsulamento e polimorfismo.

## 🎮 Características

- **Sistema de Classes**: Guerreiro, Mago e Arqueiro, cada um com habilidades únicas
- **Combate Detalhado**: Exibe informações completas de cada turno (HP, dano, defesa)
- **Sistema de Níveis**: Ganhe XP, suba de nível e melhore seus atributos
- **Inventário**: Colete e use itens (poções, elixirs, etc.)
- **Persistência**: Salve e carregue seu progresso em arquivos JSON
- **Logging**: Todos os eventos são registrados em arquivo .log
- **Múltiplos Inimigos**: Goblin, Lobo, Orc e Chefão com habilidades especiais

## 🚀 Como Executar

### Pré-requisitos

- Python 3.11 ou superior

### Instalação e Execução

1. Clone o repositório ou baixe os arquivos
2. Abra o terminal na pasta do projeto
3. Execute o comando:

```bash
python main.py
```

## 📁 Estrutura do Projeto

```
rpg_oo/
├── README.md
├── main.py                 # Arquivo principal que inicia o jogo
├── jogo.py                 # Classe principal que orquestra o jogo
├── models/
│   ├── base.py            # Classe base Atributos
│   ├── personagem.py      # Classe Personagem
│   ├── classes.py         # Subclasses (Guerreiro, Mago, Arqueiro)
│   ├── inimigo.py         # Classes de inimigos
│   └── missão.py          # Sistema de missões e combate
└── utils/
    ├── repositorio.py     # Sistema de persistência (JSON)
    └── logger.py          # Sistema de logging
```

## 🎯 Classes Principais

### Personagem
Classe base que representa o jogador com:
- Atributos: HP, Mana, Nível, XP, Dano, Defesa
- Métodos: `atacar()`, `usar_item()`, `ganhar_xp()`
- Inventário para armazenar itens

### Guerreiro
Subclasse especializada em combate corpo a corpo:
- Alto HP e Defesa
- Baixa Mana
- Habilidade Especial: Ataque Devastador

### Mago
Subclasse especializada em magia:
- Baixo HP e Defesa
- Alta Mana
- Habilidade Especial: Bola de Fogo

### Arqueiro
Subclasse equilibrada:
- HP e Mana médios
- Habilidade Especial: Chuva de Flechas (com chance de crítico)

### Inimigo
Classes de inimigos com diferentes dificuldades:
- **Goblin**: Inimigo fraco (HP: 14, Dano: 3)
- **Lobo**: Inimigo médio com chance de ataque duplo (HP: 25, Dano: 5)
- **Orc**: Inimigo forte (HP: 40, Dano: 7)
- **Chefão**: Inimigo poderoso com habilidades especiais (HP: 80, Dano: 10)

### Missao
Gerencia missões e combates:
- Gera inimigos aleatórios baseados na dificuldade
- Sistema de combate por turnos
- Recompensas de XP e itens

### Jogo
Orquestra o fluxo principal:
- Menu de interação
- Criação de personagem
- Gerenciamento de missões
- Salvamento e carregamento

### Repositorio
Sistema de persistência:
- Salva progresso em JSON
- Carrega dados salvos
- Compatível com todas as classes de personagem

### Logger
Sistema de logging:
- Registra todos os eventos do jogo
- Salva em arquivo `jogo.log`
- Timestamps em todas as entradas

## 🎮 Como Jogar

1. **Criar Personagem**: Escolha um nome e uma classe (Guerreiro, Mago ou Arqueiro)
2. **Encarar Missão**: Enfrente inimigos em missões aleatórias
3. **Combate**: Durante o combate, escolha entre:
   - Atacar (ataque básico)
   - Habilidade Especial (consome mana)
   - Usar Item (se tiver no inventário)
4. **Progressão**: Ganhe XP, suba de nível e melhore seus atributos
5. **Itens**: Colete itens das missões e use quando necessário
6. **Salvar/Carregar**: Salve seu progresso e continue depois

## 📊 Exemplo de Combate

```
=== Missão: Encontro na Floresta ===
Você encontrou um Goblin!
HP do inimigo: 14

--- Turno 1 ---
Escolha sua ação:
[1] Atacar
[2] Habilidade Especial (Mana: 50/50)
> 2

Léo usa habilidade especial!
Léo causa 8 de dano em Goblin!
Goblin agora tem 6 HP.

--- Turno 2 ---
Goblin causa 2 de dano em Léo!
Léo agora tem 20 HP.

=== Resultado da Missão ===
Léo venceu o combate!
XP ganho: 50
Itens obtidos: poção
```

## 🔧 Funcionalidades Técnicas

### Programação Orientada a Objetos
- **Herança**: Personagem herda de Atributos; Guerreiro, Mago e Arqueiro herdam de Personagem
- **Encapsulamento**: Atributos privados e métodos públicos bem definidos
- **Polimorfismo**: Métodos `atacar()` e `habilidade_especial()` sobrescritos nas subclasses

### Estruturas de Dados
- **Listas**: Inventário, lista de missões, lista de itens
- **Dicionários**: Dados do personagem para JSON, tipos de inimigos por dificuldade

### Persistência
- Salvamento em formato JSON
- Carregamento automático de todas as propriedades
- Compatibilidade entre sessões

### Logging
- Registro de todos os eventos importantes
- Timestamps automáticos
- Arquivo de log persistente

## 📝 Notas de Desenvolvimento

- O código está totalmente documentado com docstrings em português
- Todos os métodos principais possuem comentários explicativos
- A estrutura segue as melhores práticas de POO
- O jogo é totalmente funcional e testado

## 🎓 Conceitos Aplicados

- Classes e Objetos
- Herança e Polimorfismo
- Encapsulamento
- Métodos especiais (`__init__`, `to_dict`, `from_dict`)
- Estruturas condicionais e laços
- Listas e dicionários
- Funções e métodos
- Persistência de dados (JSON)
- Manipulação de arquivos
- Tratamento de exceções

## 📄 Licença

Este projeto foi desenvolvido como trabalho acadêmico para aprendizado de Programação Orientada a Objetos em Python.

## 👥 Integrantes

[João Gabriel, Fabricio Rychard, Luiz André, Andrew Bezerra, Luanderson Santana, Mike Daivid]

---

**Desenvolvido com Python 3.11+**

