import requests_html
import math

class Ordbok:
    def __init__(self,filnamn):
        fil = open(filnamn)
        self.rader = [r.strip() for r in fil.readlines() if len(r) == 6]
    def get_words(self): return self.rader

def possible(word,matches,words):
    possible=[]
    for w in words:
        is_match = True
        for i,m in enumerate(matches):
            if m == 1 and w[i] == word[i]:
                continue
            if m == 2 and word[i] in w:
                continue
            if m == 0 and word[i] not in w:
                continue
            is_match = False
        if is_match:
            possible.append(w)
    return possible

def all_permutations(size,rng):
    if size==1: 
        for i in range(rng):
            yield [i]
    for perm in all_permutations(size-1,rng):
        for i in range(rng):
            yield [i]+perm

            

def all_possible(word,words):
    for perm in all_permutations(5,3):
        p=possible(word,perm,words)
        if not len(p): continue
        print("Perm: "+str(perm))
        print("Möjliga: "+str(p))
        print("Probabilitet: " + str(len(p)/len(words)))
        print("Information: " + str(math.log2(len(words)/len(p))))
        #yield possible(word,p,words)

def main():
    obok = Ordbok('./svenska-ord.txt')
    words = obok.get_words()
    all_p = all_possible('aktie',words)
    #for p in all_p:
     #   if not len(p): continue
     #   print("Möjliga: "+str(p))
    #    print("Probabilitet: " + str(len(p)/len(words)))
   #     print("Information: " + str(math.log2(len(words)/len(p))))
    
#    obok.show_rader()

if __name__ == "__main__": main()
