#coding=utf-8
__author__ = 'popka'

import main


class LinkContainer(object):

    links = []

    def __init__(self):
        pass

    def add(self, array):
        """
        Если не лох - переделай. Так пиздец как плохо.
        Даже страшно подумать, как это плохо!
        Возможно надо вставить сет, но проверить, что он не выстраивается по алфавиту
        :param array:
        :return:
        """
        for i in array:
            i.lower()
            flag = True
            if (not main.QUEST_SYMBOL_SUPPORTED):
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
