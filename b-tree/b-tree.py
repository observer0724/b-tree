from __future__ import division
from bisect import insort_left

split_count = 0
merge_count = 0
searchAccess_count = 0
insertAccess_count = 0
deleteAccess_count = 0
class node:
    def __init__(self):
        self.key = []
        self.child = []
        self.leaf = None
        self.n = None
        self.h = 0

    def height(self):
        if not self.leaf:
            return self.child[0].height()+1
        else:
            return 0

    def print_this_level(self, level):
        if level == 0:
            print "(",
            for i in range(self.n):
                print self.key[i],
                print",",
            print")",
        else:
            if level>0:
                for i in range(self.n+1):
                    self.child[i].print_this_level(level-1)

    def print_order(self, level):
        if level == 0:
            print self.n+1,
        else:
            if level>0:
                for i in range(self.n+1):
                    self.child[i].print_order(level-1)

    def print_level_order(self):
        h = self.height()
        for i in range(h+1):
            self.print_this_level(i)
        print ""
        for j in range(h+1):
            self.print_order(j)





    def split_child(self,i):
        global split_count
        global insertAccess_count
        split_count += 1
        insertAccess_count += 2
        new_child = node()
        new_child.leaf = self.child[i].leaf
        new_child.n = 1
        new_child.key.append(self.child[i].key[2])
        self.child[i].key.remove(self.child[i].key[-1])
        if not self.child[i].leaf:
            new_child.child.append(self.child[i].child[2])
            new_child.child.append(self.child[i].child[3])
            self.child[i].child.remove(self.child[i].child[-1])
            self.child[i].child.remove(self.child[i].child[-1])
        self.child[i].n = 1
        self.child.append(None)
        for j in range(self.n,i,-1):
            self.child[j+1] = self.child[j]
        self.child[i+1] = new_child
        self.key.append(None)
        for k in range(self.n,i, -1):
            self.key[j] = self.key[j-1]
        self.key[i] = self.child[i].key[1]
        self.child[i].key.remove(self.child[i].key[-1])
        self.n += 1

    def insert_nonfull(self, k):
        global insertAccess_count
        insertAccess_count += 1
        i = self.n-1
        if self.leaf:
            insort_left(self.key, k)
            self.n += 1
        else:
            while i>=0 and k<self.key[i]:
                i -= 1
            i += 1
            if self.child[i].n == 3:
                self.split_child(i)
                if k > self.key[i]:
                    i += 1
            self.child[i].insert_nonfull(k)





    def merge_node(self,i):
        global merge_count
        global deleteAccess_count
        merge_count += 1
        deleteAccess_count += 2
        self.child[i].n = 3
        self.child[i].key.append(None)
        self.child[i].key.append(None)
        self.child[i].key[2] = self.child[i+1].key[0]
        self.child[i].key[1] = self.key[i]
        if not self.child[i].leaf:
            self.child[i].child.append(None)
            self.child[i].child.append(None)
            self.child[i].child[3] = self.child[i+1].child[1]
            self.child[i].child[2] = self.child[i+1].child[0]
        for j in range(i,self.n-1):
            self.key[j] = self.key[j+1]
            self.child[j+1] = self.child[j+2]
        self.key.remove(self.key[-1])
        self.child.remove(self.child[-1])
        self.n -= 1

    def get_prede(self):
        x = self
        while not x.leaf:
            x = x.child[-1]
        return x.key[-1]

    def get_succe(self):
        x = self
        while not x.leaf:
            x = x.child[0]
        return x.key[0]

    def right_shift(self,i):
        global deleteAccess_count
        deleteAccess_count += 2
        self.child[i+1].n +=1
        j = self.child[i+1].n-1
        self.child[i+1].key.append(None)
        while j >0:
            self.child[i+1].key[j] = self.child[i+1].key[j-1]
            j -= 1
        self.child[i+1].key[0] = self.key[i]
        self.key[i] = self.child[i].key[-1]
        if not self.child[i+1].leaf:
            j = self.child[i+1].n -1
            self.child[i+1].child.append(None)
            while j >=0:
                self.child[i+1].child[j+1] = self.child[i+1].child[j]
                j -= 1
            self.child[i+1].child[0] = self.child[i].child[-1]
        self.child[i].n -= 1

    def left_shift(self,i):
        global deleteAccess_count
        deleteAccess_count += 2
        self.child[i].n += 1
        self.child[i].key.append(self.key[i])
        self.key[i] = self.child[i+1].key[0]
        self.child[i+1].n -= 1
        j = 0
        while j< self.child[i+1].n:
            self.child[i+1].key[j] = self.child[i+1].key[j+1]
            j+=1
        self.child[i+1].key.remove(self.child[i+1].key[-1])
        if not self.child[i+1].leaf:
            self.child[i].child.append(self.child[i+1].child[0])
            j = 0
            while j<self.child[i+1].n +1:
                self.child[i+1].child[j] = self.child[i+1].child[j+1]
                j += 1
            self.child[i+1].child.remove(self.child[i+1].child[-1])

    def remove_node_key(self,k):
        global deleteAccess_count
        deleteAccess_count += 1
        i = 0
        print "in node %d, n is %d,last key is %d" %(self.key[0],self.n, self.key[-1])
        while i < self.n and k > self.key[i]:
            i += 1
            print "bigger"

        print i
        if i<self.n and k == self.key[i]:
            if self.leaf:
                for j in range(i+1,self.n):
                    self.key[j-1] = self.key[j]
                self.key.remove(self.key[-1])
                self.n -= 1
                return
            else:
                if self.child[i].n > 1:
                    k_1 = self.child[i].get_prede()
                    self.child[i].remove_node_key(k_1)
                    self.key[i] = k_1
                    return
                elif self.child[i+1].n >1:
                    k_2 = self.child[i+1].get_succe()
                    self.child[i+1].remove_node_key(k_2)
                    self.key[i] = k_2
                    return
                else:
                    self.merge_node(i)
                    self.remove_node_key(k)
        else:
            if self.child[i].n == 1:
                if i>0 and self.child[i-1].n>1:
                    self.right_shift(i)
                    print "rightshift"
                else:
                    if i< self.n:
                        if self.child[i+1].n>1:
                            self.left_shift(i)
                            print "leftshift"
                    else:
                        if i>0:
                            self.merge_node(i-1)
                        else:
                            if i < self.n:
                                self.merge_node(i)
            self.child[i].remove_node_key(k)






class tree:
    def __init__(self, root):
        self.root = root

    def search(self, x, k):
        global searchAccess_count
        searchAccess_count += 1
        i = 0
        while i < x.n and k > x.key[i]:
            i += 1
        if i < x.n and k == x.key[i]:
            print "found in level %d" %(x.height()+1)
        elif x.leaf:
            print "Not found"
        else:
            self.search(x.child[i], k)




    def print_tree(self):
        h = self.root.height()
        for i in range(h+1):
            self.root.print_this_level(i)
            print ""
        print "\n"

    def print_level_order(self):
        self.root.print_level_order()



    def insert(self,k):
        global insertAccess_count

        if len(self.root.key) == 0:
            self.root.key.append(k)
            self.root.n += 1
            insertAccess_count += 1
        else:
            if self.root.n == 3:
                s = node()
                s.leaf = False
                s.n = 0
                s.child.append(self.root)
                s.split_child(0)
                s.insert_nonfull(k)
                self.root = s
                insertAccess_count += 1
            else:
                self.root.insert_nonfull(k)



    def remove_key(self,k):
        if self.root.n == 1:
            if self.root.child[0].n == 1 and self.root.child[1].n ==1:
                self.root.merge_node(0)
                self.root = self.root.child[0]
        self.root.remove_node_key(k)



a = node()
a.leaf = True
a.n = 0
t = tree(a)
insertion_times = 0
deletion_times = 0
search_times = 0

commands = raw_input("input:").split(",")
for command in commands:
    command = command.split(" ")
    while "" in command:
        command.remove("")
    print command
    if len(command) >0:
        if command[0] == "P":
            t.print_tree()
        elif command[0] == "I":
            t.insert(int(command[1]))
            insertion_times += 1
        elif command[0] == "D":
            t.remove_key(int(command[1]))
            deletion_times += 1
        elif command[0] == "L":
            t.search(t.root,int(command[1]))
            search_times += 1

print "split %d times in total, %f times on average" % (split_count, (split_count/insertion_times))
print "merge %d times in total, %f times on average" % (merge_count,(merge_count/deletion_times))
print "accessnode %d times in total, %f time on average when insertion" % (insertAccess_count,(insertAccess_count/insertion_times))
print "accessnode %d times in total, %f time on average when deletion" % (deleteAccess_count,(deleteAccess_count/deletion_times))
print "accessnode %d times in total, %f time on average when lookup" % (searchAccess_count,(searchAccess_count/search_times))