import numpy as np

# m is usually set to 2 and r to 0.10-0.25 times standard deviation of lista

def Sample_Entropy(lista, m, r):
    # split list in an array of vectors with length 2 and 1 number overlap
    l_with_mvectors = []
    k = 0
    lista = np.array(lista)
    for i in range(len(lista[:-m+1])):
        l_with_mvectors.append(lista[i:i + m])

    # split list in an array of vectors with length 3 and 2 numbers overlap
    l_with_mplus1vectors = []
    i = 0
    for i in range (len(lista[:-m])):
        l_with_mplus1vectors.append(lista[i:i + m + 1])

    # create an inside function to calculate sum of logs of l_with2vectors and l_with3vectors
    def sumprobs(l, vectoSz, r):

        matches = []

        for en1,vector in enumerate(l):

            countSimilar = 0
            limits = [[vector[i] + r, vector[i] - r] for i in range(vectoSz)] # position m mth value, 0 is max 1 is min
            for en2,tmp in enumerate(l):

                if en1==en2: continue

                countSimilarE = 0
                for t in range(vectoSz):

                    #upperLim = vector[t] + r
                    #lowerLim = vector[t] - r

                    #if tmp[t] >= lowerLim and tmp[t] <= upperLim:
                    if tmp[t] >= limits[t][1] and tmp[t] <= limits[t][0]:
                        countSimilarE += 1

                if countSimilarE == vectoSz:
                    countSimilar += 1

            matches.append(countSimilar)

        prob = sum(matches) / (len(l) - 1)

        AiBi = prob/ (len(lista) - m)

        return AiBi

    Bi = sumprobs(l_with_mvectors, m, r)
    Ai = sumprobs(l_with_mplus1vectors, m + 1, r)

    A = ((len(lista) - m - 1) * (len(lista) - m) * Ai) / 2
    B = ((len(lista) - m - 1) * (len(lista) - m) * Bi) / 2

    sampen = -np.log(A / B)

    return sampen
