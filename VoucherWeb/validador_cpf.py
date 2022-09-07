def validar_cpf(cpf):
    #try: 
        #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
        #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
        #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
        if int(cpf) and len(set(cpf)) != 1:  
            print("teste1 - é inteiro e os digitos são diferentes")
            num = 11
            ver_cpf = []
            d1 = 0
            d2 = 0

            for i in range(9):
                ver_cpf.append(cpf[i])
                print('teste2 - {}'.format(ver_cpf))

            for i in ver_cpf:
                num = num - 1
                d1 += (int(i)*num) #soma os valores do produto entre os 9pri digitos e o fatorial de 10

            num = 11
            d1 = 11 - (d1 % 11) #objetivo é pegar o resto da divisão
            
            if d1 > 9:
                d1 = 0

            
            print('teste2.1 - {}'.format(ver_cpf))
            ver_cpf.append(str(d1))
            
            print('teste3 primeiro if - {}'.format(ver_cpf))
            

            for i in ver_cpf:
                d2 += (int(i)*num)
                num = num - 1
            print("teste4 - segundo for")

            d2 = 11 - (d2 % 11)

            if d2 > 9:
                d2 = 0

            ver_cpf.append(str(d2))
            cpf_novo = "".join(ver_cpf)
            print("teste5 - segundo if. Este ver_cpf{} é igual a este cpf{}".format(cpf_novo,cpf))
            
            if cpf == cpf_novo:
                print("teste6 - cpf valido")
                return True
        else:
            print("Teste 7 - nao inteiro ou os digitos sao iguais")
            return False
    #except:
        print('O CPF informado não é valido. Digite somente numeros.')
        return False



cpf = '05701540499'
validar_cpf(cpf)
