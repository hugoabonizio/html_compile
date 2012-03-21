import sys

EXTENSION = 'hugo'

class Compiler:
    tags, code, compiled = [], '', ''

    def parser(self):
        lines = self.code.split('\n')

        tags = []
        temp = ''

        #itera linha
        for line in lines:

            i = 0
            aux = 0
            lastTag = ''
            isString = False
            isID = False
            isClass = False
            
            #itera caractere
            for c in line:
                #abre tag no primeiro caractere da linha
                #if i == 0:
                #    temp += '<'

                if isString:
                    if c != '\"':
                        temp += c
                    else:
                        isString = False
                        
                elif isID:
                    aux += 1
                    if aux == 1:               #variavel auxiliar pra contar dentro do nome id
                        lastTag += ' id=\"' + c
                    elif c == ' ' or c == '{':
                        lastTag += '\"'
                        isID = False
                        aux = 0
                    else:
                        lastTag += c
                    
                elif isClass:
                    aux += 1
                    if aux == 1:
                        lastTag += ' class=\"' + c
                    elif c == ' ' or c == '{':
                        lastTag += '\"'
                        isClass = False
                        aux = 0
                    elif c == '.':                 #se tiver mais um ponto (ex: .primeiraClasse.segundaClasse) adiciona as duas como classe
                        lastTag += ' '
                    else:
                        lastTag += c
                    
                else:
                    if c == ' ' or c == '\t':
                        continue #se for espaco dentro de codigo, continua
                    
                    if c == '{':
                        tags.append(lastTag.split(' ')[0])
                        temp += '<' + lastTag + '>'
                        lastTag = ''
                    elif c == '}':
                        temp += '</' + tags.pop() + '>'
                    elif c == '\"':
                        isString = True
                    elif c == '#':
                        isID = True
                    elif c == '.':
                        isClass = True
                    else:
                        lastTag += c


                
                i += 1
                
        self.code = temp
        
        return self

    def save(self):
        fileName = (self.name).split('.' + EXTENSION)[0]
        saved = file(fileName + '.html', 'w')
        saved.write(self.code)
        saved.close()
        if saved:
            return True
        else:
            return False

    def loadCode(self, src):
        self.name = src
        self.code = file(src).read()
        return self

if __name__ == '__main__':
    src = sys.argv[1]                                 #o arquivo e passado como primeiro argumento
    if src.split('.')[-1] == EXTENSION:
        c = Compiler()
        if c.loadCode(src).parser().save():
            print 'It\'s ready!'
        else:
            print 'Something went wrong when file create was called'
    else:
        print 'File extension invalid!'
