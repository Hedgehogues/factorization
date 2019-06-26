"""
This module factorize price of payment operation by collection prices and return all solves.

We implemented some alg:
* brute force and duplicates
* factorisation with bin search with single solves (not added)


# Для доклада:
# Идея с удельным весом и жадным алгоритмом


Бизнес-задача.
В одной из внешних систем хранятся платёжные операции по отправлениям заказов. В данном кейсе нас будет интересовать
стоимость отправлений. Отправление -- это неделимый объект, который состоит из объектов поменьше. Во внутренней системе
о платёжной операции хранится расширенная информация: стоимость всей операции и стоимость частей целого.
случае это

Постановка задачи. Пус

# Этапы развития алгоритма:
Первое, что приходит в голову -- это полный перебор. Как осуществить такой перебор.
# Брутфорс (нет отсечений, много повторений)
# Задача о рюкзаке
# Оптимизация до поиска ответа с конца
# Построение генератора
# Попытка построения нерекурсивного генератора
# Идея с поиском в отсортированном массиве
# Идея с бинарным поиском
# Идея с суммой
# Идея с предпосчётом суммы
# Оптимизация: взять предпоследний
# Удельная сумма

http://acm.mipt.ru/twiki/bin/view/Curriculum/FIVTLecturesTerm1Lecture6
http://www.cyberforum.ru/cpp-beginners/thread342773.html
https://neerc.ifmo.ru/wiki/index.php?title=%D0%9D%D0%B0%D1%85%D0%BE%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5_%D0%BA%D0%BE%D0%BB%D0%B8%D1%87%D0%B5%D1%81%D1%82%D0%B2%D0%B0_%D1%80%D0%B0%D0%B7%D0%B1%D0%B8%D0%B5%D0%BD%D0%B8%D0%B9_%D1%87%D0%B8%D1%81%D0%BB%D0%B0_%D0%BD%D0%B0_%D1%81%D0%BB%D0%B0%D0%B3%D0%B0%D0%B5%D0%BC%D1%8B%D0%B5
https://www.mccme.ru/free-books/dubna/smirnov-asm.pdf
http://studlab.com/news/razbienie_chisla_na_slagaemye/2013-09-02-1003
http://problems.ru/view_problem_details_new.php?id=34899
https://pro-prof.com/forums/topic/number_compositions
http://www.programmersforum.ru/showthread.php?t=85056


brute force example:

def decompose(s, x):
    if s <= 0 or not x:
        return
    for i, item in enumerate(x):
        if s - item == 0:
            yield [item]
        for v in decompose(s - item, x[:i] + x[i + 1:]):
            yield [item] + v


x = sorted([1, 1, 2, 2, 2, 3, 5, 7, 8, 10, 10, 15, 20, 24, 25])
s = 22

variants = decompose(s, x)
res = set()
for v in variants:
    # print(v, sum(v) == s)
    res.add(tuple(sorted(v)))
print(sorted(list(res)))
print(len(list(res)))


"""