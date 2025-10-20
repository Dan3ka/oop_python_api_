from datetime import datetime
from collections import Counter
import timeit

class Ratings:
    """
    Analyzing data from ratings.csv
    """
    def __init__(self, path_to_the_file_ratings, path_to_the_file_movies):
        """
        Put here any fields that you think you will need.
        """
        with open(path_to_the_file_ratings, 'r') as f:
            f.readline()
            self.data_ratings = [line.strip().split(',') for line in f]

        with open(path_to_the_file_movies, 'r', encoding='utf-8') as f:
            f.readline()
            self.movie_titles = {}
            for line in f:
                if '"' not in line:
                    parts = [part.strip() for part in line.split(',')]
                else:
                    add_line = ''
                    inside_quotes = False
                    for char in line:
                        if char == '"':
                            inside_quotes = not inside_quotes
                        elif char == ',' and not inside_quotes:
                            add_line += '@'
                        else:
                            add_line += char
                    parts = [part.strip() for part in add_line.split('@')]
                self.movie_titles[int(parts[0])] = parts[1]
                
    class Movies:
        def __init__(self, parent):
            self.parent = parent

        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts. 
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
            years = [datetime.fromtimestamp(int(line[3])).year for line in self.parent.data_ratings]
            return dict(sorted(Counter(years).items()))
        
        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
            Sort it by ratings ascendingly.
            """
            ratings = [float(line[2]) for line in self.parent.data_ratings]
            return dict(sorted(Counter(ratings).items()))
        
        def top_by_num_of_ratings(self, n):
            """
            The method returns top-n movies by the number of ratings. 
            It is a dict where the keys are movie titles and the values are numbers.
            Sort it by numbers descendingly.
            """
            movie_ids = [int(line[1]) for line in self.parent.data_ratings]
            top_movies = Counter(movie_ids).most_common(n)

            return {self.parent.movie_titles[movie_id] : count for movie_id, count in top_movies}
        
        def _get_all_ratings_by(self, index):
            ratings = {}
            for line in self.parent.data_ratings:
                if int(line[index]) in ratings:
                    ratings[int(line[index])].append(float(line[2]))
                else:
                    ratings[int(line[index])] = [float(line[2])]
            return ratings
        
        def _calc_metric(self, ratings_dict, metric = 'average'):
            """Вычисляет average или median для словаря {id: [оценки]}."""
            result = {}
            if metric == 'average':
                result = {object_id : round(sum(ratings) / len(ratings), 2) for object_id, ratings in ratings_dict.items()}
            elif metric == 'median':
                for object_id, ratings in ratings_dict.items():
                    sorted_ratings = sorted(ratings)
                    len_ = len(sorted_ratings)
                    mid = len_ // 2
                    if len_ % 2 == 0:
                        result[object_id] = round((sorted_ratings[mid - 1] + sorted_ratings[mid]) / 2, 2)
                    else:
                        result[object_id] = round(sorted_ratings[mid], 2)
            else:
                 ValueError("Metric must be 'average' or 'median'")
            return result
        
        def _calc_variance(self, ratings_dict):
            """Вычисляет дисперсию для словаря {id: [оценки]}."""
            variances = {}
            for object_id, ratings in ratings_dict.items():
                average = sum(ratings) / len(ratings)
                variances[object_id] = 0
                for rating in ratings:
                    variances[object_id] += (rating - average)**2
                variances[object_id] /= len(ratings_dict[object_id])
                variances[object_id] = round(variances[object_id], 2)
            return variances

        def top_by_ratings(self, n, metric='average'):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
            movie_ratings = self._get_all_ratings_by(1)
            metric_values = self._calc_metric(movie_ratings, metric)

            top_movies = sorted(metric_values.items(), key = lambda x: x[1], reverse=True)[:n]
            return {self.parent.movie_titles[movie_id] : value for movie_id, value in top_movies}
        
        def top_controversial(self, n):
            """
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
            Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
            movie_ratings = self._get_all_ratings_by(1)
            variances = self._calc_variance(movie_ratings)

            variances_sorted = sorted(variances.items(), key=lambda x: x[1], reverse=True)[:n]
            return {self.parent.movie_titles[movie_id] : round(var, 2) for movie_id, var in variances_sorted}

    class Users(Movies):
        """
        In this class, three methods should work. 
        The 1st returns the distribution of users by the number of ratings made by them.
        The 2nd returns the distribution of users by average or median ratings made by them.
        The 3rd returns top-n users with the biggest variance of their ratings.
        Inherit from the class Movies. Several methods are similar to the methods from it.
        """
        def dist_by_num_of_user_ratings(self):
            users_ratings = self._get_all_ratings_by(0)
            return {user_id : len(ratings) for user_id, ratings in users_ratings.items()}
        
        def dist_by_user_ratings(self, metric='average'):
            users_ratings = self._get_all_ratings_by(0)
            return self._calc_metric(users_ratings, metric)

        def top_controversial(self, n):
            users_ratings = self._get_all_ratings_by(0)
            variances = self._calc_variance(users_ratings)
            return dict(sorted(variances.items(), key=lambda x: x[1], reverse=True)[:n])


        """Additional part"""
        def most_active_users(self, n):
            """
            Returns the top-n most active users by the number of ratings they have submitted.
            """
            users_activity = self.dist_by_num_of_user_ratings()
            top_users = sorted(users_activity.items(), key=lambda item: item[1], reverse=True)[:n]
            return dict(top_users)