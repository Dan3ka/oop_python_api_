import pytest
from movies import Movies
from ratings import Ratings
from tags import Tags
from links import Links
from decimal import Decimal
import timeit


@pytest.fixture
def movies_object():
    movies = Movies('data files/movies.csv')
    yield movies
    movies = None

@pytest.fixture
def ratings_object():
    ratings = Ratings('data files/ratings.csv','data files/movies.csv')
    yield ratings
    ratings = None

@pytest.fixture
def tags_object():
    tags = Tags('data files/tags.csv')
    yield tags
    tags = None

@pytest.fixture
def links_object():
    links=Links('data files/links.csv', 'data files/movies.csv')
    yield links
    links=None

class Tests:
    
    def test_movies_dist_by_release_returns_dict(self, movies_object):
        """проверяем, что метод возвращает словарь (dict)/"""
        res = movies_object.dist_by_release()
        assert isinstance(res, dict)

    def test_movies_dist_by_release_is_sorted(self, movies_object):
        """проверяем, что значения отсортированы по убыванию."""
        res = list(movies_object.dist_by_release().values())
        assert res == sorted(res, reverse=True)
        

    def test_movies_dist_by_release_keys_are_int(self, movies_object):
        """проверяем, что все ключи (годы) являются целыми числами (int)."""
        release_years = movies_object.dist_by_release().keys()
        new_res=[]

        for key in release_years:
            if key==None:
                pass
            else:
                new_res.append(key)
        assert all(isinstance(res, int)for res in new_res)
        

    def test_movies_dist_by_release_values_are_int(self, movies_object):
        """проверяем, что все значения (количество фильмов) являются целыми числами (int)."""
        counts = movies_object.dist_by_release().values()
        assert all(isinstance(value, int) for value in counts)



    "тесты функции dist_by_genres"
    def test_movies_dist_by_genres_returns_dict(self, movies_object):
        """проверяем, что метод возвращает словарь (dict)."""
        res=movies_object.dist_by_genres()
        assert isinstance(res, dict)

    def test_movies_dist_by_genres_is_sorted(self, movies_object):
        """проверяем, что ключи-годы отсортированы по убыванию."""
        res=list(movies_object.dist_by_genres().values())

        assert res==sorted(res, reverse=True)
    
    def test_movies_dist_by_genres_keys_are_str(self, movies_object):
        """проверяем, что все ключи (жанры) являются строками(str)."""
        keys=movies_object.dist_by_genres().keys()
        assert all(isinstance(my_key, str) for my_key in keys)

    def test_movies_dist_by_genres_values_are_int(self, movies_object):
        """проверяем, что все значения являются целыми числами (int)."""
        values=movies_object.dist_by_genres().values()
        assert all(isinstance(my_value, int) for my_value in values)


    "тесты функции most_genres"
    def test_movie_most_genres_returns_dict(self, movies_object):
        """проверяем, что метод возвращает словарь (dict)."""
        res=movies_object.most_genres(10)
        assert isinstance(res, dict)

    def test_movie_most_genres_is_sorted(self, movies_object):
        """проверяем, что ключи-годы отсортированы по убыванию."""
        res=list(movies_object.most_genres(10).values())
        assert res==sorted(res, reverse=True)
    
    def test_movies_most_genres_keys_are_str(self, movies_object):
        """проверяем, что все ключи (жанры) являются строками(str)."""
        keys=movies_object.most_genres(10).keys()
        assert all(isinstance(my_key, str) for my_key in keys)

    def test_movies_most_genres_values_are_int(self, movies_object):
        """проверяем, что все значения являются целыми числами (int)."""
        values=movies_object.most_genres(10).values()
        assert all(isinstance(my_value, int) for my_value in values)

    def test_movies_most_genres_len_is_correct(self, movies_object):
        """проверяем, что длина списка действительно имеет велечину заданного числа"""
        res=movies_object.most_genres(10)
        assert len(res)==10
    


    """
    
    
    НОВЫЙ СКРИПТ
    
    
    
    """

    """Тесты для raitings.py"""
    def test_cl_movies_dist_by_year_returns_dict(self,ratings_object):
        """проверяем, что функция возвращает словарь"""
        movies_analyzer = Ratings.Movies(ratings_object)
        result=movies_analyzer.dist_by_year()
        assert isinstance(result, dict)

    def test_cl_movies_dist_by_year_is_sorted(self, ratings_object):
        """проверяем, отсортированность по ключам-годам"""
        movies_analyzer = Ratings.Movies(ratings_object)
        result=list(movies_analyzer.dist_by_year().keys())
        assert result==sorted(result)

    def test_cl_movies_dist_by_year_keys_are_int(self, ratings_object):
        """проверяем что вссе ключи являются числами"""
        movies_analyzer = Ratings.Movies(ratings_object)
        keys=movies_analyzer.dist_by_year().keys()
        assert all(isinstance(key, int) for key in keys)
    
    def test_cl_movies_dist_by_year_values_are_int(self, ratings_object):
        """проверям, что всем занчения числа """
        movies_analyzer = Ratings.Movies(ratings_object)
        values=movies_analyzer.dist_by_year().values()
        assert all(isinstance(val, int) for val in values)


    

    """тесты для dist_by_rating"""
    def test_cl_movies_dist_by_rating_returns_dict(self, ratings_object):
        """проверяем, что функция возвращает словарь"""
        movies_analyzer = Ratings.Movies(ratings_object)
        
        result = movies_analyzer.dist_by_rating()
        assert isinstance(result, dict)

    def test_cl_movies_dist_by_ratings_is_sorted(self, ratings_object):
        """проверяем, что словарь отсортирован по ключам"""
        movies_analyzer = Ratings.Movies(ratings_object)
        result = list(movies_analyzer.dist_by_rating().keys())
        assert result == sorted(result)

    def test_cl_movies_dist_by_ratings_keys_are_float(self, ratings_object): 
        """проверяем, что все ключи (рейтинги) - числа с плавающей точкой"""
        movies_analyzer = Ratings.Movies(ratings_object)
        keys = movies_analyzer.dist_by_rating().keys()
        assert all(isinstance(k, float) for k in keys)

    def test_cl_movies_dist_by_ratings_values_are_int(self, ratings_object):
        """проверяем, что все значения (количество) - целые числа"""
        movies_analyzer = Ratings.Movies(ratings_object)
        values = movies_analyzer.dist_by_rating().values()
        assert all(isinstance(v, int) for v in values)


    """тесты для top_by_num_of_ratings"""
    def test_cl_movies_top_by_num_of_ratings_returns_dict(self, ratings_object):
        """проверяем что возрващается словарь"""
        movies_analyzer = Ratings.Movies(ratings_object)
        result = movies_analyzer.top_by_num_of_ratings(10)
        assert isinstance(result, dict)

    def test_cl_movies_top_by_num_of_ratings_is_sorted(self, ratings_object):
        """проверяем, что отсортировано по убыванию по значениям"""
        movies_analyzer = Ratings.Movies(ratings_object)
        result = list(movies_analyzer.top_by_num_of_ratings(10).values())
        assert result == sorted(result, reverse=True)

    def test_cl_movies_top_by_num_of_ratings_keys_are_str(self, ratings_object):
        """проверям, что ключи(названия фильмов) являются строками"""
        movies_analyzer = Ratings.Movies(ratings_object)
        result = list(movies_analyzer.top_by_num_of_ratings(10).keys())
        assert all(isinstance(res, str) for res in result)

    def test_cl_movies_top_by_num_of_ratings_values_are_int(self, ratings_object):
        """проверям, что значения (количество оценок) являются целыми числами"""
        movies_analyzer = Ratings.Movies(ratings_object)
        result = list(movies_analyzer.top_by_num_of_ratings(10).values())
        assert all(isinstance(res, int) for res in result)

    def test_cl_movies_top_by_num_of_ratings_len_is_correct(self, ratings_object):
        """проверям, что длина корректна"""
        movies_analyzer = Ratings.Movies(ratings_object)
        result = movies_analyzer.top_by_num_of_ratings(10)
        assert len(result) == 10

    
    """Тесты для top_by_ratings"""
    def test_cl_movies_top_by_rating_returns_dict(self,ratings_object):
        """проверям, возвращается словарь"""
        movies_analyzer = Ratings.Movies(ratings_object)
        result=movies_analyzer.top_by_ratings(10,metric='average')
        assert isinstance(result, dict)

    def test_cl_movies_top_by_rating_is_sorted(self,ratings_object):
        """проверяем, что отсортировано по убыванию"""
        movies_analyzer = Ratings.Movies(ratings_object)
        result=list(movies_analyzer.top_by_ratings(10,metric='average').values())
        assert result==sorted(result, reverse=True)
    
    def test_cl_movies_top_by_rating_keys_are_str(self,ratings_object):
        """проверяем, что ключи( навзания фильмов) строки"""
        movies_analyzer = Ratings.Movies(ratings_object)
        result=movies_analyzer.top_by_ratings(10,metric='average').keys()
        assert all(isinstance(k,str) for k in result)

    def test_cl_movies_top_by_rating_values_are_float(self,ratings_object):
        """проверяем, что ключи( навзания фильмов) строки"""
        movies_analyzer = Ratings.Movies(ratings_object)
        result=movies_analyzer.top_by_ratings(10,metric='average').values()
        assert all(isinstance(v,float) for v in result)

    def test_cl_movies_top_by_rating_values_two_signs_after(self,ratings_object):
        """проверяем, что все числа содерадт два знака после запятой"""
        movies_analyzer = Ratings.Movies(ratings_object)
        result=movies_analyzer.top_by_ratings(10,metric='average').values()
        assert all(v==round(v,2) for v in result)




    """Тесты для top_controversial"""
    def test_cl_movies_top_controversial_returns_dict(self, ratings_object):
        """поверяем, что возвращается словарь"""
        movies_analyzer = Ratings.Movies(ratings_object)
        result=movies_analyzer.top_controversial(10)
        assert isinstance(result, dict)

    def test_cl_movies_top_controversial_is_sorted(self, ratings_object):
        """проверяем, отсортированность словарая по значениям в порядке убывания"""
        movies_analyzer = Ratings.Movies(ratings_object)
        result=list(movies_analyzer.top_controversial(10).values())
        assert result==sorted(result, reverse=True)

    def test_cl_movies_top_controversial_keys_are_str(self, ratings_object):
        """поверяем, что ключи строки"""
        movies_analyzer = Ratings.Movies(ratings_object)
        result=movies_analyzer.top_controversial(10).keys()
        assert all(isinstance(k, str) for k in result)

    def test_cl_movies_top_controversial_values_are_float(self, ratings_object):
        """поверяем, что знаечния числа"""
        movies_analyzer = Ratings.Movies(ratings_object)
        result=movies_analyzer.top_controversial(10).values()
        assert all(isinstance(v, float) for v in result)
    
    def test_cl_movies_top_controversial_two_signs_after(self, ratings_object):
        """поверяем, что два знака после запятой"""
        movies_analyzer = Ratings.Movies(ratings_object)
        result=movies_analyzer.top_controversial(10).values()
        assert all(r==round(r,2) for r in result)



    """тестирование подкласса Users"""


    """Тесты для метода dist_by_num_of_user_ratings"""
    def test_users_dist_by_num_of_user_ratings_returns_dict(self, ratings_object):
        """проверяем, что метод возвращает словарь."""
        users_analyzer = Ratings.Users(ratings_object)
        result = users_analyzer.dist_by_num_of_user_ratings()
        assert isinstance(result, dict)

    def test_users_dist_by_num_of_user_ratings_keys_are_int(self, ratings_object):
        """проверяем, что ключи (userId) являются целыми числами."""
        users_analyzer = Ratings.Users(ratings_object)
        keys = users_analyzer.dist_by_num_of_user_ratings().keys()
        assert all(isinstance(key, int) for key in keys)

    def test_users_dist_by_num_of_user_ratings_values_are_int(self, ratings_object):
        """проверяем, что значения (количество оценок) являются целыми числами."""
        users_analyzer = Ratings.Users(ratings_object)
        values = users_analyzer.dist_by_num_of_user_ratings().values()
        assert all(isinstance(value, int) for value in values)


    """Тесты для метода dist_by_user_ratings"""
    def test_users_dist_by_user_ratings_returns_dict(self, ratings_object):
        """проверяем, что метод возвращает словарь."""
        users_analyzer = Ratings.Users(ratings_object)
        result = users_analyzer.dist_by_user_ratings(metric='average')
        assert isinstance(result, dict)

    def test_users_dist_by_user_ratings_keys_are_int(self, ratings_object):
        """проверяем, что ключи (userId) являются целыми числами."""
        users_analyzer = Ratings.Users(ratings_object)
        keys = users_analyzer.dist_by_user_ratings().keys()
        assert all(isinstance(key, int) for key in keys)

    def test_users_dist_by_user_ratings_values_are_numeric(self, ratings_object):
        """проверяем, что значения (средние оценки) являются числами (int или float)."""
        users_analyzer = Ratings.Users(ratings_object)
        values = users_analyzer.dist_by_user_ratings(metric='average').values()
        assert all(isinstance(value, (int, float)) for value in values)
        
    def test_users_dist_by_user_ratings_values_are_rounded(self, ratings_object):
        """проверяем, что у значений не более двух знаков после запятой."""
        users_analyzer = Ratings.Users(ratings_object)
        values = users_analyzer.dist_by_user_ratings(metric='average').values()
        for val in values:
            str_val = str(val)
            if '.' in str_val:
                decimal_part = str_val.split('.')[1]
                assert len(decimal_part) <= 2


    """Тесты для метода top_controversial"""
    def test_users_top_controversial_returns_dict(self, ratings_object):
        """проверяем, что метод возвращает словарь."""
        users_analyzer = Ratings.Users(ratings_object)
        result = users_analyzer.top_controversial(10)
        assert isinstance(result, dict)

    def test_users_top_controversial_is_sorted(self, ratings_object):
        """проверяем, что словарь отсортирован по значениям (дисперсии) по убыванию."""
        users_analyzer = Ratings.Users(ratings_object)
        values = list(users_analyzer.top_controversial(10).values())
        assert values == sorted(values, reverse=True)

    def test_users_top_controversial_len_is_correct(self, ratings_object):
        """проверяем, что возвращается правильное количество (n) пользователей."""
        users_analyzer = Ratings.Users(ratings_object)
        n = 10
        result = users_analyzer.top_controversial(n)
        assert len(result) == n

    def test_users_top_controversial_keys_are_int(self, ratings_object):
        """проверяем, что ключи (userId) являются целыми числами."""
        users_analyzer = Ratings.Users(ratings_object)
        keys = users_analyzer.top_controversial(10).keys()
        assert all(isinstance(key, int) for key in keys)

    def test_users_top_controversial_values_are_numeric(self, ratings_object):
        """проверяем, что значения (дисперсии) являются числами (int или float)."""
        users_analyzer = Ratings.Users(ratings_object)
        values = users_analyzer.top_controversial(10).values()
        assert all(isinstance(value, (int, float)) for value in values)

    def test_users_top_controversial_values_are_rounded(self, ratings_object):
        """проверяем, что у значений (дисперсий) не более двух знаков после запятой."""
        users_analyzer = Ratings.Users(ratings_object)
        values = users_analyzer.top_controversial(10).values()
        for val in values:
            str_val = str(val)
            if '.' in str_val:
                decimal_part = str_val.split('.')[1]
                assert len(decimal_part) <= 2
    
    def test_users_top_contraversial_len_correct(self, ratings_object):
        users_analyzer = Ratings.Users(ratings_object)
        res = users_analyzer.top_controversial(10)
        assert len(res)==10


    """
    
    Тесты для скрипта tags.py


    """
    """тесты для most_words"""

    def test_tags_most_words_return_dict(self, tags_object):
        """"""
        result=tags_object.most_words(10)
        assert isinstance(result, dict)

    def test_tags_most_words_is_sorted(self, tags_object):
        """"""
        result=list(tags_object.most_words(10).values())
        assert result==sorted(result, reverse=True)

    def test_tags_most_words_keys_are_str(self, tags_object):
        """"""
        result=tags_object.most_words(10).keys()
        assert all(isinstance(r, str) for r in result)
     
    def test_tags_most_words_values_are_int(self, tags_object):
        """"""
        result=tags_object.most_words(10).values()
        assert all(isinstance(r, int) for r in result)
    
    def test_tags_most_words_len_correct(self, tags_object):
        result=tags_object.most_words(10)
        assert len(result)==10


    """тесты для longest"""
    def test_tags_longest_returns_list(self, tags_object):
        """проверяем, что метод возвращает список."""
        result = tags_object.longest(10)
        assert isinstance(result, list)

    def test_tags_longest_elements_are_str(self, tags_object):
        """проверяем, что все элементы списка (теги) являются строками."""
        result = tags_object.longest(10)
        assert all(isinstance(tag, str) for tag in result)

    def test_tags_longest_is_sorted(self, tags_object):
        """проверяем, что список отсортирован по длине тега по убыванию."""
        result = tags_object.longest(10)
        lengths = [len(tag) for tag in result]
        assert lengths == sorted(lengths, reverse=True)
    
    def test_tags_longest_len_correct(self, tags_object):
        """проверяем что длина равно заданному числу"""
        result=tags_object.longest(10)
        assert len(result)==10



    """тесты для метода most_words_and_longest"""
    def test_tags_most_words_and_longest_returns_list(self, tags_object):
        """проверяем, что метод возвращает список."""
        result = tags_object.most_words_and_longest(10)
        assert isinstance(result, list)

    def test_tags_most_words_and_longest_elements_are_str(self, tags_object):
        """проверяем, что все элементы списка (теги) являются строками."""
        result = tags_object.most_words_and_longest(10)
        assert all(isinstance(tag, str) for tag in result)

    def test_tags_most_words_and_longest_is_sorted(self, tags_object):
        """проверяем, что список отсортирован по длине тега по убыванию."""
        result = tags_object.most_words_and_longest(10)
        lengths = [len(tag) for tag in result]
        assert lengths == sorted(lengths, reverse=True)

    def test_tags_most_words_and_longest_no_duplicates(self, tags_object):
        """проверяем, что в списке только уникальные значения"""
        result= tags_object.most_words_and_longest(10)
        assert len(result)==len(set(result))




    """тесты для метода most_popular"""
    def test_tags_most_popular_returns_dict(self, tags_object):
        """проверяем, что метод возвращает словарь."""
        result = tags_object.most_popular(10)
        assert isinstance(result, dict)

    def test_tags_most_popular_keys_are_str(self, tags_object):
        """проверяем, что ключи (теги) являются строками."""
        keys = tags_object.most_popular(10).keys()
        assert all(isinstance(key, str) for key in keys)

    def test_tags_most_popular_values_are_int(self, tags_object):
        """проверяем, что значения (частота) являются целыми числами."""
        values = tags_object.most_popular(10).values()
        assert all(isinstance(value, int) for value in values)

    def test_tags_most_popular_is_sorted(self, tags_object):
        """проверяем, что словарь отсортирован по значениям (частоте) по убыванию."""
        values = list(tags_object.most_popular(10).values())
        assert values == sorted(values, reverse=True)

    def test_tags_most_popular_len_correct(self, tags_object):
        """проверяем что длина равно заданному числу"""
        result=tags_object.most_popular(10)
        assert len(result)==10

    



    """тесты для метода tags_with"""
    def test_tags_tags_with_returns_list(self, tags_object):
        """проверяем, что метод возвращает список."""
        result = tags_object.tags_with("adventure")
        assert isinstance(result, list)

    def test_tags_tags_with_elements_are_str(self, tags_object):
        """проверяем, что все элементы списка (теги) являются строками."""
        result = tags_object.tags_with("adventure")
        assert all(isinstance(tag, str) for tag in result)

    def test_tags_tags_with_is_sorted(self, tags_object):
        """проверяем, что список отсортирован по алфавиту."""
        result = tags_object.tags_with("adventure")
        assert result == sorted(result)

    def test_tags_tags_with_no_duplicates(self, tags_object):
        """проверяем, что в списке только уникальные значения"""
        result= tags_object.tags_with("adventure")
        assert len(result)==len(set(result))
    """
    ТЕСТЫ ДЛЯ СКРИПТА links.py
    """
    


    """тесты для get_imdb"""
    def test_links_get_imdb_is_sorted(self, links_object):
        links_object.movies_id_cut = [356, 318]
        
        movie_ids_to_test = [356, 318]
        list_of_fields = ['Director', 'Budget']
        result = links_object.get_imdb(movie_ids_to_test, list_of_fields)
        expected_result = [
            [356, 'Robert Zemeckis', '$55,000,000 (estimated)'],
            [318, 'Frank Darabont', '$25,000,000 (estimated)']
        ]
        assert result == expected_result

    def test_links_get_imdb_returns_correct_data_types(self, links_object):
        links_object.movies_id_cut = [356, 318]
        movie_ids_to_test = [356, 318]
        list_of_fields = ['Director', 'Budget']
        
        result = links_object.get_imdb(movie_ids_to_test, list_of_fields)
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(row, list) for row in result)
        assert isinstance(result[0][0], int) # movieId
        assert isinstance(result[0][1], str) # Director
        assert isinstance(result[0][2], str) # Budget




    """тесты для top_directors"""
    def test_links_top_directors_returns_dict(self, links_object):
        """проверяем, что метод возвращает словарь."""
        links_object.movies_id_cut = [356, 318]
        result = links_object.top_directors(2)
        assert isinstance(result, dict)

    def test_links_top_directors_data_types_are_correct(self, links_object):
        """проверяем типы ключей (str) и значений (int)."""
        links_object.movies_id_cut = [356, 318]
        result = links_object.top_directors(2)
        assert all(isinstance(key, str) for key in result.keys())
        assert all(isinstance(value, int) for value in result.values())

    def test_links_top_directors_is_sorted(self, links_object):
        """проверяем, что результат отсортирован по количеству фильмов."""
        links_object.movies_id_cut = [356, 1] 
        result = links_object.top_directors(2)
        values = list(result.values())
        assert values == sorted(values, reverse=True)


    """тесты для most_expensive"""
    def test_links_most_expensive_returns_dict(self, links_object):
        """проверяем, что метод возвращает словарь."""
        links_object.movies_id_cut = [356]
        result = links_object.most_expensive(1)
        assert isinstance(result, dict)

    def test_links_most_expensive_data_is_correct(self, links_object):
        """проверяем типы и конкретное значение для известного фильма."""
        links_object.movies_id_cut = [356]
        result = links_object.most_expensive(1)
        expected_title = 'Forrest Gump (1994)'
        expected_budget = '$55,000,000'
        
        assert expected_title in result
        assert result[expected_title] == expected_budget
        assert isinstance(list(result.keys())[0], str)
        assert isinstance(list(result.values())[0], str)


    """тесты для most_profitable"""
    def test_links_most_profitable_returns_dict(self, links_object):
        """проверяем, что метод возвращает словарь."""
        links_object.movies_id_cut = [356]
        result = links_object.most_profitable(1)
        assert isinstance(result, dict)

    def test_links_most_profitable_data_is_correct(self, links_object):
        """проверяем типы и конкретное значение для известного фильма."""
        links_object.movies_id_cut = [356]
        result = links_object.most_profitable(1)
        expected_title = 'Forrest Gump (1994)'
        #прибыль = $678,226,465 - $55,000,000 = $623,226,465
        expected_profit = '$623,226,465'
        
        assert expected_title in result
        assert result[expected_title] == expected_profit


    """тесты для longest"""
    def test_links_longest_returns_dict(self, links_object):
        """проверяем, что метод возвращает словарь."""
        links_object.movies_id_cut = [318]
        result = links_object.longest(1)
        assert isinstance(result, dict)

    def test_links_longest_data_is_correct(self, links_object):
        """проверяем типы и конкретное значение для известного фильма."""
        links_object.movies_id_cut = [318]
        result = links_object.longest(1)
        expected_title = "Shawshank Redemption, The (1994)"
        expected_runtime = '2h 22m'
        
        assert expected_title in result
        assert result[expected_title] == expected_runtime
        assert isinstance(list(result.keys())[0], str)
        assert isinstance(list(result.values())[0], str)
        

    """тесты для top_cost_per_minute"""
    def test_links_top_cost_per_minute_returns_dict(self, links_object):
        """проверяем, что метод возвращает словарь."""
        links_object.movies_id_cut = [356]
        result = links_object.top_cost_per_minute(1)
        assert isinstance(result, dict)

    def test_links_top_cost_per_minute_data_is_correct(self, links_object):
        """проверяем типы и конкретное значение для известного фильма."""
        links_object.movies_id_cut = [356]
        result = links_object.top_cost_per_minute(1)
        expected_title = 'Forrest Gump (1994)'
        # Стоимость = 55,000,000 / (2*60 + 22) = 55,000,000 / 142 ≈ 387323.94
        expected_cost = '387323.94'
        
        assert expected_title in result
        assert result[expected_title] == expected_cost

        """Additional tests for ratings"""


        """тесты для метода get_tags_by_word_count"""
    def test_tags_get_tags_by_word_count_returns_list(self, tags_object):
        """проверяем, что метод возвращает список."""
        result = tags_object.get_tags_by_word_count(1)
        assert isinstance(result, list)

    def test_tags_get_tags_by_word_count_elements_are_str(self, tags_object):
        """проверяем, что все элементы списка (теги) являются строками."""
        result = tags_object.get_tags_by_word_count(2)
        if result:
            assert all(isinstance(tag, str) for tag in result)

    def test_tags_get_tags_by_word_count_is_sorted(self, tags_object):
        """проверяем, что список отсортирован по алфавиту."""
        result = tags_object.get_tags_by_word_count(3)
        assert result == sorted(result)


    """тесты для метода get_tags_stats"""
    def test_tags_get_tags_stats_returns_dict(self, tags_object):
        """проверяем, что метод возвращает словарь."""
        result = tags_object.get_tags_stats()
        assert isinstance(result, dict)

    def test_tags_get_tags_stats_elements_are_correct_types(self, tags_object):
        """проверяем, что ключи - строки, а значения - числа."""
        result = tags_object.get_tags_stats()
        assert all(isinstance(key, str) for key in result.keys())
        assert all(isinstance(value, (int, float)) for value in result.values())

    



    """тесты для метода most_active_users"""
    def test_users_most_active_users_returns_dict(self, ratings_object):
        """проверяем, что метод возвращает словарь."""
        users_analyzer = Ratings.Users(ratings_object)
        result = users_analyzer.most_active_users(10)
        assert isinstance(result, dict)

    def test_users_most_active_users_data_types_are_correct(self, ratings_object):
        """проверяем, что ключи - int (userId), а значения - int (количество)."""
        users_analyzer = Ratings.Users(ratings_object)
        result = users_analyzer.most_active_users(10)
        assert all(isinstance(key, int) for key in result.keys())
        assert all(isinstance(value, int) for value in result.values())

    def test_users_most_active_users_is_sorted(self, ratings_object):
        """проверяем, что словарь отсортирован по значениям (количеству) по убыванию."""
        users_analyzer = Ratings.Users(ratings_object)
        values = list(users_analyzer.most_active_users(10).values())
        assert values == sorted(values, reverse=True)


    """тесты для метода best_movie_of_the_year"""
    def test_movies_best_movie_of_the_year_returns_tuple(self, ratings_object):
        """проверяем, что метод возвращает кортеж."""
        movies_analyzer = Ratings.Users(ratings_object)
        result = movies_analyzer.best_movie_of_the_year(1995)
        assert isinstance(result, tuple)

    def test_movies_best_movie_of_the_year_data_types_are_correct(self, ratings_object):
        """проверяем, что в кортеже лежат строка (название) и число (рейтинг)."""
        movies_analyzer = Ratings.Users(ratings_object)
        result = movies_analyzer.best_movie_of_the_year(1995)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert isinstance(result[1], (int, float))


    """Links"""
    """тесты для метода best_opening_weekend"""
    def test_links_best_opening_weekend_returns_dict(self, links_object):
        """проверяем, что метод возвращает словарь."""
        result = links_object.best_opening_weekend(10)
        assert isinstance(result, dict)

    def test_links_best_opening_weekend_is_sorted(self, links_object):
        """проверяем, что словарь отсортирован по сборам по убыванию."""
        result = links_object.best_opening_weekend(10)
        values = list(result.values())
        numeric_values = [int(v.replace('$', '').replace(',', '')) for v in values]
        assert numeric_values == sorted(numeric_values, reverse=True)

    def test_links_best_opening_weekend_keys_are_str(self, links_object):
        """проверяем, что ключи (названия фильмов) являются строками."""
        result = links_object.best_opening_weekend(10)
        assert all(isinstance(key, str) for key in result.keys())

    def test_links_best_opening_weekend_values_are_str(self, links_object):
        """проверяем, что значения (сборы) являются строками (из-за форматирования)."""
        result = links_object.best_opening_weekend(10)
        assert all(isinstance(value, str) for value in result.values())

    def test_links_best_opening_weekend_len_correct(self, links_object):
        """проверяем, что длина словаря не превышает n."""
        n = 10
        result = links_object.best_opening_weekend(n)
        assert len(result) <= n




    """тесты для метода top_countries"""
    def test_links_top_countries_returns_dict(self, links_object):
        """проверяем, что метод возвращает словарь."""
        result = links_object.top_countries(10)
        assert isinstance(result, dict)

    def test_links_top_countries_is_sorted(self, links_object):
        """проверяем, что словарь отсортирован по количеству фильмов по убыванию."""
        result = links_object.top_countries(10)
        values = list(result.values())
        assert values == sorted(values, reverse=True)

    def test_links_top_countries_keys_are_str(self, links_object):
        """проверяем, что ключи (страны) являются строками."""
        result = links_object.top_countries(10)
        assert all(isinstance(key, str) for key in result.keys())

    def test_links_top_countries_values_are_int(self, links_object):
        """проверяем, что значения (количество фильмов) являются целыми числами."""
        result = links_object.top_countries(10)
        assert all(isinstance(value, int) for value in result.values())

    def test_links_top_countries_len_correct(self, links_object):
        """проверяем, что длина словаря не превышает n."""
        n = 10
        result = links_object.top_countries(n)
        assert len(result) <= n

        




    """Movies"""

    """тесты для метода genre_combinations"""
    def test_movies_genre_combinations_returns_dict(self, movies_object):
        """проверяем, что метод возвращает словарь."""
        result = movies_object.genre_combinations(10)
        assert isinstance(result, dict)

    def test_movies_genre_combinations_is_sorted(self, movies_object):
        """проверяем, что словарь отсортирован по количеству (значениям) по убыванию."""
        result = movies_object.genre_combinations(10)
        values = list(result.values())
        assert values == sorted(values, reverse=True)

    def test_movies_genre_combinations_keys_are_str(self, movies_object):
        """проверяем, что ключи (комбинации жанров) являются строками."""
        result = movies_object.genre_combinations(10)
        assert all(isinstance(key, str) for key in result.keys())

    def test_movies_genre_combinations_values_are_int(self, movies_object):
        """проверяем, что значения (количество) являются целыми числами."""
        result = movies_object.genre_combinations(10)
        assert all(isinstance(value, int) for value in result.values())

    def test_movies_genre_combinations_len_correct(self, movies_object):
        """проверяем, что длина словаря равна n."""
        n = 10
        result = movies_object.genre_combinations(n)
        assert len(result) <= n


    """тесты для метода movies_by_decade"""
    def test_movies_movies_by_decade_returns_dict(self, movies_object):
        """проверяем, что метод возвращает словарь."""
        result = movies_object.movies_by_decade()
        assert isinstance(result, dict)

    def test_movies_movies_by_decade_is_sorted(self, movies_object):
        """проверяем, что словарь отсортирован по количеству фильмов (значениям) по убыванию."""
        result = movies_object.movies_by_decade()
        values = list(result.values())
        assert values == sorted(values, reverse=True)

    def test_movies_movies_by_decade_keys_are_str(self, movies_object):
        """проверяем, что ключи (десятилетия) являются строками."""
        result = movies_object.movies_by_decade()
        assert all(isinstance(key, str) for key in result.keys())

    def test_movies_movies_by_decade_values_are_int(self, movies_object):
        """проверяем, что значения (количество фильмов) являются целыми числами."""
        result = movies_object.movies_by_decade()
        assert all(isinstance(value, int) for value in result.values())