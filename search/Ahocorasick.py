'''
本程序实现了：
AC自动机，对文章进行检索
'''

# python3
from search.utils import cut

class Node(object):
    """
    节点的抽象
    """

    def __init__(self,str='',is_root=False):
        self._next_p={}
        self.fail=None
        self.is_root=is_root
        self.str=str
        self.parent=None

    def __iter__(self):
        return iter(self._next_p.keys())

    def __getitem__(self,item):
        return self._next_p[item]

    def __setitem__(self,key,value):
        _u=self._next_p.setdefault(key,value)
        _u.parent=self

    def __repr__(self):
        return "<Node object '%s' at %s>"%\
               (self.str,object.__repr__(self)[1:-1].split('at')[-1])

    def __str__(self):
        return self.__repr__()


class AhoCorasick(object):
    """
    Ac自动机对象
    """
    def __init__(self,words):
        self.words_set=set(words)
        self.words=list(self.words_set)
        self.words.sort(key=lambda x:len(x))
        self._root=Node(is_root=True)
        self._node_meta={}
        self._node_all=[(0,self._root)]
        _a={}
        self.num={} #储存着每个单词的出现日志数目
        self.isin = 1 #判定是否完成了全覆盖
        self.hit_num = 0
        for word in self.words:
            self.num[word] = 0
            for w in word:
                _a.setdefault(w,set())
                _a[w].add(word)

        def node_append(keyword):
            assert len(keyword)>0
            _=self._root
            for _i,k in enumerate(keyword):
                node=Node(k)
                if k in _:
                    pass
                else:
                    _[k]=node
                    self._node_all.append((_i+1,_[k]))
                self._node_meta.setdefault(id(_[k]),set())
                if _i>=1:
                    for _j in _a[k]:
                        if keyword[:_i+1].endswith(_j):
                            self._node_meta[id(_[k])].add((_j,len(_j)))
                _=_[k]
            else:
                if _!=self._root:
                    self._node_meta[id(_)].add((keyword,len(keyword)))

        for word in self.words:
            node_append(word)
        self._node_all.sort(key=lambda x:x[0])
        self._make()

    def _make(self):
        """
        构造Ac树
        :return:
        """
        for _level,node in self._node_all:
            if node==self._root or _level<=1:
                node.fail=self._root
            else:
                _node=node.parent.fail
                while True:
                    if node.str in _node:
                        node.fail=_node[node.str]
                        break
                    else:
                        if _node==self._root:
                            node.fail=self._root
                            break
                        else:
                            _node=_node.fail
    def search(self,content,with_index=False):
        result=set()
        node=self._root
        index=0
        for i in content:
            while 1:
                if i not in node:
                    if node==self._root:
                        break
                    else:
                        node=node.fail
                else:
                    for keyword,keyword_len in self._node_meta.get(id(node[i]),set()):
                        if not with_index:
                            result.add(keyword)
                        else:
                            self.num[keyword] += 1
                    node=node[i]
                    break
            index+=1
        for i in self.num.values():
            self.isin = self.isin and bool(i)
            self.hit_num += i
        return result

    def clear(self):#清除字典里面的记录
        for i in self.num.keys():
            self.num[i] = 0
if __name__=='__main__':
    ac=AhoCorasick(["天文台"])
    ac.search("你好世界，我在这里，你好世界,中国天文台",True)
    print(ac.num)
    print(ac.isin)
    print(ac.hit_num)