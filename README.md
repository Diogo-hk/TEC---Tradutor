# TEC - Tradutor

Tradutor de Modelos de Máquina de Turing

Este repositório contém um tradutor de modelos de Máquinas de Turing, desenvolvido para a disciplina de Teoria da Computação. O programa é capaz de converter programas de MT entre o modelo de fita semi-infinita (Sipser) e o modelo de fita duplamente infinita.

A sintaxe de entrada e saída é 100% compatível com o simulador online Morphett's Turing Machine Simulator.

Objetivo

O programa lê um arquivo de entrada (.in) que contém:

    Uma linha de cabeçalho (;S ou ;I) indicando o modelo da máquina.

    Uma série de transições de uma MT determinística.

Ele então produz um arquivo de saída (.out) contendo um programa de MT funcional para o modelo "oposto", capaz de reconhecer a mesma linguagem.

Requisitos

    Python 3.x

    O script foi desenvolvido e testado para ser executado em um ambiente Ubuntu 22.04.4 LTS (64 bits), conforme os requisitos do trabalho.

    Nenhuma biblioteca externa é necessária (utiliza apenas sys e os).

Execute o script: Utilize o interpretador python3, passando o nome do script e o caminho para o seu arquivo de entrada como argumento.
Bash

    python3 tecTradutor .py <caminho/para/seu/arquivo.in>

                                                     
                              ....::..                          
                          ::@@MM::..::                          
                    MM@@..::##@@mmmm--++++mmmm::::              
                mm@@##++mm--@@##--..  ::--++mm##++::..          
                mm####MM--                  --mm..##MM++        
            ++++++##@@                          --####@@mm      
          ----++mm..              ..              mmmmMMMM      
          ::::....          --mm@@@@                ..##MMMM    
        --..mm++          ..mm++mmmm..                mm++++mm  
        ++::--                  MMMM##                  mm  ++  
      mm::..--                  --....                  mm++--  
        ::..                    ++@@MM::                  --  ++
      ::::                      @@##@@MM                  ++mm::
      mm....                  mm####@@mm                  ##++--
    ..@@++--                  ++##mm##mm@@                mmMM@@
    MM##mm--                mmMM##  @@@@@@                mmmm@@
    --##MMmm              ::MM----  ++--##MM              ::::@@
      ..++##              ##++@@      MM--mm              ++mm@@
      mmmm##            ##MM@@        ::++mm              ::++mm
      @@++##          ::MM--@@        ..####MM  --        ..MM--
      ##mmMM++        ##@@++            MMmmmm::mmmm    ++@@mm--
        ++##MM          mm              ::MMMM::::::    ######  
        ++@@##--      ..--                @@mm++        mm####  
          MM@@MM--                                  ++..--MM    
            --..++--                              ##@@++::      
            ::mm  --@@                          MM##@@##++      
              ++--MM@@@@..                  ++--::mmmm::        
                  ::..++  ++mmMM::++++mm@@@@@@MM####            
                    mm    @@MMMMmm::##@@++######@@              
                        ::mmmmMM##mmmmmm####--                  
                                                            
                                                            
                                                            
                                                            
                                                            
