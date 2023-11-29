# Ejudje
These tasks are for BMSTU students </br> </br>

Task №1 </br>
На стандартном потоке ввода задаётся последовательность целых чисел.
Каждое число последовательности не меньше -200 000 000 и не больше 200 000 000.
На стандартный поток вывода напечатайте сумму этих чисел. https://github.com/Dogifu/Ejudje/blob/main/sum_1.py  </br> </br>

Task №2 </br>
Реализуйте дек (двустороннюю очередь), используя только массив. https://github.com/Dogifu/Ejudje/blob/main/dequeue_2.py </br> </br>


Task №3 </br>
Реализуйте вывод всех путей до уязвимых библиотек для проекта. https://github.com/Dogifu/Ejudje/blob/main/graph_3.py </br> </br>


Task №4 </br>
Реализуйте косое дерево (splay tree).
Реализация самой структуры данных должна быть инкапуслирована, т.е. не зависеть от форматов входных/выходных данных и непосредственно ввода/вывода.
Тесты предполагают "левостороннюю" реализацию, т.е. если действие можно реализовать двумя симметричными способами, надо делать тот, который больше использует левую сторону. https://github.com/Dogifu/Ejudje/blob/main/Splay_tree_4.py </br> </br>

Task №5 </br>
Реализуйте двоичную min-кучу. Модифицируйте ее таким образом, чтобы внутреннее ее строение было таким же, но при этом доступ по ключу к любому элементу осуществлялся в среднем за константное время.
Реализация самой структуры данных должна быть инкапуслирована, т.е. не зависеть от форматов входных/выходных данных и непосредственно ввода/вывода. https://github.com/Dogifu/Ejudje/blob/main/heap_tree_5.py </br> </br>


Task №6 </br>
Реализуйте программу, которая предлагает варианты замены слова, в котором допущена одна ошибка.
Для решения этой задачи реализуйте сжатое префиксное дерево.
Регистр букв для программы коррекции не имеет значения (слова в словаре хранятся в нижнем регистре).
Варианты ошибок - как в алгоритме Дамерау-Левенштейна: вставка лишнего символа, удаление символа, замена символа или транспозиция соседних символов.
Реализация алгоритма должна быть инкапсулирована. В комментариях напишите сложность ключевых алгоритмов с пояснением.
Обход детей узла можно и нужно реализовать в среднем за время, линейно зависящее от длины подходящего префикса. Соответственно, проверка наличия слова в префиксном дереве — это в среднем линейная операция, зависящая только от длины слова. https://github.com/Dogifu/Ejudje/blob/main/autocorrection_6.py  </br> </br>


Task №7 </br> 
Реализуйте алгоритм, который на основе истории неуспешных попыток логина пользователя в систему блокирует ему доступ.
Пользователь блокируется на некоторый период времени B в случае нескольких неуспешных попыток входа N в течение определенного интервала времени P.
Блокировка начинается сразу после последней неудачной попытки логина.
В случае, если пользователь уже был недавно заблокирован, то время повторной блокировки удваивается за каждую блокировку, т.е. растет экспоненциально. При этом время блокировки ограничено сверху некоторым периодом B_max.
При расчете учитываются все попытки за период 2*B_max.
В примере ниже если пользователь совершит 5 неуспешных попыток в течение часа, то он должен быть заблокирован на 2 часа. Если после окончания блока он еще раз не сможет залогиниться за 5 попыток в течение часа, то он будет заблокирован уже на 4 часа, потом на 8 и т.д., но не более чем на 30 дней.
В комментариях к программе напишите асимптотическую сложность алгоритма и использование памяти с пояснениями, как вы их рассчитали. https://github.com/Dogifu/Ejudje/blob/main/block_7.cpp  </br> </br>


Task №8 </br>
Реализуйте фильтр Блума, позволяющий дать быстрый, но вероятностный ответ, присутствует ли объект в коллекции.
Реализация самой структуры данных должна быть инкапуслирована, т.е. не зависеть от форматов входных/выходных данных и непосредственно ввода/вывода.
Реализация битового массива также должна быть инкапсулирована. Массив битов должен быть эффективно расположен в памяти.
Параметрами структуры данных являются n - приблизительное количество элементов (целое), P - вероятность ложноположительного ответа.
Размер структуры, m, вычисляется как -n log2 P / ln 2, а количество хэш-функций - как -log2 P. Оба значения округляются до ближайшего целого.
В качестве семейства функций используйте семейство хэш-функций вида
hi(x) = (((i + 1)*x + pi+1) mod M) mod m,
где - x - ключ, i - номер хэш-функции, i∈[0; k-1], pj - j-тое по счету простое число, а M - 31ое число Мерсенна. https://github.com/Dogifu/Ejudje/blob/main/bloom_8.py </br> </br>


Task №9 </br>
Решите задачу о рюкзаке приближенно. Алгоритм должен быть инкапсулирован. https://github.com/Dogifu/Ejudje/blob/main/knapsack_9.py </br>


