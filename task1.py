quotes_tuples = [
    (1, 'Rick Cook', 'программирование сегодня — это гонка разработчиков программ...'),
    (2, 'Robert Martin', 'Чтобы написать чистый код, мы сначала пишем грязный код, а затем рефакторим его'),
    (3, 'Alan Kay', 'Я изобрел понятие «объектно-ориентированный», и могу заявить, что не имел в виду C++'),
    (4, 'Donald Knuth', 'Чтобы понять алгоритм, нужно его увидеть.'),
    (5, 'Donald Knuth', 'Помните, что обычно есть решение проще и быстрее того, что первым приходит вам в голову'),
    (6, 'Waldi Ravens', 'Программирование на С похоже на быстрые танцы на только...'),
    (7, 'Donald Knuth', 'Преждевременная оптимизация — корень всех зол.'),
    (8, 'Alan Kay', 'Легче изобрести будущее, чем предсказать его')
]

#
# keys = ["id", "author", "text"]
#
#
# quotes = []
# for quote in quotes_tuples:
#     quotes.append(dict(zip(keys, quote)))
#
# print(quotes)
#
# name = "Tim"
# rating = ""
# text = "програм"
#
# name_filter = ""
# rating_filter = ""
# text_filter = ""
# if len(name) == 0:
#     name_filter = f"QuoteModel.author.has.ilike(f'%{name}%')"
# if rating is not None:
#     rating_filter = f"QuoteModel.rating=={rating}"
# if text is not None:
#    text_filter = f"QuoteModel.text.ilike(f'%{text}%')"
# quotes = f"QuoteModel.query.filter({name_filter} + {rating_filter} + {text_filter})"
#
# print(quotes)


authors_dict = [
    {
        "id": 1,
        "name": "Stepan",
        "surname": None
    },
    {
        "id": 2,
        "name": "nina",
        "surname": None
    },
    {
        "id": 5,
        "name": "Rick Cook",
        "surname": None
    },
    {
        "id": 6,
        "name": "Alan J. Perlis",
        "surname": None
    },
    {
        "id": 7,
        "name": "Waldi Ravens",
        "surname": None
    },
    {
        "id": 8,
        "name": "Mosher’s Law of Software Engineering",
        "surname": None
    },
    {
        "id": 9,
        "name": "Bill Bryson",
        "surname": None
    }
]

print(sorted(authors_dict, key=lambda x: x['name']))

request = {args: {
    'name': 'Nina',
    'name2': 'Stepan',
    'surname': 'Krylov',
    'surname5': 'Polekhina',
    'age': 33}
}

other_args = set(request.args.keys()) - {'name', 'name2', 'surname', 'surname2'}: #можно настроить другие параметры, оставила для проверки ограничения
print(re)
        # if other_args is not None:
        #     return f"Use a request to view all authors", 40
