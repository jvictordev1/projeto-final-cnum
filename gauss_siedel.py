import numpy as np

def readMatrix(arq):
    with open(arq, 'r') as arq:
        lines = arq.readlines()

    A = []
    b = []
    x0 = []
    matrix = True

    for line in lines:
        line = line.strip()
        print(line)

def gauss_seidel(A, b, x0, max_iter, tol):
    n = len(A) # tamanho da matriz
    x = x0.copy() # copia o array da iteração 0 para a var x
    it = 0 # iterações
    
    while it < max_iter: # enquanto as iterações forem menores que o limite de iterações
        x_old = x.copy() # copia o array da ultima iteração para a var x_old
        for i in range(n): # para i menor que 3
            sum1 = sum(A[i,j] * x[j] for j in range(i)) # multiplica os coeficientes do lado esquerdo da diagonal principal pelos valores de x na iteração vigente   
            sum2 = sum(A[i,j] * x[j] for j in range(i+1, n)) # multiplica os coeficientes do lado direito da diagonal principal pelos valores de x na iteração vigente
            x[i] = round(((b[i] - sum1 - sum2) / A[i,i]), 3) # calcula o x(i+1)^(k+1) e poe no indice i do array x
        
        error = np.max(np.abs(x - x_old)) / np.max(np.abs(x_old)) # calcula o erro na iteração
        it += 1 # soma 1 na iteração
        if error < tol: # se o erro da iteração for menor que a tolerância, retorna o resultado
            return x, it, error
            
    print("Aviso: O método não convergiu no número máximo de iterações") # caso as iterações tenham atingido o limite, retorna esse aviso
    return x, it, error

def menu():
    while True:
        cond = input("Para encerrar, digite 0.")
        if cond == 0:
            break
    A = np.array([
        [10, 2, 1],
        [1, 5, 1],
        [2, 3, 10]
    ], dtype=float)  # Importante: usar float para evitar divisão inteira
    
    b = np.array([7, -8, 6], dtype=float)
    x0 = np.array([0.7, -1.6, 0.6], dtype=float)
    
    solucao, iteracoes, erro = gauss_seidel(A, b, x0, 100, 5e-2)
    
    print("\nResultados:")
    print(f"Solução encontrada: {solucao}")
    print(f"Número de iterações: {iteracoes}")
    print(f"Erro final: {erro}")

if __name__ == "__main__":
    readMatrix('arq.txt')