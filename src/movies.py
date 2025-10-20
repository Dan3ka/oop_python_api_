from collections import Counter

class Movies:
    """ Analyzing data from movies.csv """
    def __init__(self, path_to_the_file):
        with open(path_to_the_file, 'r') as f:
            f.readline()
            self.data_movies = []
            for line in f:
                if '"' not in line:
                    fields = [part.strip() for part in line.split(',')]
                    self.data_movies.append(fields)
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
                    fields = [part.strip() for part in add_line.split('@')]
                    self.data_movies.append(fields)

    def _exctract_year(self, title):
        if '(' in title and ')' in title:
            year_str = title[-5:-1]
            if year_str.isdigit():
                return int(year_str)
        return None
        
    def dist_by_release(self):
        """ The method returns a dict or an OrderedDict where the keys are years and the values are counts. """
        release_years = [self._exctract_year(line[1]) for line in self.data_movies]
        return dict(sorted(Counter(release_years).items(), key=lambda x: x[1], reverse=True))
    
    def dist_by_genres(self):
        """ The method returns a dict where the keys are genres and the values are counts. """
        genres = []
        for line in self.data_movies:
            for genre in line[2].split('|'):
                genres.append(genre)
        return dict(sorted(Counter(genres).items(), key=lambda x: x[1], reverse=True))
        
    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and 
        the values are the number of genres of the movie.
        """
        movies = {line[1] : len(line[2].split('|')) for line in self.data_movies}
        return dict(sorted(movies.items(), key=lambda x: x[1], reverse=True)[:n])
    
    def genre_combinations(self, n):
        """
        Возвращает топ-n самых популярных комбинаций жанров
        Ключи - комбинации жанров, значения - количество фильмов
        """
        combinations = {}
        for line in self.data_movies:
            genres = line[2].split('|')
            if len(genres) > 1:
                genre_combo = ' + '.join(sorted(genres))
                combinations[genre_combo] = combinations.get(genre_combo, 0) + 1
        
        return dict(sorted(combinations.items(), key=lambda x: x[1], reverse=True)[:n])
    
    def movies_by_decade(self):
        """
        Возвращает словарь с распределением фильмов по десятилетиям
        Ключи - десятилетия (например, "1990s"), значения - количество фильмов
        """
        decades = {}
        for line in self.data_movies:
            year = self._exctract_year(line[1])
            if year:
                decade = f"{year // 10 * 10}s"
                decades[decade] = decades.get(decade, 0) + 1
        
        return dict(sorted(decades.items(), key=lambda x: x[1], reverse=True))