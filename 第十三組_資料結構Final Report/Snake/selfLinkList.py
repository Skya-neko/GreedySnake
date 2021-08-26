# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 21:52:42 2020

@author: Vivian
"""
class Node():
    def  __init__(self, data = None):
        self.data = data
        self.next = None
        
        
        
class SingleLinkList:
    def __init__(self):
        self.pointer = None
        self.headNode = None
        self.count = 0
        

    def append(self, data):
        node = Node(data)
        if self.pointer:
            self.pointer.next = node
            self.pointer = node
        else:
            self.pointer = node
            self.headNode = node
        self.count += 1
            
    def iterate_item(self):
        current_pointer = self.headNode
        while current_pointer:
            val = current_pointer.data
            current_pointer = current_pointer.next
            yield val
            
            
    def iterate_item_end(self, endIndex):
        current_pointer = self.headNode
        for i in range(endIndex):
            val = current_pointer.data
            current_pointer = current_pointer.next
            yield val
        
            
    def __getitem__(self, index):
        if index > self.count -1 :
            return "index out of range"
        current_pointer = self.headNode
        for i in range(index):
            current_pointer = current_pointer.next
        return current_pointer.data
            
    def delete_item(self, data):
        current_pointer = self.headNode
        previous_pointer = self.headNode 
        while  current_pointer:
            if current_pointer.data == data:
                if current_pointer == self.headNode:
                    self.headNode = current_pointer.next
                else:
                    current_pointer = current_pointer.next
                    previous_pointer.next = current_pointer
                self.count -= 1
                return
            previous_pointer = current_pointer
            current_pointer = current_pointer.next
    
            
            
    
            
            
            
# listo = SingleLinkList()
# print(listo)
# listo.append("哈囉")
# listo.append("你好嗎")
# listo.append("衷心感謝")



# for val in listo.iterate_item():
#     print(val)

# print('1234654154613')
# print(listo[2])

# listo.delete_item(listo[1])
# for val in listo.iterate_item():
#     print(val)