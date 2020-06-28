#!/usr/bin/env python3

import os
import sys
import re
import spacy
import warnings

#-----------------------------------
# DETALHES POEMA

def numEstrofesVersos(poema):
    estrofes = 0
    versos = 0
    for est in re.split('\n\n+', poema):
        estrofes +=1
    for ver in re.split('\n+', poema):
        versos +=1
    return estrofes, versos

def tipoEstrofes(poema):
    tipos = dict()
    estrofe = 1
    for est in re.split('\n\n+', poema):
        n_versos = 0
        for ver in re.split('\n', est):            
            n_versos += 1
     
        if n_versos == 1:
            tipos[estrofe] = 'Monóstico'
        elif n_versos == 2:
            tipos[estrofe] = 'Dístico'
        elif n_versos == 3:
            tipos[estrofe] = 'Terceto'
        elif n_versos == 4:
            tipos[estrofe] = 'Quadra'
        elif n_versos == 5:
            tipos[estrofe] = 'Quintilha'
        elif n_versos == 6:
            tipos[estrofe] = 'Sextilha'
        elif n_versos == 7:
            tipos[estrofe] = 'Septilha'
        elif n_versos == 8:
            tipos[estrofe] = 'Oitava'
        elif n_versos == 9:
            tipos[estrofe] = 'Nona'
        elif n_versos == 10:
            tipos[estrofe] = 'Décima'
        else:
            tipos[estrofe] = 'Irregular'
        
        estrofe += 1
    return tipos

#-----------------------------------
# RIMAS

def rima(p1,p2):
    count = 0
    flag = 1
    for c,d in zip(reversed(p1),reversed(p2)):
        if(c==d and flag == 1):
            count+=1
        else:
            flag = 0
    if(count >= 2):
        return 1
    else:
        return 0

def tiposRima(poema,nlp):
    poema = re.sub(r'[^\w\s]','',poema)
    count = 1
    rimas = dict()

    for est in re.split('\n\n+', poema):
        pals = []
        for ver in re.split('\n', est):
            ver = nlp(ver)
            tokens = ver.text.split()
            pals.append(tokens[-1])
        
        if(len(pals) == 4):
            if(rima(pals[0],pals[2]) and rima(pals[1],pals[3])):
                rimas[count] = 'Cruzada'
            elif(rima(pals[0],pals[3]) and rima(pals[1],pals[2])):
                rimas[count] = 'Interpolada'
            elif(rima(pals[0],pals[1]) and rima(pals[2],pals[3])):
                rimas[count] = 'Emparelhada'
            else:
                rimas[count] = 'Versos Soltos'
        count +=1
    return rimas

#-----------------------------------
# ALITERAÇOES

def vogal(char):
    char = char.lower()
    if char in "aeiou":
        return True
    else:
        return False

def aliteracao(line):
    line = re.sub(r'[^\w\s]','',line)
    occur = dict()
    words = line.split()
    for word in words:
        letter = word[0].lower()
        if(len(word)==1 or len(word)==2 or vogal(letter)):
            continue
        elif(occur.get(letter)==None):
            occur[letter] = 1
        else:
            occur[letter] += 1
    key, value = max(occur.items(), key = lambda k: k[1])
    return key, value

def verifyAlit(poema):
    alit = dict()
    count = 1
    for est in re.split('\n\n+', poema):
        for ver in re.split('\n', est):
            letra, occur = aliteracao(ver)
            if(occur >= 3):
                verso = (letra, ver)
                alit[count] = verso
            count += 1
    return alit

#-----------------------------------
# ASSONANCIAS

def assonancia(line):
    line = re.sub(r'[^\w\s]','',line)
    occur = dict()
    words = line.split()
    for word in words:
        if(len(word)==1 or len(word)==2):
            continue
        for c in word:
            if(vogal(c.lower()) and occur.get(c.lower())==None):
                occur[c.lower()] = 1
            elif(vogal(c.lower())):
                occur[c.lower()] += 1
    key, value = max(occur.items(), key = lambda k: k[1])
    return key, value

def verifyAsson(poema):
    asson = dict()
    count = 1
    for est in re.split('\n\n+', poema):
        for ver in re.split('\n', est):
            letra, occur = assonancia(ver)
            if(occur >= 5):
                verso = (letra, ver)
                asson[count] = verso
            count += 1
    return asson

#-------------------------------------
# CLASSES GRAMATICAIS

def classes(poema, nlp):
    poema = nlp(poema)
    verbs = set()
    adj = set()
    adv = set()
    nomes = set()

    for token in poema:
        if(token.pos_ == "NOUN"):
            nomes.add(token.orth_.lower())
        elif(token.pos_ == "ADV"):
            adv.add(token.orth_.lower())
        elif(token.pos_ == "ADJ"):
            adj.add(token.orth_.lower())
        elif(token.pos_ == "VERB"):
            # Infinitivo
            verbs.add(token.lemma_.lower())
    return nomes, verbs, adj, adv

#-------------------------------------
# FAMILIAS SEMANTICAS

def semantica(poema, nlp):
    doc = nlp(poema)
    tokens = [token for token in doc if not token.is_punct]
    
    family = dict()
    for t in tokens:
        for n in tokens:
            if(str(t).lower()!=str(n).lower() and len(str(t))>=3 and len(str(n))>=3 and t.similarity(n) >= 0.50):
                if(family.get(str(t).lower())==None):
                    family[str(t).lower()] = [str(n).lower()]
                else:
                    entrys = family.get(str(t).lower())
                    entrys.append(str(n).lower())
                    entrys = list(set(entrys))
                    family[str(t).lower()] = entrys
    return family
#-------------------------------------
# MAIN

def main():
    warnings.filterwarnings("ignore")
    nlp = spacy.load('pt')
    with open(sys.argv[1], 'r') as f:
        name = f.name.split("/")[1].split(".")[0]
        readme = open(name+".md",'w')
        file = f.read()

        autor = re.findall('AUTOR:(.*)', file)[0]
        titulo = re.findall('TITULO:(.*)', file)[0]
        poema = re.search(r'POEMA:\n*(.*)$', file, re.DOTALL).group(1)       

        noEstrofes, noVersos = numEstrofesVersos(poema)
        tiposEst = tipoEstrofes(poema)
        rimas = tiposRima(poema, nlp)
        alit = verifyAlit(poema)
        asson = verifyAsson(poema)
        nomes, verbs, adj, adv = classes(poema, nlp)
        family = semantica(poema, nlp)

        #------------------------------------------------------------------------
        # Write info file
        readme.write("#" + titulo)
        readme.write("\n### Autor:" + autor)
        for est in re.split('\n\n+', poema):
            for ver in re.split('\n', est):
                readme.write("\n"+ver+"  ")
            readme.write("\n\n")
        readme.write("\n\n## Detalhes")
        readme.write("\n### Nº Estrofes: " + str(noEstrofes))
        readme.write("\n### Nº Versos: " + str(noVersos))
        readme.write("\n### Tipos de Estrofes")
        readme.write("\nTipos de estrofes quanto ao número de versos:\n")
        for t in tiposEst:
            readme.write("\n**Estrofe " + str(t) + " -** " + str(tiposEst[t])+"  ")
        readme.write("\n## Esquema de Rimas  ")
        if(bool(rimas)):
            for r in rimas:
                readme.write("\n**Estrofe " + str(r) + " -** " + str(rimas[r])+"  ")
        else:
            readme.write("\nEste poema não contém um esquema de rimas em nenhuma das suas estrofes.")
        readme.write("\n## Aliterações")
        if(bool(alit)):
            for a in alit:
                readme.write("\n**Verso " + str(a) + " -** \"" + str(alit[a][1]) + "\" - Letra **"+ str(alit[a][0]) +"**  ")
        else:
            readme.write("\nEste poema não contém nenhuma aliteração nos seus versos.")
        readme.write("\n## Assonâncias")
        if(bool(asson)):
            for a in asson:
                readme.write("\n**Verso " + str(a) + " -** \"" + str(asson[a][1]) + "\" - Letra **"+ str(asson[a][0]) +"**  ")
        else:
            readme.write("\nEste poema não contém nenhuma assonação nos seus versos.")
        readme.write("\n## Classes Gramaticais")
        readme.write("\n\n|   |   |")
        readme.write("\n|---|---|")
        readme.write("\n| **Substantivos** | ")
        for n in nomes:
            readme.write(n+"; ")
        readme.write("|")
        readme.write("\n| **Advérbios**    | ")
        for a in adv:
            readme.write(a+"; ")
        readme.write("|")
        readme.write("\n| **Adjetivos**    | ")
        for a in adj:
            readme.write(a+"; ")
        readme.write("|")
        readme.write("\n| **Verbos**       | ")
        for v in verbs:
            readme.write(v+"; ")
        readme.write("|")
        readme.write("\n## Famílias Semânticas")
        readme.write("\n\n|   |   |")
        readme.write("\n|---|---|")
        for w in family:  
            readme.write("\n| **"+w+"**    | ")
            for e in family[w]:
                readme.write(e + "; ")
            readme.write("|")
        
    readme.close()

    print("\nProcessamento ocorreu com sucesso!")
    print("Nome do documento -> " + readme.name + "\n")


if __name__ == "__main__":
    main()