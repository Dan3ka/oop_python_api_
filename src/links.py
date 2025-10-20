import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

class Links:
    """ Analyzing data from links.csv """
    def __init__(self, path_to_the_file_links, path_to_the_file_movies):
        with open(path_to_the_file_links, 'r') as f:
            self.data_links = {}
            f.readline()
            for line in f:
                items = line.strip().split(',')
                if items[2] != '':
                    self.data_links[int(items[0])] = [items[1], items[2]]
        
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

            
        self.movies_id_cut = [movie_id for movie_id in self.data_links.keys()][:10]
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9"
        }

        self.imdb_cache = {}

    def _ensure_cashed(self, movie_id):
        if movie_id in self.imdb_cache:
            return
        imdb_id = self.data_links[movie_id][0]
        url = f'https://www.imdb.com/title/tt{imdb_id}/'
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Page not found: {url}")
        
        soup = BeautifulSoup(response.text, "html.parser")
        values = {}

        for li in soup.select('li.ipc-metadata-list__item'):
            label_tag = li.find('span', class_='ipc-metadata-list-item__label')
            if not label_tag:
                continue
            label = label_tag.get_text(strip=True)

            is_multiple_field = label in ['Countries of origin', 'Languages', 'Genres', 'Production companies']

            if is_multiple_field:
                val_tags = li.find_all(['a', 'span'], class_='ipc-metadata-list-item__list-content-item')
                if val_tags:
                    values_list = [tag.get_text(strip=True) for tag in val_tags if tag.get_text(strip=True)]
                    values[label] = ','.join(values_list) if values_list else "N/A"
                else:
                    values[label] = "N/A"
            else:
                val_tag = li.find(['a', 'span'], class_='ipc-metadata-list-item__list-content-item')
                values[label] = val_tag.get_text(strip=True) if val_tag else "N/A"

        self.imdb_cache[movie_id] = values
    
    def get_imdb(self, list_of_movies, list_of_fields):
        """
        The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
        """
        imdb_info = []

        for movie_id in list_of_movies:
            self._ensure_cashed(movie_id)
            values = [self.imdb_cache[movie_id].get(field, "N/A") for field in list_of_fields]
            imdb_info.append([movie_id] + values)

        return sorted(imdb_info, key=lambda x: x[0], reverse=True)
    
    def _to_int(self, value):
        """Превращает строку с деньгами или числом в int. Возвращает -inf для N/A."""
        if not value or value == "N/A":
            return -float('inf')
        digits = re.sub(r"[^\d]", "", value)
        return int(digits) if digits else -float('inf')
        
    def _format_money(self, value):
        """Форматирует число в $12,345,678. N/A оставляет как есть."""
        if value == 'N/A' or value == -float('inf'):
            return 'N/A'
        return f'${value:,}'

    def top_directors(self, n):
        """
        The method returns a dict with top-n directors where the keys are directors and 
        the values are numbers of movies created by them.
        """
        imdb_info = self.get_imdb(self.movies_id_cut, ['Director'])
        directors = [item[1] for item in imdb_info if item[1] != "N/A"]
        return dict(Counter(directors).most_common(n))
        
    def most_expensive(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets.
        """
        imdb_info = self.get_imdb(self.movies_id_cut, ['Budget'])
        budgets = {val[0] : self._to_int(val[1]) for val in imdb_info}
        budgets_sorted = sorted(budgets.items(), key=lambda x: x[1], reverse=True)[:n]
        return {self.movie_titles[item[0]] : self._format_money(item[1]) for item in budgets_sorted}
        
    def most_profitable(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
        """
        imdb_info = self.get_imdb(self.movies_id_cut, ['Gross worldwide', 'Budget'])

        profits = {}
        for item in imdb_info:
            gross = self._to_int(item[1])
            budget = self._to_int(item[2])
            if gross < 0 or budget < 0:
                profits[item[0]] = -float('inf')
            else:
                profits[item[0]] = gross - budget

        profits_sorted = sorted(profits.items(), key=lambda x: x[1], reverse=True)[:n]

        return {self.movie_titles[item[0]] : self._format_money(item[1]) for item in profits_sorted}
    
    def _to_minutes(self, value):
        if not value or value == "N/A":
            return -1
        hours, minutes = 0, 0
        match_h = re.search(r'(\d+)h', value)
        match_m = re.search(r'(\d+)m', value)
        if match_h:
            hours = int(match_h.group(1))
        if match_m:
            minutes = int(match_m.group(1))
        return hours * 60 + minutes
        
    def longest(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime.
        """
        runtimes = self.get_imdb(self.movies_id_cut, ['Runtime'])
        runtimes_sorted = sorted(runtimes, key=lambda x: self._to_minutes(x[1]), reverse=True)[:n]
        return {self.movie_titles[item[0]] : item[1] for item in runtimes_sorted}
    
    def _format_cost_per_min(self, value):
        if value == -1:
            return 'N/A'
        return f'{value:.2f}'
        
    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the budgets divided by their runtime.
        """
        imdb_info = self.get_imdb(self.movies_id_cut, ['Budget', 'Runtime'])

        costs = {}
        for item in imdb_info:
            budget = self._to_int(item[1])
            runtime = self._to_minutes(item[2])
        
            if budget < 0 or runtime < 0:
                costs[item[0]] = -1
            else:
                costs[item[0]] = budget / runtime

        costs_sorted = sorted(costs.items(), key=lambda x: x[1], reverse=True)[:n]
        return {self.movie_titles[item[0]] : self._format_cost_per_min(item[1]) for item in costs_sorted}
    
    def best_opening_weekend(self, n):
        """
        Возвращает топ-n фильмов по сборам в первый уикенд в США и Канаде
        Ключи - названия фильмов, значения - сборы в первый уикенд
        """
        imdb_info = self.get_imdb(self.movies_id_cut, ['Opening weekend US & Canada'])
        opening_weekends = {}
        
        for item in imdb_info:
            opening = self._to_int(item[1])
            if opening > 0:
                opening_weekends[item[0]] = opening
        
        opening_sorted = sorted(opening_weekends.items(), key=lambda x: x[1], reverse=True)[:n]
        return {self.movie_titles[movie_id]: self._format_money(opening) for movie_id, opening in opening_sorted}
    
    def top_countries(self, n):
        """
        Возвращает топ-n стран по количеству фильмов
        Ключи - страны, значения - количество фильмов
        """
        imdb_info_1 = self.get_imdb(self.movies_id_cut, ['Country of origin'])
        imdb_info_2 = self.get_imdb(self.movies_id_cut, ['Countries of origin'])
        imdb_info = imdb_info_1 + imdb_info_2

        countries = []

        for item in imdb_info:
            if item[1] != "N/A":
                individual_countries = [country for country in item[1].split(',')]
                countries.extend(individual_countries)

        return dict(Counter(countries).most_common(n))