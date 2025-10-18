import os
import sys

# Funções para a conversão de Fita Infinita -> Sipser (I -> S)

def prepararFitaSipser(arquivoSaida):

    # Marca símbolo inicial
    arquivoSaida.write("0 0 # R sr0\n")
    arquivoSaida.write("0 1 # R sr1\n")
    arquivoSaida.write("0 _ # R mf\n")
    arquivoSaida.write("\n")
    
    # Shift Right de zeros
    arquivoSaida.write("sr0 0 0 R sr0\n")
    arquivoSaida.write("sr0 1 0 R sr1\n")
    arquivoSaida.write("sr0 _ 0 R mf\n")
    arquivoSaida.write("\n")
    
    #Shift Right de uns
    arquivoSaida.write("sr1 0 1 R sr0\n")
    arquivoSaida.write("sr1 1 1 R sr1\n")
    arquivoSaida.write("sr1 _ 1 R mf\n")
    arquivoSaida.write("\n")
    
    # Marca o fim da fita com '&'
    arquivoSaida.write("mf _ & L ini\n")
    
    # Volta o cabeçote para a célula mais à esquerda de Sipser
    arquivoSaida.write("ini 0 0 L ini\n")
    arquivoSaida.write("ini 1 1 L ini\n")
    arquivoSaida.write("ini # # R 0S\n")
    arquivoSaida.write("\n")

def gerarSubRotinaCorrecaoDeslocamento(arquivoSaida, nomeEstado):

    # Cheguei no limite da fita de Sipser e acessei um branco antes dela
    arquivoSaida.write(f"ltc_{nomeEstado} 0 _ R sr0_{nomeEstado}\n")
    arquivoSaida.write(f"ltc_{nomeEstado} 1 _ R sr1_{nomeEstado}\n")
    arquivoSaida.write(f"ltc_{nomeEstado} _ _ R sr__{nomeEstado}\n")
    arquivoSaida.write(f"ltc_{nomeEstado} & _ R srF_{nomeEstado}\n")
    
    # Shift Right de zeros
    arquivoSaida.write(f"\nsr0_{nomeEstado} 0 0 R sr0_{nomeEstado}\n")
    arquivoSaida.write(f"sr0_{nomeEstado} 1 0 R sr1_{nomeEstado}\n")
    arquivoSaida.write(f"sr0_{nomeEstado} _ 0 R sr__{nomeEstado}\n")
    arquivoSaida.write(f"sr0_{nomeEstado} & 0 R srF_{nomeEstado}\n")
    
    # Shift Right de uns
    arquivoSaida.write(f"\nsr1_{nomeEstado} 0 1 R sr0_{nomeEstado}\n")
    arquivoSaida.write(f"sr1_{nomeEstado} 1 1 R sr1_{nomeEstado}\n")
    arquivoSaida.write(f"sr1_{nomeEstado} _ 1 R sr__{nomeEstado}\n")
    arquivoSaida.write(f"sr1_{nomeEstado} & 1 R srF_{nomeEstado}\n")
    
    # Shift Right de _
    arquivoSaida.write(f"\nsr__{nomeEstado} 0 _ R sr0_{nomeEstado}\n")
    arquivoSaida.write(f"sr__{nomeEstado} 1 _ R sr1_{nomeEstado}\n")
    arquivoSaida.write(f"sr__{nomeEstado} _ _ R sr__{nomeEstado}\n")
    arquivoSaida.write(f"sr__{nomeEstado} & _ R srF_{nomeEstado}\n")
    
    # Shift Right de F (marcador final '&')
    arquivoSaida.write(f"\nsrF_{nomeEstado} _ & L ini_{nomeEstado}\n")
    
    # Corrigir o cabeçote (rebobinar)
    arquivoSaida.write(f"\nini_{nomeEstado} _ _ L ini_{nomeEstado}\n")
    arquivoSaida.write(f"ini_{nomeEstado} 0 0 L ini_{nomeEstado}\n")
    arquivoSaida.write(f"ini_{nomeEstado} 1 1 L ini_{nomeEstado}\n")
    arquivoSaida.write(f"ini_{nomeEstado} # # R {nomeEstado}S\n")
    
    # Correção da fita à direita (se bater no marcador '&')
    arquivoSaida.write(f"\nrtc_{nomeEstado} _ & L {nomeEstado}S\n")

def mapearTransicoesInfinitas(arquivoEntrada, arquivoSaida, estadosVisitados, estadosPendentes):

    for linha in arquivoEntrada.readlines():
        tokens = linha.split(" ")
        while "" in tokens:
            tokens.remove("")
        if(";" in tokens[0]):
            linha = linha.replace("\n", "")
            arquivoSaida.write(f"{linha} from Double-Infinite tape\n")
            continue
        if (linha != "\n" and tokens[0] != ";"):
            if tokens[0] not in estadosVisitados and tokens[4] not in estadosVisitados:
                estadosVisitados.append(tokens[0])
                
                # Mandar para o estado de correção da fita para esquerda e para a direita
                arquivoSaida.write(f"{tokens[0]}S # # R ltc_{tokens[0]}\n")
                arquivoSaida.write(f"{tokens[0]}S & _ R rtc_{tokens[0]}\n")
                
                if ("halt" not in tokens[4]) and ("halt-accept" not in tokens[4]):
                    estadosPendentes.append(tokens[4])
            tokens[0] = f"{tokens[0]}S"
            if ("halt" not in tokens[4]) and ("halt-accept" not in tokens[4]):
                tokens[4] = tokens[4].replace("\n", "")
                tokens[4] = f"{tokens[4]}S"
            
            direcao = tokens[3]
            if direcao == 'S':
                direcao = '*'

            arquivoSaida.write(f"{tokens[0]} {tokens[1]} {tokens[2]} {direcao} {tokens[4]}")
        if len(tokens) > 5:
            if(";" in tokens[5]):
                for i in range(5, len(tokens)):
                    tokens[i] = tokens[i].replace("\n", "")
                    arquivoSaida.write(f" {tokens[i]}")
                arquivoSaida.write(" from Double-Infinite tape")
        arquivoSaida.write("\n")

# Funções para a conversão de Sipser -> Fita Infinita (S -> I)

def prepararFitaInfinita(arquivoSaida):

    # Marca símbolo inicial
    arquivoSaida.write("0 0 # R sr0\n")
    arquivoSaida.write("0 1 # R sr1\n")
    arquivoSaida.write("0 _ # R 0I\n")
    arquivoSaida.write("\n")
    
    # Shift Right de zeros
    arquivoSaida.write("sr0 0 0 R sr0\n")
    arquivoSaida.write("sr0 1 0 R sr1\n")
    arquivoSaida.write("sr0 _ 0 L ini\n")
    arquivoSaida.write("\n")
    
    #Shift Right de uns
    arquivoSaida.write("sr1 0 1 R sr0\n")
    arquivoSaida.write("sr1 1 1 R sr1\n")
    arquivoSaida.write("sr1 _ 1 L ini\n")
    arquivoSaida.write("\n")
    
    # Volta o cabeçote para a célula mais à esquerda (a "parede")
    arquivoSaida.write("ini 0 0 L ini\n")
    arquivoSaida.write("ini 1 1 L ini\n")
    arquivoSaida.write("ini # # R 0I\n")
    arquivoSaida.write("\n")

def mapearTransicoesSipser(arquivoEntrada, arquivoSaida, estadosVisitados, estadosPendentes):
    """
    Lê as transições da máquina S e as mapeia para estados I,
    adicionando a transição de "mola" (bater na parede '#').
    """
    for linha in arquivoEntrada.readlines():
        tokens = linha.split(" ")
        while "" in tokens:
            tokens.remove("")
        if(";" in tokens[0]):
            linha = linha.replace("\n", "")
            arquivoSaida.write(f"{linha} from Sipser\n")
            continue
        if (linha != "\n" and tokens[0] != ";"):
            if tokens[0] not in estadosVisitados and tokens[4] not in estadosVisitados:
                estadosVisitados.append(tokens[0])
                
                # Transição para simular a mola (bater na parede)
                arquivoSaida.write(f"{tokens[0]}I # # R {tokens[0]}I\n")
                
                if ("halt" not in tokens[4]) and ("halt-accept" not in tokens[4]):
                    estadosPendentes.append(tokens[4])
            tokens[0] = f"{tokens[0]}I"
            if ("halt" not in tokens[4]) and ("halt-accept" not in tokens[4]):
                tokens[4] = tokens[4].replace("\n", "")
                tokens[4] = f"{tokens[4]}I"

            direcao = tokens[3]
            if direcao == 'S':
                direcao = '*'

            arquivoSaida.write(f"{tokens[0]} {tokens[1]} {tokens[2]} {direcao} {tokens[4]}")
        if len(tokens) > 5:
            if(";" in tokens[5]):
                for i in range(5, len(tokens)):
                    tokens[i] = tokens[i].replace("\n", "")
                    arquivoSaida.write(f" {tokens[i]}")
                arquivoSaida.write(" from Sipser")
        arquivoSaida.write("\n")

# Funções de Orquestração

def processarSipserParaInfinito(arquivoEntrada, arquivoSaida):

    prepararFitaInfinita(arquivoSaida)
    estadosVisitados = []
    estadosPendentes = []
    mapearTransicoesSipser(arquivoEntrada, arquivoSaida, estadosVisitados, estadosPendentes)
    
    # Gera a transição de "mola" para qualquer estado novo encontrado
    for estado in estadosPendentes:
        estado = estado.replace("\n", "")
        if estado not in estadosVisitados:
            arquivoSaida.write(f"\n{estado}I # # R {estado}I\n")

def processarInfinitoParaSipser(arquivoEntrada, arquivoSaida):

    prepararFitaSipser(arquivoSaida)
    estadosVisitados = []
    estadosPendentes = []
    mapearTransicoesInfinitas(arquivoEntrada, arquivoSaida, estadosVisitados, estadosPendentes)

    # Gera a sub-rotina de correção/deslocamento para TODOS os estados
    for estado in estadosVisitados:
        gerarSubRotinaCorrecaoDeslocamento(arquivoSaida, estado)
        
    for estado in estadosPendentes:
        estado = estado.replace("\n", "")
        if estado not in estadosVisitados:
            gerarSubRotinaCorrecaoDeslocamento(arquivoSaida, estado)

def executarConversao(): ##Principal

    if len(sys.argv) > 1 and len(sys.argv) < 3:
        caminhoArquivoEntrada = sys.argv[1]
    else:
        raise Exception("Nome do arquivo da máquina que será traduzido deve ser colocado como argumento da execução")
    
    # O nome do arquivo de saída agora é baseado no nome de entrada
    nomeBase = caminhoArquivoEntrada
    if caminhoArquivoEntrada.endswith(".in"):
        nomeBase = caminhoArquivoEntrada[:-3]
    caminhoArquivoSaida = f"{nomeBase}.out"
    
    with open(caminhoArquivoEntrada, "r") as arquivoEntrada:
        primeiraLinha = arquivoEntrada.readline()
        with open(caminhoArquivoSaida, "w+") as arquivoSaida:
            # Verificação se a formatação de comentário da primeira linha está correta
            verificacaoCabecalho = primeiraLinha.split(" ")
            verificacaoCabecalho[-1] = verificacaoCabecalho[-1].replace("\n", "")
            while "" in verificacaoCabecalho:
                verificacaoCabecalho.remove("")
            
            indicePontoVirgula = -1
            indiceModelo = -1
            
            if ";" in verificacaoCabecalho:
                indicePontoVirgula = verificacaoCabecalho.index(";")
            if "S" in verificacaoCabecalho:
                indiceModelo = verificacaoCabecalho.index("S")
            elif "I" in verificacaoCabecalho:
                indiceModelo = verificacaoCabecalho.index("I")

            if(len(verificacaoCabecalho) > 2):
                raise Exception("Primeira linha deve conter apenas ';' e 'S' ou ';' e 'I' seguidos")
            
            # Decide qual conversão executar
            if ";S" in primeiraLinha or ((indicePontoVirgula < indiceModelo) and "S" in primeiraLinha):
                print("Iniciando conversão: Sipser -> Fita Infinita")
                # Adiciona o cabeçalho ;I para a saída
                arquivoSaida.write(";I from Sipser\n") 
                processarSipserParaInfinito(arquivoEntrada, arquivoSaida)
                print(f"Conversão concluída. Arquivo salvo em: {caminhoArquivoSaida}")
        
            elif ";I" in primeiraLinha or ((indicePontoVirgula < indiceModelo) and "I" in primeiraLinha):
                print("Iniciando conversão: Fita Infinita -> Sipser")
                # Adiciona o cabeçalho ;S para a saída
                arquivoSaida.write(";S from Double-Infinite tape\n") 
                processarInfinitoParaSipser(arquivoEntrada, arquivoSaida)
                print(f"Conversão concluída. Arquivo salvo em: {caminhoArquivoSaida}")
            else:
                raise Exception("Primeira linha deve conter apenas ';' e 'S' ou ';' e 'I' seguidos")

if __name__ == "__main__":
    executarConversao()