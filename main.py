from operator import itemgetter

class restaurant:
    def __init__(self):
        self.mesas = {}
        self.estoque = {}
        self.cardapio = {}
        self.pedidos = []
        self.aux = {}
    
    def atualizar_mesas(self): #deve-se ler o nome de um arquivo contendo uma configuração de mesas do restaurante
        #Inserir novas mesas no restaurante;
        #Inserir novas áreas no restaurante caso seja lida alguma mesa em uma área nova;
        #Atualizar informações de mesas já existentes.
        arq = open('P3_Arquivos_Mesas\{}'.format(entradas[x+1]),'r')
        for elemento in arq.readlines():
            elemento = elemento.strip('\n')
            elemento = elemento.split(',')
            self.mesas[elemento[0]] = elemento[2]
            self.aux[elemento[0]] = elemento[1]

        self.aux = sorted(self.aux.items(),key=itemgetter(1))
        arq.close()

    def atualizar_cardapio(self):#deve-se ler um arquivo contendo uma configuração de cardápio contendo itens de cardápio e seus respectivos ingredientes.
        #Caso seja lido um item que não exista no cardápio atual, 
        # deve-se adicioná-lo ao cardápio junto com seus respectivos ingredientes.
        #Caso seja lido um item que já exista no cardápio, 
        # deve-se atualizar este item com as novas informações de ingredientes, sobrescrevendo as antigas.
        arq = open('P3_Arquivos_Cardapio\{}'.format(entradas[x+1]),'r')
        for elemento in arq.readlines():
            elemento = elemento.strip('\n')
            elemento = elemento.split(',')
            self.cardapio[elemento[0]] = []
            for ingrediente in elemento:
                if ingrediente != elemento[0]:
                    self.cardapio[elemento[0]].append(ingrediente)
        arq.close()

    def atualizar_estoque(self):#deve-se ler um arquivo contendo uma configuração de estoque contendo ingredientes e suas respectivas quantidades.
        #Caso seja lido algum ingrediente que não exista no estoque, 
        # deve-se adicioná-lo ao estoque com sua respectiva quantidade.
        #Caso seja lido algum ingrediente que já exista no estoque, 
        # deve-se adicioná-lo ao estoque somando sua respectiva quantidade 
        #com a quantidade já armazenada no estoque.
        arq = open('P3_Arquivos_Estoque\{}'.format(entradas[x+1]),'r')
        for elemento in arq.readlines():
            elemento = elemento.strip('\n')
            elemento = elemento.split(',')
            if elemento[0] in self.estoque:
                self.estoque[elemento[0]] += int(elemento[1])
            else:
                self.estoque[elemento[0]] = int(elemento[1])
        arq.close()
    
    def relatorio_mesas(self):
        #Imprime os pedidos feitos pelo restaurante em ordem crescente de número de mesa e 
        #em ordem alfabética do nome dos itens pedidos, no seguinte formato:
        if len(self.mesas) == 0:
            print('- restaurante sem mesas')
        else:
            detec = None
            for chave in self.aux:
                if detec != chave[1]: 
                    print(f'area:{chave[1]}')
                print(f'- mesa: {chave[0]}, status:{self.mesas[chave[0]]}')
                detec = chave[1]

        self.aux = dict(self.aux)
    
    def relatorio_cardapio(self):
        if len(self.cardapio) == 0:
            print('- cardapio vazio')
        else:
            self.cardapio = sorted(self.cardapio.items(),key=itemgetter(0))
            for elemento in self.cardapio:
                elemento[1].sort()

            for elemento in self.cardapio:
                print(f'item: {elemento[0]}')
                detec = None
                for ingrediente in elemento[1]:
                    if detec != ingrediente:
                        print(f'-{ingrediente}: {elemento[1].count(ingrediente)}')
                    detec = ingrediente

        self.cardapio = dict(self.cardapio)
    
    def relatorio_estoque(self):
        if len(self.estoque) == 0:
            print('- estoque vazio')
        else:
            self.estoque = sorted(self.estoque.items(),key=itemgetter(0))
            for elemento in self.estoque:
                print(f'{elemento[0]}: {elemento[1]}')
        
        self.estoque = dict(self.estoque)

    def fazer_pedidos(self):
        pedido = entradas[x+1].split(',')
        
        #verficar se a mesa existe
        if pedido[0] not in self.mesas:
            print(f'erro >> mesa {pedido[0]} inexistente')
        
        #verificar se está ocupada
        elif self.mesas[pedido[0]] != ' ocupada':
            print(f'erro >> mesa {pedido[0]} desocupada')
        
        #verificar se o item existe
        elif pedido[1].strip(' ') not in self.cardapio:
            print(f'erro >> item{pedido[1]} nao existe no cardapio')
        
        #verificar se os ingredientes sao suficientes 
        elif len(self.estoque) == 0:
            print(f'erro >> ingredientes insuficientes para produzir o item {pedido[1]}')  

        else:
            print(f'sucesso >> pedido realizado: item{pedido[1]} para mesa {pedido[0]}')
            ingredientes_pedido = self.cardapio[pedido[1].strip(' ')]
            if len(self.estoque) != 0:
                for elemento in ingredientes_pedido:
                    self.estoque[elemento.strip(' ')] -= 1
                    if self.estoque[elemento.strip(' ')] == 0:
                        self.estoque.pop(elemento.strip(' '))  
            self.pedidos.append(pedido)
        #fazer alteraçoes para essas quatro condiç~pes estejam relacionadas
                
    def relatorio_pedidos(self):
        aux = self.pedidos[:]
        if len(aux) == 0:
            print('- nenhum pedido foi realizado')
        else:               
            aux.sort()
            for pedido in aux:
                print(f'mesa: {pedido[0]}')
                print(f'-{pedido[1]}')

    def fechar_restaurante(self):
        if len(self.pedidos) == 0:
            print('- historico vazio')
        else:
            for x in range(len(self.pedidos)):
                print(f'{x+1}. mesa {self.pedidos[x][0]} pediu{self.pedidos[x][1]}')
        print('=> restaurante fechado')

Myrestaurant = restaurant()
entradas = []
while True:
    try:
        entradas.append(input())
    except:
        break

print('=> restaurante aberto')
for x in range(len(entradas)):
    if entradas[x] == '+ atualizar mesas':
        Myrestaurant.atualizar_mesas()

    elif entradas[x] == '+ atualizar cardapio':
        Myrestaurant.atualizar_cardapio()
    
    elif entradas[x] == '+ atualizar estoque':
        Myrestaurant.atualizar_estoque()
    
    elif entradas[x] == '+ relatorio mesas':
        Myrestaurant.relatorio_mesas()
    
    elif entradas[x] == '+ relatorio cardapio':
        Myrestaurant.relatorio_cardapio()

    elif entradas[x] == '+ relatorio estoque':
        Myrestaurant.relatorio_estoque()
    
    elif entradas[x] == '+ fazer pedido':
        Myrestaurant.fazer_pedidos()
    
    elif entradas[x] == '+ relatorio pedidos':
        Myrestaurant.relatorio_pedidos()
        
    elif entradas[x] == '+ fechar restaurante':
        Myrestaurant.fechar_restaurante()

    elif entradas[x][0] == '+':
        print('erro >> comando inexistente')
    else:
        pass
