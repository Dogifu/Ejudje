import sys

# Узел дерева


class Node:
    def __init__(self, string, nodes=None):
        self.str = string
        self.nodes = nodes if nodes is not None else []


class Radix_Tree:
    def __init__(self):
        self._root = None

    """
    Если переданный индекс находится за пределами длины строки родительского узла, 
    функция завершается, так как разделение не требуется.
    Иначе функция извлекает суффикс от индекса до конца строки родительского узла.
    Создается новый узел (child_node), используя извлеченный суффикс и дочерние узлы родительского узла.
    Дочерние узлы родительского узла заменяются новым узлом.
    Строка родительского узла обрезается, оставляя только префикс до индекса.
    Временная сложность:
    Временная сложность функции __split зависит от длины суффикса, 
    который обычно будет коротким. 
    Поэтому временная сложность этой операции можно считать O(1) или близкой к O(1), 
    так как операции обрезания строк и создания новых узлов обычно выполняются за постоянное время, 
    не зависящее от общей длины
    """

    def __split(self, parent_node, index):
        if index >= len(parent_node.str):
            return
        # Извлекаем суффикс от индекса до конца строки узла.
        suffix = parent_node.str[index:]

        # Создаем новый узел, используя извлеченный суффикс и дочерние узлы родительского узла.
        child_node = Node(suffix, parent_node.nodes)

        # Заменяем дочерние узлы родительского узла новым узлом.
        parent_node.nodes = [child_node]

        # Обрезаем строку родительского узла, оставляя только префикс до индекса.
        parent_node.str = parent_node.str[:index]

    # Функция __prefix используется для определения длины общего префикса двух строк.
    # В худшем случае, когда строки полностью совпадают или отличаются только в последнем символе,
    # время выполнения этой функции будет пропорционально минимальной длине строки из двух.
    # Таким образом, временная сложность функции __prefix составляет O(min(len(str1), len(str2))).
    def __prefix(self, str1, str2):
        # Возвращает длину общего префикса двух строк.
        common_prefix = 0
        for char1, char2 in zip(str1, str2):
            if char1 == char2:
                common_prefix += 1
            else:
                break
        return common_prefix

    """
    Функция __handle_common_prefix используется для обработки случая, 
    когда обнаруживается общий префикс между строкой, которую нужно добавить, 
    и строкой, уже содержащейся в дочернем узле.
    """

    def __handle_common_prefix(self, child_node, string, prefix_length):
        # Разбивает узел, если есть общий префикс.
        self.__split(child_node, prefix_length)
        # Добавляет оставшуюся часть строки в разделенный узел.
        self.add_word(string[prefix_length:], child_node)

    """
    Функция проходит по дочерним узлам текущего узла.
    Для каждого дочернего узла вычисляется длина общего префикса между 
    строкой, хранящейся в дочернем узле, и входной строкой.
    Если общий префикс охватывает всю входную строку, это означает, 
    что слово уже находится в трие, и функция завершается.
    Если есть частичный общий префикс, вызывается функция __handle_common_prefix 
    для обработки общего префикса.
    Если среди дочерних узлов не найдено общего префикса, 
    добавляется новый узел в список дочерних узлов текущего узла, 
    представляя новую ветвь для оставшейся части входной строки.
    Временная сложность:
    
    Временная сложность функции add_word зависит от количества дочерних узлов в 
    текущем узле и длины общего префикса. В худшем случае, когда общего префикса с 
    существующими дочерними узлами нет и добавляется новый узел, временная сложность 
    составляет O(k), где k - длина входной строки. 
    Это потому, что требуется добавить новый узел в список дочерних узлов.

    В среднем случае, когда есть общий префикс, временная сложность может быть 
    меньше O(k), так как она зависит от длины общего префикса.
    """

    def add_word(self, string, node):
        for child_node in node.nodes:
            # Проверяем длину общего префикса между строкой в дочернем узле и входной строкой.
            prefix_length = self.__prefix(child_node.str, string)
            if prefix_length == len(string):
                # Строка уже полностью в дереве, ничего не делаем.
                return
            if prefix_length:
                # Обрабатываем общий префикс, вызывая рекурсивно функцию __handle_common_prefix.
                self.__handle_common_prefix(child_node, string, prefix_length)
                return

        # Если не нашли общего префикса, добавляем новый узел.
        node.nodes.append(Node(string, []))

    def add_word_add(self, input_str):
        if not self._root:
            self._root = Node("", [])
        # Добавляем символ окончания строки (терминальный символ)
        str_to_insert = input_str.lower() + "$"
        self.add_word(str_to_insert, self._root)


"""
Всего 6 состояний:
1) Общее начальное состояние.
2) Начальное состояние для обработки следующих трех символов в строке.
3) Состояние для обработки случая, когда длина строки текущего узла равна 3.
4) Состояние для обработки случая, когда длина строки текущего узла равна 2.
5) Состояние для обработки случая, когда длина строки текущего узла равна 1.
6) Состояние для обработки случая, когда длина строки текущего узла равна 0.
"""


class Status:
    A, B, C, D, E, F = range(6)


class DemLevAutomaton:
    def __init__(self):
        self.suggested_strs = set()

    transition_matrix = [[[(Status.B, 0), None, None, None, None, None],
                          [(Status.B, 0), None, None, None, None, None],
                          [(Status.B, 0), None, None, None, None, None],
                          [(Status.B, 0), None, None, None, None, None],
                          [(Status.B, 0), None, None, None, None, None],
                          [(Status.B, 0), None, None, None, None, None],
                          [(Status.B, 0), None, None, None, None, None],
                          [(Status.B, 0), None, None, None, None, None]],

                         [[(Status.C, 0), None, None, None, None, None],
                          [(Status.C, 0), None, None, None, None, None],
                          [(Status.C, 0), None, None, None, None, None],
                          [(Status.C, 0), None, None, None, None, None],
                          [(Status.A, 1), (Status.B, 1),
                           (Status.B, 1), None, None, None],
                          [(Status.A, 1), (Status.B, 1),
                           (Status.B, 1), None, None, None],
                          [(Status.A, 1), (Status.B, 1),
                           (Status.B, 1), None, None, None],
                          [(Status.A, 1), (Status.B, 1), (Status.B, 1), None, None, None]],

                         [[(Status.C, 0), None, None, None, None, None],
                          [(Status.C, 0), None, None, None, None, None],
                          [(Status.F, 0), None, (Status.B, 2),
                           None, (Status.B, 2), (Status.B, 2)],
                          [(Status.F, 0), None, (Status.B, 2),
                           None, (Status.B, 2), (Status.B, 2)],
                          [(Status.A, 1), (Status.B, 1), (Status.B, 1),
                           (Status.B, 1), (Status.B, 1), (Status.C, 1)],
                          [(Status.A, 1), (Status.B, 1), (Status.B, 1),
                           (Status.B, 1), (Status.B, 1), (Status.C, 1)],
                          [(Status.A, 1), (Status.B, 1), (Status.C, 1),
                           (Status.B, 1), (Status.C, 1), (Status.C, 1)],
                          [(Status.A, 1), (Status.B, 1), (Status.C, 1), (Status.B, 1), (Status.C, 1), (Status.C, 1)]],

                         [[(Status.C, 0), None, None, None, None, None],
                          [(Status.C, 0), None, None, (Status.B, 3),
                           (Status.B, 3), (Status.B, 3)],
                          [(Status.F, 0), None, (Status.B, 2),
                           None, (Status.B, 2), (Status.B, 2)],
                          [(Status.F, 0), None, (Status.B, 2),
                           (Status.B, 3), (Status.C, 2), (Status.C, 2)],
                          [(Status.A, 1), (Status.B, 1), (Status.B, 1),
                           (Status.B, 1), (Status.B, 1), (Status.C, 1)],
                          [(Status.A, 1), (Status.B, 1), (Status.B, 1),
                           (Status.D, 1), (Status.D, 1), (Status.E, 1)],
                          [(Status.A, 1), (Status.B, 1), (Status.C, 1),
                           (Status.B, 1), (Status.C, 1), (Status.C, 1)],
                          [(Status.A, 1), (Status.B, 1), (Status.C, 1), (Status.D, 1), (Status.E, 1), (Status.E, 1)]]]

    # проверяет первые три символа подстроки (substr) на равенство с символом char.
    # Результатом функции является число от 0 до 7.

    def return_value(self, char, substr):
        return sum((4 >> i) * (char == substr[i]) for i in range(min(len(substr), 3)))

    def __findSimilarInTrie(self, tested_str, index, node, condition, heritage_str, i):
        # Случай, когда длина строки текущего нода >=3
        while i + 3 <= len((heritage_str + node.str)) and index < len(tested_str):
            indication_vector = self.return_value(
                tested_str[index], (heritage_str + node.str)[i:])
            transition = self.transition_matrix[3][indication_vector][condition]
            # Автомат отработал, перешел в нулевое состояние (конечное), означающее,
            # что слово содержит более двух ошибок
            if not transition:
                return
            condition = transition[0]
            i += transition[1]
            index += 1

        # Текущий узел является листом. Надо обработать оставшуюся строку в узле (длина 0, 1, 2)
        if not node.nodes:
            # Очевидно, если разница длин слов >1, то расстояние по Демерау Левенштейна >1
            if abs(len(heritage_str + node.str) - len(tested_str)) > 1:
                return
            while i < len((heritage_str + node.str)) and index < len(tested_str):
                indication_vector = self.return_value(
                    tested_str[index], (heritage_str + node.str)[i:])
                transition = \
                    self.transition_matrix[len(
                        (heritage_str + node.str)) - i][indication_vector][condition]
                if not transition:
                    break
                condition = transition[0]
                i += transition[1]
                index += 1

            # Проверка конечных состояний
            remaining_length = len(heritage_str + node.str) - i
            if remaining_length == 0 and condition not in [Status.A, Status.B]:
                return
            elif remaining_length == 1 and condition not in [Status.A, Status.C]:
                return
            elif remaining_length == 2 and condition not in [Status.D, Status.len_1, Status.F]:
                return

            self.suggested_strs.add(heritage_str + node.str[:-1])
            return

        for child_node in node.nodes:
            self.__findSimilarInTrie(
                tested_str, index, child_node, condition, heritage_str + node.str, i)

    def findSimilarInTrie(self, input_str, trie):
        self.suggested_strs.clear()
        str_to_search = input_str.lower() + "$"
        if trie._root:
            self.__findSimilarInTrie(
                str_to_search, 0, trie._root, Status.A, "", 0)
        return self.suggested_strs


def main():
    MyTrie = Radix_Tree()
    Automaton = DemLevAutomaton()

    line = input()
    for _ in range(int(line)):
        word = input()
        MyTrie.add_word_add(word)

    for line in sys.stdin:
        if line == "" or line == "\n":
            break

        line = line[:-1]
        suggested_strs = Automaton.findSimilarInTrie(line, MyTrie)
        if line.lower() in suggested_strs:
            print(f"{line} - ok")
        elif not suggested_strs:
            print(f"{line} -?")
        else:
            print(f"{line} -> {', '.join(sorted(suggested_strs))}")


if __name__ == "__main__":
    main()
