import numpy as np
import matplotlib.pyplot as plt

def calcularErroQuadratico(valoresReais, valoresAjustados):
    erro = np.sum((valoresReais - valoresAjustados) ** 2)
    return erro

def ajusteLinear(x, y):
    numeroPontos = len(x)
    matrizDesign = np.vstack([x, np.ones(numeroPontos)]).T
    coeficienteAngular, coeficienteLinear = np.linalg.lstsq(matrizDesign, y, rcond=None)[0]
    return coeficienteAngular, coeficienteLinear

def ajusteQuadratico(x, y):
    numeroPontos = len(x)
    matrizDesign = np.vstack([x**2, x, np.ones(numeroPontos)]).T
    coeficientes = np.linalg.lstsq(matrizDesign, y, rcond=None)[0]
    coeficienteA, coeficienteB, coeficienteC = coeficientes
    return coeficienteA, coeficienteB, coeficienteC

def ajusteExponencial(x, y):
    if np.any(y <= 0):
        raise ValueError("Todos os valores de y devem ser positivos para o ajuste exponencial.")
    
    logY = np.log(y)
    numeroPontos = len(x)
    matrizDesign = np.vstack([x, np.ones(numeroPontos)]).T
    coeficienteB, lnCoeficienteA = np.linalg.lstsq(matrizDesign, logY, rcond=None)[0]
    coeficienteA = np.exp(lnCoeficienteA)
    return coeficienteA, coeficienteB

def executarAjustes(valoresX, valoresY):
    # Ajuste Linear
    coeficienteAngularLinear, coeficienteLinear = ajusteLinear(valoresX, valoresY)
    valoresYLinear = coeficienteAngularLinear * valoresX + coeficienteLinear
    erroLinear = calcularErroQuadratico(valoresY, valoresYLinear)

    # Ajuste Quadrático
    coeficienteAQuadratico, coeficienteBQuadratico, coeficienteCQuadratico = ajusteQuadratico(valoresX, valoresY)
    valoresYQuadratico = (coeficienteAQuadratico * valoresX**2 +
                          coeficienteBQuadratico * valoresX +
                          coeficienteCQuadratico)
    erroQuadratico = calcularErroQuadratico(valoresY, valoresYQuadratico)

    # Tentando o Ajuste Exponencial
    try:
        coeficienteAExponencial, coeficienteBExponencial = ajusteExponencial(valoresX, valoresY)
        valoresYExponencial = coeficienteAExponencial * np.exp(coeficienteBExponencial * valoresX)
        erroExponencial = calcularErroQuadratico(valoresY, valoresYExponencial)
        ajusteExponencialValido = True
    except ValueError as e:
        print(f"Ajuste Exponencial não realizado: {e}")
        ajusteExponencialValido = False

    print("\nResultados dos Ajustes:")
    print("Ajuste Linear:")
    print(f"  Coeficientes: coeficienteAngular = {coeficienteAngularLinear:.4f}, coeficienteLinear = {coeficienteLinear:.4f}")
    print(f"  Erro Quadrático: {erroLinear:.4f}\n")

    print("Ajuste Quadrático:")
    print(f"  Coeficientes: a = {coeficienteAQuadratico:.4f}, b = {coeficienteBQuadratico:.4f}, c = {coeficienteCQuadratico:.4f}")
    print(f"  Erro Quadrático: {erroQuadratico:.4f}\n")

    if ajusteExponencialValido:
        print("Ajuste Exponencial:")
        print(f"  Coeficientes: a = {coeficienteAExponencial:.4f}, b = {coeficienteBExponencial:.4f}")
        print(f"  Erro Quadrático: {erroExponencial:.4f}\n")
    else:
        print("Ajuste Exponencial não foi realizado devido a valores de Y não positivos ou igual a 0 em um situação que ele não pode ser 0.\n")

    # Plotando os resultados
    plt.figure(figsize=(14, 6))

    # Gráfico do Ajuste Linear
    plt.subplot(1, 3, 1)
    plt.scatter(valoresX, valoresY, color='blue', label='Dados Reais')
    plt.plot(valoresX, valoresYLinear, color='red', label='Ajuste Linear')
    plt.title('Ajuste Linear')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)

    # Gráfico do Ajuste Quadrático
    plt.subplot(1, 3, 2)
    plt.scatter(valoresX, valoresY, color='blue', label='Dados Reais')
    plt.plot(valoresX, valoresYQuadratico, color='green', label='Ajuste Quadrático')
    plt.title('Ajuste Quadrático')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)

    # Gráfico do Ajuste Exponencial (Caso seja aplicado)
    plt.subplot(1, 3, 3)
    plt.scatter(valoresX, valoresY, color='blue', label='Dados Reais')
    if ajusteExponencialValido:
        plt.plot(valoresX, valoresYExponencial, color='purple', label='Ajuste Exponencial')
        plt.title('Ajuste Exponencial')
    else:
        plt.title('Ajuste Exponencial não realizado')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show(block=False)
    input("Pressione Enter para continuar...")
    plt.close('all')

def solicitarDadosDoUsuario():
    print("\nPor favor, insira os valores de X e Y.")
    print("Digite os valores separados por vírgula. Exemplo: 1, 2, 3, 4")

    while True:
        try:
            entradaX = input("Valores de X: ")
            valoresX = np.array([float(valor.strip()) for valor in entradaX.split(",")])
            entradaY = input("Valores de Y: ")
            valoresY = np.array([float(valor.strip()) for valor in entradaY.split(",")])

            if len(valoresX) != len(valoresY):
                print("O número de valores de X e Y deve ser igual. Tente novamente.\n")
                continue

            return valoresX, valoresY
        except ValueError:
            print("Entrada inválida. Certifique-se de digitar números separados por vírgula.\n")

def menuPrincipal():
    while True:
        print("\nBem-vindo ao Ajuste de Curvas!")
        print("Escolha uma opção:")
        print("1. Usar dados da propria questao")
        print("2. Inserir novos dados")
        print("3. Sair")
        opcao = input("Opção: ")

        if opcao == '1':
            valoresX = np.array([0, 1.5, 2.6, 4.2, 6, 8.2, 10, 11.4])
            valoresY = np.array([18, 13, 11, 9, 6, 4, 2, 1])
            executarAjustes(valoresX, valoresY)
        elif opcao == '2':
            valoresX, valoresY = solicitarDadosDoUsuario()
            executarAjustes(valoresX, valoresY)
        elif opcao == '3':
            print("Obrigado por usar o programa. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.\n")

if __name__ == "__main__":
    menuPrincipal()
