import tkinter as tk
from tkinter import messagebox

class SistemaLinearApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resolução de Sistemas de Equações Lineares")
        self.root.state("normal")
        
        self.dados_sistema = None

        # instanciando a tela
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True, padx=20, pady=20)
        
        # centralizando colunas e alinhando texto ao centro
        for i in range(5):
            self.main_frame.grid_columnconfigure(i, weight=1)

        # onde informa o numero de equações
        tk.Label(self.main_frame, text="Número de equações:", anchor="e").grid(row=0, column=0, sticky="e")
        self.num_equacoes = tk.Entry(self.main_frame, width=5, justify="center")
        self.num_equacoes.grid(row=0, column=1, padx=5)

        tk.Label(self.main_frame, text="Método de resolução:", anchor="e").grid(row=0, column=2, sticky="e")
        self.metodo_var = tk.StringVar(value="Eliminação de Gauss")
        self.menu_metodo = tk.OptionMenu(self.main_frame, self.metodo_var, "Eliminação de Gauss", "Eliminação de Jordan", "Fatoração LU")
        self.menu_metodo.grid(row=0, column=3, padx=5)

        self.botao_definir = tk.Button(self.main_frame, text="Definir Sistema", command=self.definir_sistema)
        self.botao_definir.grid(row=0, column=4, padx=10)

        # frame para o sistema de equações
        self.frame_sistema = tk.Frame(self.main_frame)
        self.frame_sistema.grid(row=1, column=0, columnspan=5, pady=10)

        # botão para resolver o sistema
        self.botao_resolver = tk.Button(self.main_frame, text="Resolver Sistema", command=self.resolver_sistema, state=tk.DISABLED)
        self.botao_resolver.grid(row=2, column=0, columnspan=5, pady=10)

        # textbox para exibir o resultado
        self.resultado = tk.Text(self.main_frame, height=20, width=60, state=tk.DISABLED)
        self.resultado.grid(row=3, column=0, columnspan=5, pady=10)

        # botão para novo cálculo
        self.botao_novo = tk.Button(self.main_frame, text="Novo Cálculo", command=self.limpar_campos, state=tk.DISABLED)
        self.botao_novo.grid(row=4, column=0, columnspan=5, pady=10)

    def definir_sistema(self):
        try:
            self.n = int(self.num_equacoes.get())
            if self.n <= 0:
                raise ValueError("O número de equações deve ser positivo.")
            
            # Se já existir um sistema de equações, não redefine.
            if self.dados_sistema is None:
                for widget in self.frame_sistema.winfo_children():
                    widget.destroy()
                
                self.entradas = []
                tk.Label(self.frame_sistema, text="Coeficientes e termos independentes:").grid(row=0, column=0, columnspan=self.n + 1)
                
                for i in range(self.n):
                    linha = []
                    for j in range(self.n):
                        entrada_coef = tk.Entry(self.frame_sistema, width=5)
                        entrada_coef.grid(row=i + 1, column=j)
                        linha.append(entrada_coef)
                    
                    entrada_termo = tk.Entry(self.frame_sistema, width=5)
                    entrada_termo.grid(row=i + 1, column=self.n)
                    linha.append(entrada_termo)
                    
                    self.entradas.append(linha)
                
                # Armazenar os dados do sistema
                self.dados_sistema = [linha for linha in self.entradas]
            
            self.botao_resolver.config(state=tk.NORMAL)
        
        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")


    def resolver_sistema(self):
        try:
            matriz_aumentada = []
            if self.dados_sistema:
                # Reaproveitar os dados armazenados
                for i in range(self.n):
                    linha = []
                    for j in range(self.n + 1):
                        valor = float(self.dados_sistema[i][j].get())  # Usar os dados armazenados
                        linha.append(valor)
                    matriz_aumentada.append(linha)
            else:
                raise ValueError("Sistema de equações não definido.")
            
            self.resultado.config(state=tk.NORMAL)
            self.resultado.delete(1.0, tk.END)
            self.resultado.insert(tk.END, "Passo a passo do cálculo:\n\n")

            metodo = self.metodo_var.get()
            if metodo == "Eliminação de Gauss":
                matriz_triangular = self.eliminacao_gauss(self.n, matriz_aumentada)
                solucoes = self.substituicao_reversa(self.n, matriz_triangular)
            elif metodo == "Eliminação de Jordan":
                solucoes = self.eliminacao_jordan(matriz_aumentada)
            elif metodo == "Fatoração LU":
                solucoes = self.fatoracao_lu(matriz_aumentada)

            self.resultado.insert(tk.END, "\nSoluções do sistema:\n")
            for i, solucao in enumerate(solucoes):
                self.resultado.insert(tk.END, f"x{i + 1} = {solucao:.2f}\n")
            self.resultado.config(state=tk.DISABLED)
            
            self.botao_novo.config(state=tk.NORMAL)
            self.botao_resolver.config(state=tk.DISABLED)
        
        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")


    def eliminacao_gauss(self, n, matriz_aumentada):
        for i in range(n):
            # se o pivô for zero vai procurar
            if matriz_aumentada[i][i] == 0:
                max_linha = i
                for k in range(i + 1, n):
                    if matriz_aumentada[k][i] != 0:
                        max_linha = k
                        break
                
                # troca se encontrar uma linha em que o elemento na coluna não seja zero
                if max_linha != i:
                    matriz_aumentada[i], matriz_aumentada[max_linha] = matriz_aumentada[max_linha], matriz_aumentada[i]
                    self.resultado.insert(tk.END, f"Troca linha {i+1} com linha {max_linha+1} para evitar pivô zero\n")
                    for row in matriz_aumentada:
                        self.resultado.insert(tk.END, f"{[round(num, 4) for num in row]}\n") 

            for k in range(i + 1, n):
                m = matriz_aumentada[k][i] / matriz_aumentada[i][i]
                m = round(m, 4)  
                self.resultado.insert(tk.END, f"Aplicando fator {m} para eliminar elemento da linha {k+1}\n")
                for j in range(i, n + 1):
                    matriz_aumentada[k][j] = matriz_aumentada[k][j] - (m * matriz_aumentada[i][j])
                    # if abs(matriz_aumentada[k][j]) < 1e-10:  # tolerância para valores pequenos
                        # matriz_aumentada[k][j] = 0.0
                self.resultado.insert(tk.END, f"Estado da matriz após eliminação na linha {i+1}:\n")
                for row in matriz_aumentada:
                    self.resultado.insert(tk.END, f"{[round(num, 4) for num in row]}\n")
                self.resultado.insert(tk.END, "\n")
        return matriz_aumentada

    def substituicao_reversa(self, n, matriz_aumentada):
        x = [0] * n
        for i in range(n - 1, -1, -1):
            termo_independente = matriz_aumentada[i][n]
            x[i] = termo_independente

            subtracoes = []

            for j in range(i + 1, n):
                termo_subtracao = matriz_aumentada[i][j] * x[j]
                x[i] -= termo_subtracao

                subtracoes.append(f"{matriz_aumentada[i][j]:.4f} * {x[j]:.4f}")

                self.resultado.insert(
                    tk.END, f"Subtraindo {matriz_aumentada[i][j]:.4f} * {x[j]:.4f}"
                            f"(= {termo_subtracao:.4f}) de {termo_independente:.4f}\n"
                )

            x[i] /= matriz_aumentada[i][i]

            if subtracoes:
                expressao_subtracoes = " - ".join(subtracoes)
                self.resultado.insert(
                    tk.END, f"\nCalculando x[{i+1}]:\n"
                    f"=> ({termo_independente:.4f} - {expressao_subtracoes}) / {matriz_aumentada[i][i]:.4f}\n"
                    f"=> x[{i+1}] = {x[i]:.4f}\n\n"
                )
            else:
                self.resultado.insert(
                    tk.END, f"\nCalculando x[{i+1}]:\n"
                    f"=> ({termo_independente:.4f})/ {matriz_aumentada[i][i]:.4f}\n"
                    f"=> x[{i+1}] = {x[i]:.4f}\n\n"
                )   
        return x

    def eliminacao_jordan(self, matriz_aumentada):
        self.resultado.insert(tk.END, "Matriz aumentada inicial:\n")
        for row in matriz_aumentada:
            self.resultado.insert(tk.END, f"{[round(num, 4) for num in row]}\n")

        n = len(matriz_aumentada)
        self.resultado.insert(tk.END, "\nInício da eliminação de Jordan:\n")

        for i in range(n):
            self.resultado.insert(tk.END, f"\nEscolhendo pivô a[{i+1}][{i+1}] = {matriz_aumentada[i][i]:.4f}\n")
            
            pivot = matriz_aumentada[i][i]
            self.resultado.insert(tk.END, f"Dividindo linha {i+1} pelo pivô ({pivot:.4f}):\n")
            for j in range(i, n + 1):
                matriz_aumentada[i][j] /= pivot
            for row in matriz_aumentada:
                self.resultado.insert(tk.END, f"{[round(num, 4) for num in row]}\n")

            for k in range(n):
                if k != i:
                    m = matriz_aumentada[k][i]
                    self.resultado.insert(tk.END, f"\nEliminando entrada a[{k+1}][{i+1}] usando a linha {i+1}:\n")
                    self.resultado.insert(tk.END, f"Multiplicador m = {matriz_aumentada[k][i]:.4f}/{matriz_aumentada[i][i]:.4f}\n")
                    self.resultado.insert(tk.END, f"Logo: L{k+1}={matriz_aumentada[k][i]:.4f}-({m:.4f}*{matriz_aumentada[i][i]:.4f})\n")
                    for j in range(i, n + 1):
                        matriz_aumentada[k][j] -= m * matriz_aumentada[i][j]
                    for row in matriz_aumentada:
                        self.resultado.insert(tk.END, f"{[round(num, 4) for num in row]}\n")
        
        solucoes = [matriz_aumentada[i][n] for i in range(n)]
        
        return solucoes


    def fatoracao_lu(self, matriz_aumentada):
        n = len(matriz_aumentada)
        L = [[0.0] * n for _ in range(n)]
        U = [[0.0] * n for _ in range(n)]
        
        self.resultado.insert(tk.END, "Início da fatoração LU:\n")
        
        # processo de fatoração
        for i in range(n):
            self.resultado.insert(tk.END, f"\nAtualizando U para i={i+1}:\n")
            
            # atualiza a linha i da matriz U
            for k in range(i, n):
                soma = sum(L[i][j] * U[j][k] for j in range(i))
                U[i][k] = matriz_aumentada[i][k] - soma
                self.resultado.insert(tk.END, f"U{i+1}{k+1} = a{i+1}{k+1} - ({'+'.join([f'L[{i+1}][{j+1}] * U[{j+1}][{k+1}]' for j in range(i)])}) = {U[i][k]:.4f}\n")

            # pra mostrar a matriz U dps de att cada linha
            self.resultado.insert(tk.END, "\nMatriz U atualizada:\n")
            for row in U:
                self.resultado.insert(tk.END, f"{[round(num, 4) for num in row]}\n")

            self.resultado.insert(tk.END, f"\nAtualizando L para i={i+1}:\n")
            
            # atualizando agora a linha i da matriz L
            for k in range(i, n):
                if i == k:
                    L[i][i] = 1.0
                    self.resultado.insert(tk.END, f"L[{i+1}][{i+1}] = 1\n")
                else:
                    soma = sum(L[k][j] * U[j][i] for j in range(i))
                    L[k][i] = (matriz_aumentada[k][i] - soma) / U[i][i]
                    self.resultado.insert(tk.END, f"L{k+1}{i+1} = (a{k+1}{i+1} - ({'+'.join([f'L[{k+1}][{j+1}] * U[{j+1}][{i+1}]' for j in range(i)])})) / U[{i+1}][{i+1}] = {L[k][i]:.4f}\n")

            # mostra a matriz L dps de alterar
            self.resultado.insert(tk.END, "\nMatriz L atualizada:\n")
            for row in L:
                self.resultado.insert(tk.END, f"{[round(num, 4) for num in row]}\n")

        # exivbe as matrizes finais L e U
        self.resultado.insert(tk.END, "\nMatriz L final:\n")
        for row in L:
            self.resultado.insert(tk.END, f"{[round(num, 4) for num in row]}\n")
        self.resultado.insert(tk.END, "\nMatriz U final:\n")
        for row in U:
            self.resultado.insert(tk.END, f"{[round(num, 4) for num in row]}\n")
        
        self.resultado.insert(tk.END, "\nComparação com a matriz aumentada original (A):\n")
        for i in range(n):
            original_row = [matriz_aumentada[i][j] for j in range(n)]
            self.resultado.insert(tk.END, f"A linha original {i+1}: {original_row}\n")
            reconstructed_row = [sum(L[i][k] * U[k][j] for k in range(n)) for j in range(n)]
            self.resultado.insert(tk.END, f"Reconstruída com L*U {i+1}: {[round(num, 4) for num in reconstructed_row]}\n")
        
        # resolvendo os sistemas triangulares
        self.resultado.insert(tk.END, "\nResolvendo L * y = b:\n")
        y = [0] * n
        for i in range(n):
            y[i] = matriz_aumentada[i][-1] - sum(L[i][j] * y[j] for j in range(i))
            self.resultado.insert(tk.END, f"y[{i+1}] = {y[i]:.4f}\n")

        self.resultado.insert(tk.END, "\nResolvendo U * x = y:\n")
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
            self.resultado.insert(tk.END, f"x[{i+1}] = {x[i]:.4f}\n")

        return x



    def limpar_campos(self):
        self.num_equacoes.delete(0, tk.END)
        self.resultado.config(state=tk.NORMAL)
        self.resultado.delete(1.0, tk.END)
        self.resultado.config(state=tk.DISABLED)
        
        for widget in self.frame_sistema.winfo_children():
            widget.destroy()
        
        self.dados_sistema = None
        self.botao_resolver.config(state=tk.DISABLED)
        self.botao_novo.config(state=tk.DISABLED)


root = tk.Tk()
app = SistemaLinearApp(root)
root.mainloop()
