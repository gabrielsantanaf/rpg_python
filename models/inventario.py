class Item:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

    def __str__(self):
        return self.nome

class Inventario:
    def __init__(self):
        self.itens = []

    def adicionar_item(self, item):
        self.itens.append(item)

    def listar_itens(self):
        if not self.itens:
            print("(vazio)")
            return
        for i, item in enumerate(self.itens, start=1):
            # Suporta tanto objetos Item quanto strings simples
            if hasattr(item, "nome"):
                nome = item.nome
                descricao = getattr(item, "descricao", "")
            else:
                nome = str(item)
                descricao = ""
            print(f"{i}. {nome} - {descricao}")

    def usar_item(self, indice):
        if indice < 1 or indice > len(self.itens):
            print("Índice inválido!")
            return
        item = self.itens.pop(indice - 1)
        # Imprime nome adequadamente
        nome = item.nome if hasattr(item, "nome") else str(item)
        print(f"Você usou o item {nome}!")

def main():
    inventario = Inventario()

    while True:
        print("\n1. Adicionar item")
        print("2. Listar itens")
        print("3. Usar item")
        print("4. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Digite o nome do item: ")
            descricao = input("Digite a descrição do item: ")
            item = Item(nome, descricao)
            inventario.adicionar_item(item)
        elif opcao == "2":
            inventario.listar_itens()
        elif opcao == "3":
            inventario.listar_itens()
            indice = int(input("Digite o número do item que deseja usar: "))
            inventario.usar_item(indice)
        elif opcao == "4":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()