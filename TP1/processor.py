#!/usr/bin/env python3

from itertools import combinations
from graphviz import Digraph
import fileinput
import re
import hashlib


def getTexto():
    texto = ""
    for line in fileinput.input():
        texto += line
    return texto


def limpa(dictionary):
    pairsDict = {k: v for k, v in dictionary.items() if v > 9}
    return pairsDict


def entidades(texto):

    pronomes = [
        "Oh",
        "They",
        "See",
        "I",
        "You",
        "He",
        "She",
        "It",
        "What",
        "We",
        "Yes",
        "That",
        "So",
        "And",
        "There",
        "But",
        "Well",
        "No",
        "Why",
        "How",
        "The",
        "But",
        "In",
        "At",
    ]

    s = r"\s+"
    maiusc = r"(?:[A-Z]\w+(?:[-\']\w+)*|[A-Z]\.)"
    ent = f"({maiusc}(?:{s}{maiusc}|{s}{maiusc})*)"

    pairsDict = {}

    frases = texto.split("@")

    for frase in frases:
        nomes = list(dict.fromkeys(re.findall(ent, frase)))

        for pronome in pronomes:
            if pronome in nomes:
                nomes.remove(pronome)

        if nomes:
            nomes.sort()

        pairs = list(combinations(nomes, 2))

        for pair in pairs:
            if pair in pairsDict:
                i = pairsDict[pair] + 1
                pairsDict[pair] = i
            else:
                pairsDict[pair] = 1

    return pairsDict


def frases(texto):
    exp1 = r"(\n\n+\s*)([\“\"A-Z])"
    exp2 = r"([a-z][.?!]+\s*)([\“\"A-Z])"

    pageRef = r"(Page \|)(.*)"
    mr = r"(Mrs|Mr)(\.)"

    texto = re.sub(pageRef, "", texto)
    texto = re.sub(mr, r"\1", texto)

    texto = re.sub(exp1, r"\1@\2", texto)
    texto = re.sub(exp2, r"\1@\2", texto)

    return texto


def interpretador(dictionary):
    print("-------------TABLE----------------\n")
    for item, val in dictionary.items():
        print(item[0] + " - " + item[1] + " --> " + str(val))
    print("\n--------------------------------\n")

    entidade = input("Insira um nome da tabela: ")

    amigos = {}

    for item, val in dictionary.items():
        if item[0] == entidade:
            amigos[item] = val
        elif item[1] == entidade:
            amigos[item] = val

    amigos = {
        k: v for k, v in sorted(amigos.items(), key=lambda item: item[1], reverse=True)
    }

    print("\n--------------TOP5--------------\n")
    for key in list(amigos)[0:5]:
        if key[0] != entidade:
            print("--> " + key[0])
        else:
            print("--> " + key[1])
    
    print("\n--------------------------------")


def graph(dictionary):
    dot = Digraph()
    for item, val in dictionary.items():
        dot.node(item[0])
        dot.node(item[1])
        dot.edge(item[0], item[1], label=str(val))
    dot.render("grafo", view=True, format="png")


def main():
    # Construção do dicionário de combinações
    dic = limpa(entidades(frases(getTexto())))
    # Top 5 amigos
    interpretador(dic)
    # Print total combinações
    total = len(dic.items())
    print("\nTOTAL COMBINAÇÕES: " + str(total))
    print("\n--------------------------------")
    # Construção do grafo
    graph(dic)


if __name__ == "__main__":
    main()
