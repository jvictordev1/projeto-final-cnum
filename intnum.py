import numpy as np
import matplotlib.pyplot as plt
import matplotlib.rcsetup as rcsetup
print(rcsetup.all_backends)

def regraTrapezio(y, h):
    area = y[0] + y[-1] + 2 * np.sum(y[1:-1])
    area *= (h / 2)
    return area

def regraSimpson(y, h):
    n = len(y) - 1
    if n % 2 != 0:
        raise ValueError("A Regra de Simpson requer um número par de subintervalos (n deve ser par).")
    somaPares = np.sum(y[2:n:2])  # Termos pares internos
    somaImpares = np.sum(y[1:n:2])  # Termos ímpares
    area = y[0] + y[n] + 2 * somaPares + 4 * somaImpares
    area *= (h / 3)
    return area

def executarCalculos(x, y):
    n = len(x) - 1
    h = x[1] - x[0]

    # Verifica se os pontos estão igualmente espaçados
    if not np.allclose(np.diff(x), h):
        print("Os pontos não estão igualmente espaçados. Não é possível aplicar os métodos.")
        return

    try:
        areaTrapezio = regraTrapezio(y, h)
        print(f"\nÁrea calculada pela Regra do Trapézio: {areaTrapezio:.4f} m²")
    except Exception as e:
        print(f"Erro ao calcular a área pela Regra do Trapézio: {e}")

    try:
        areaSimpson = regraSimpson(y, h)
        print(f"Área calculada pela Regra de Simpson: {areaSimpson:.4f} m²")
    except Exception as e:
        print(f"Erro ao calcular a área pela Regra de Simpson: {e}")

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'bo-', label='Perfil do Rio')
    plt.fill_between(x, y, color='skyblue', alpha=0.5)
    plt.title('Seção Reta do Rio')
    plt.xlabel('Distância (m)')
    plt.ylabel('Profundidade (m)')
    plt.gca().invert_yaxis()
    plt.legend()
    plt.grid(True)
    plt.show(block=False)
    input("Pressione Enter para continuar...")
    plt.close('all')

def solicitarDadosDoUsuario():
    print("\nPor favor, insira os valores de distância (X) e profundidade (Y).")
    print("Digite os valores separados por vírgula. Exemplo: 0, 1, 2, 3, 4")
    while True:
        try:
            entradaX = input("Valores de X (distância): ")
            x = np.array([float(valor.strip()) for valor in entradaX.split(",")])
            entradaY = input("Valores de Y (profundidade): ")
            y = np.array([float(valor.strip()) for valor in entradaY.split(",")])

            if len(x) != len(y):
                print("O número de valores de X e Y deve ser igual. Tente novamente.\n")
                continue

            return x, y
        except ValueError:
            print("Entrada inválida. Certifique-se de digitar números separados por vírgula.\n")

def menuPrincipal():
    while True:
        print("\nBem-vindo ao cálculo da área da seção reta do rio!")
        print("Escolha uma opção:")
        print("1. Usar dados padrão")
        print("2. Inserir novos dados")
        print("3. Sair")
        opcao = input("Opção: ")

        if opcao == '1':
            x = np.array([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
            y = np.array([0, 1.8, 2, 4, 4, 6, 4, 3.6, 3.4, 2.8, 0])
            executarCalculos(x, y)
        elif opcao == '2':
            x, y = solicitarDadosDoUsuario()
            executarCalculos(x, y)
        elif opcao == '3':
            print("Obrigado por usar o programa. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.\n")

if __name__ == "__main__":
    menuPrincipal()
