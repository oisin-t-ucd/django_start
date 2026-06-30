def my_func(*list_of_arguments, **dict_of_keword_arguments):
    print(list_of_arguments)
    print(dict_of_keword_arguments)


my_func(1, 2, 3, 4, extra_number=5)
