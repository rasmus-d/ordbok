from genericpath import exists
from http.client import SWITCHING_PROTOCOLS
import sys
import time

timeload = 0
timeadd = 0
timeexists = 0
timefind = 0
timeflatten = 0

class Node:
    def __init__(self, char):#, is_word):
        self.nodes = {}
        self.char = char
        self.is_word = False#is_word
    def __str__(self):
        return self.char

class Tree:
    def __init__(self):
        self.nodes = {}
    def load_from_file(self,filename):
        global timeload
        timeload = time.perf_counter()
        for line in open(filename).readlines():
            self.add_word(list(line.lower())[0:-1]) # list() for easier handling, slice away nullbyte
        timeload = time.perf_counter() - timeload
    def _add_word(self, word, node):
        if not word:
            node.is_word=True
            return
        c = word.pop(0)
        #is_word = not word
        if c in node.nodes.keys():
            self._add_word(word,node.nodes[c])
        else:
            n = Node(c)
            node.nodes[c] = n
            self._add_word(word,n)
    def add_word(self, word):
        self._add_word(word,self)
    def _exists(self, word, node):
        if not word:
            return node.is_word
        c = word.pop(0)
        if c in node.nodes.keys():
            return self._exists(word,node.nodes[c])
        return False
    def exists(self,word):
        global timeexists
        timeexists = time.perf_counter()
        e = self._exists(word,self)
        timeexists = time.perf_counter() - timeexists
        return e
    '''
    def _star_helper(self, query, node, acc, end):
        pos = []
        for k,v in node.nodes.items():
            if k == end:
                pos.append(self._find(self,query[1:],v,acc+k))
                pass
        pass

    def _star(self, query, node, acc, end):
        if query[1] == node.char :
                return acc if node.is_word else None
        #return self._star(query,node,acc,q[1])
        pos = []
        for k,v in node.nodes.items():
            f = self._find(query,v,acc+k)
            if f is not None:
                pos.append(f)
        return pos if pos else None
    '''
        
        
    def _qmark(self, query, node, acc):
        pos = []
        for k,v in node.nodes.items():
            f = self._find(query[1:],v,acc+k)
            if f is not None:
                pos.append(f) 
        return pos if pos else None

    def _bracket():
        pass
    def _find(self, query, node, acc):
        match query:
            case []:
                return acc if node.is_word else None
            #case [c]:
            #    return acc+[node.nodes[c].char] if node.nodes[c].is_word and c in node.nodes.keys() else None
            case q:
                match q[0]:
                    case '*':
                        if q[1] == node.char :
                            return acc if node.is_word else None
                        #return self._star(query,node,acc,q[1])
                        pos = []
                        for k,v in node.nodes.items():
                            f = self._find(query,v,acc+k)
                            if f is not None:
                                pos.append(f)
                        return pos if pos else None
                    case '?':
                        return self._qmark(query, node, acc)
                    case '[':
                        pass
                    case c:
                        return self._find(query[1:],node.nodes[c],acc+c) if c in node.nodes.keys() else None
    def find(self, query):
        global timefind
        global timeflatten
        timefind = time.perf_counter()
        f = self._find(query, self, '')
        timefind = time.perf_counter() - timefind
        res = []
        timeflatten = time.perf_counter()
        flatten(f,res)
        timeflatten = time.perf_counter() - timeflatten
        return res


def flatten(l,acc):
    for el in l:
        if isinstance(el, list):
            flatten(el,acc)
        else:
            acc.append(el)

def print_node(node):
    if not node.nodes.keys():
        return
    for k in node.nodes.keys():
        print(k,end="\t")
    print("")
    for v in node.nodes.values():
        print_node(v)



def main():
    tree = Tree()
    tree.load_from_file('svenska-ord.txt')
    print(f"timeload: {timeload}")
    
    inp = None
    while inp != 'q':
        inp = input("q - quit\ne [word] - check if [word] exists\nf [query] - find all words matching [query]\n")
        match inp[0]:
            case 'q':
                pass
            case 'e':
                word = inp[2:]
                print(str(tree.exists(list(word))))
                print(f"timeexists: {timeexists}")
            case 'f':
                query = inp[2:]
                print(str(tree.find(list(query))))
                print(f"timefind: {timefind}")
                print(f"timeflatten: {timeflatten}")


if __name__ == '__main__':
    sys.exit(main())