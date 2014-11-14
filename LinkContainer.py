#coding=utf-8
__author__ = 'popka'


class LinkContainer(object):

    links = []

    def __init__(self):
        pass

    def add(self, array):
        for i in array:
            flag = True
            if '?' in i:
                i = i[0:i.index('?')]

            for j in self.links:
                if (i==j):
                    flag = False
                    break

            if (flag == True):
                self.links.append(i)



    def get_length(self):
        return len(self.links)

    def get_all_links(self):
        '''
        Возвращает список ссылок, всегда уникальный
        '''
        return self.links

    def get_link(self, number):
        return self.links[number]
