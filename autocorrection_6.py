"""
|//////////////////////////////////////////////////////////|
|Есть два подхода к решению данной задаче:                 |
|1)создаем два класса, где первый - это вершина дерева,    |
|а второй - это наше radix tree                            |
|2)реализуем отдельно словарь и radix tree                 |
|В данном решении предоставлен первый вариант реализации   |
|//////////////////////////////////////////////////////////|
"""


class RadixNode:
    def __init__(self):
        self.end_of_the_word = False  # Булевое значение конца слова
        self.children = {}  # Словарь, где ключ - это состояния переходов, а значения - вершины


class RadixTree:
    def __init__(self, words=None):
        self.root = RadixNode()
        if words is not None:
            for word in words:
                self.add_word(word)
                """
                Добавляем вершину-потомка 
                O(n), где n - мощность алфавита, но при этом
                n зависит от входных данных -> не константа
                """

    @staticmethod
    def find_prefix(word, child):
        """
        Для цикла с обратным диапозоном:
        Диапозон от min(len(word)), len(child) до 1
        В худшем случае, когда длины word и child различаются абсолютно, 
        итерацией будет минимальное из значений, то есть кол-во итераций
        цикла ограничено минимальной длиной двух строк.

        Для операция внутри цикла:
        в данной случае операция внутри цикла выполняется за константное время
        Таким образом, общая временная сложность 
        этой функции зависит от минимальной длины из двух строк
        и составляет O(min(len(word), len(child))).
        Пусть (k = min(len(word), len(child)))
        Общая временная сложность - O(k).

        """
        for index in reversed(range(1, min(len(word), len(child)) + 1)):
            if child.startswith(word[:index]):
                return word[:index]

    def biggest_prefix(self, word, childs):
        if len(word):  # Это константная сложность
            for child in childs:  # Цикл по дочерним узлам
                # количество итераций цикла ограничено числом дочерних узлов.
                if child == word[0]:
                    # вызов нашей прошлой функции
                    return self.find_prefix(word, child), child
                """
                Общая временная сложность функции зависит от 
                числа дочерних узлов и временной сложности вызова 
                _get_longest_prefix. 
                Пусть число дочерних узлов = m, а минимальная длина слова = 
                 = (k = min(len(word), len(child))) ->  O(m * k).
                """
        return '', None

    @staticmethod
    # Реализация алгоритма Дамераю - Левенштейна (Д/Л)
    def levenstein_distance(str1, str2):
        """
        Реализация алгоритма Д/Л имеет квадратичную сложность относительно длин строк (O(str1 * str2))
        Это делает его довольно неэффективным для длинных строк
        Однако, есть иное решение: автомат Левенштейна, который я, к сожалению, не в состоянии написать
        :)
        """
        matrix = {}

        def column(i, j):
            return 1 if str1[i] != str2[j] else 0

        for i in range(-1, len(str1) + 1):
            matrix[(i, -1)] = i + 1

        for j in range(-1, len(str2) + 1):
            matrix[(-1, j)] = j + 1

        for i in range(len(str1)):
            for j in range(len(str2)):
                matrix[(i, j)] = min(
                    matrix[(i - 1, j)] + 1,
                    matrix[(i, j - 1)] + 1,
                    matrix[(i - 1, j - 1)] + column(i, j),
                )

                if i and j and str1[i] == str2[j - 1] and str1[i - 1] == str2[j]:
                    matrix[(i, j)] = min(matrix[(i, j)],
                                         matrix[i - 2, j - 2] + column(i, j))
        return matrix[len(str1) - 1, len(str2) - 1]

    def add_word(self, word):
        """
        Сложность функции add_word зависит от 
        длины входного слова и структуры уже построенного дерева. 
        1) prefix, child = self._get_longest_prefix_arr(word, node.children.keys()): 
        Эта операция выполняется за O(m * k), где m - количество дочерних узлов, k - минимальная длина слова. 
        Так как, _get_longest_prefix_arr вызывает _get_longest_prefix, которая имеет подобную сложность
        2) if prefix == child: ...: Сравнение строк выполняется за O(k), где k - длина префикса.
        3) word = word[len(prefix):]: Операция среза строки выполняется за O(k), где k - длина префикса.
        4) node = node.children[prefix]: 
        Обращение к дочернему узлу по ключу также выполняется за O(1), так как это операция словаря.
        ------> Cложность функции add_word в худшем случае оценивается как O(m * k), 
        где m - количество дочерних узлов, k - минимальная длина слова. 
        """
        word = word.lower()
        node = self.root

        while word:
            prefix, child = self.biggest_prefix(
                word, node.children.keys())
            if not prefix:
                break

            if prefix == child:
                if len(word) < len(prefix):
                    node.children[prefix].end_of_the_word = True
                    return
            else:
                prefix_node = RadixNode()
                node.children[prefix] = prefix_node
                prefix_node.children[child[len(
                    prefix):]] = node.children[child]
                prefix_node.end_of_the_word = prefix == word
                del node.children[child]

            word = word[len(prefix):]
            node = node.children[prefix]

        new_node = RadixNode()
        node.children[word] = new_node
        new_node.end_of_the_word = True

    def _search(self, word):  # Функция поиска слова в дереве
        """
        Сложность данной функции — линейная, 
        O(n), где n - длина входного слова word. 
        Функция выполняет итерации по символам слова, следуя пути в дереве, 
        начиная от корня и двигаясь к соответствующим дочерним узлам. 
        Количество итераций цикла ограничено длиной входного слова.
        Докажем эту временную сложность:
        1) word[i] not in node.children: 
        Эта операция выполняется в среднем за O(1), 
        так как node.children представляет собой словарь.
        2) node = node.children[word[i]]: Также является операцией O(1), 
        так как она работает с дочерним узлом, который представлен в виде словаря.
        3) i += 1: Операция увеличения счетчика, O(1).
        4) цикл while i < len(word) имеет линейную сложность O(n), где n - длина слова (len(word))
        Таким образом, все операции внутри цикла выполняются за константное время. 
        Количество итераций цикла ограничено длиной входного слова len(word). 
        -> O(n), где n - длина входного слова word
        """
        node = self.root
        i = 0
        while i < len(word):
            if word[i] not in node.children:
                return False
            node = node.children[word[i]]
            i += 1
            # Проверяем, является ли текущий узел конечным внутри цикла
            if i == len(word) and node.end_of_the_word:
                return True
        return False

    def words_possible(self, node, index, word, prefix, status_error, possible_words):
        """
        Функция осуществляет обход дерева решений и 
        добавляет возможные замены слова во множество possible_words.
        Временная сложность функции в худшем случае: 
        O(m^n), где n - длина входного слова, 
        m - максимальное количество дочерних узлов у каждого узла в дереве.
        """

        if node.end_of_the_word:
            if index > len(word) - 1 or (index == len(word) - 1) and (not status_error or word[-1] == prefix[-1]):
                possible_words.add(prefix)

        for next_prefix, next_node in node.children.items():
            new_index = index + len(next_prefix)
            if not len(next_node.children):
                new_index = len(word)

            distance = self.levenstein_distance(
                next_prefix, word[index:new_index])
            if distance > 2:
                continue

            if distance == 2:
                for current_index in [new_index - 1, new_index + 1]:
                    distance = self.levenstein_distance(
                        next_prefix, word[index:current_index])
                    if distance <= 1:
                        new_index = current_index
                        break

                if distance > 1:
                    continue

            elif distance == 1:
                if status_error:
                    for current_index in [new_index, new_index + 1]:
                        distance = self.levenstein_distance(prefix + next_prefix,
                                                            word[:current_index])
                        if distance <= 1:
                            new_index = current_index
                            break

                    if distance > 1:
                        continue

                self.words_possible(next_node, new_index, word,
                                    prefix + next_prefix, True,
                                    possible_words)
            else:
                self.words_possible(next_node, new_index, word,
                                    prefix + next_prefix, status_error,
                                    possible_words)
                if distance == 1 and not status_error:
                    self.words_possible(next_node, new_index + 1, word,
                                        prefix + next_prefix, True,
                                        possible_words)

    # Вставка строки проверки ошибок

    def variaty(self, word):
        word = word.lower()
        if self._search(word):
            return None
        possibility = set()
        self.words_possible(self.root, 0, word, "", False, possibility)
        return list(possibility)  # Возвращаем список возможных замен слова
    # Сортируем именно в вводе


if __name__ == "__main__":
    dict_length = int(input())
    radix = RadixTree()

    for _ in range(dict_length):
        to_insert = input()
        radix.add_word(to_insert)

    while True:
        try:
            to_correct = input()
            if not len(to_correct):
                continue

            prediction = radix.variaty(to_correct)

            if prediction is None:
                print(f"{to_correct} - ok")  # Если слово полностью совпадает
            elif not prediction:
                print(f"{to_correct} -?")  # Если слово вообще не совпадает
            else:
                if to_correct in prediction:
                    print(f"{to_correct} - ok")
                else:
                    print(f"{to_correct} -> {', '.join(sorted(prediction))}")
                    # Сортируем наши возможные варианты замены в лексикографическом порядке
                    # То есть наша реализация не заточена под вывод, инкапсуляцию нарушать плохо :)

        except EOFError:
            break
