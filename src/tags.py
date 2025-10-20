from collections import Counter

class Tags:
    """ Analyzing data from tags.csv """
    def __init__(self, path_to_the_file):
        with open(path_to_the_file, 'r') as f:
            f.readline()
            self.data_tags = [line.strip().split(',') for line in f]
        
        self.unique_tags = {line[2].strip().lower() for line in self.data_tags}

    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict 
        where the keys are tags and the values are the number of words inside the tag.
        """
        big_tags = {tag : len(tag.split()) for tag in self.unique_tags}
        return dict(sorted(big_tags.items(), key=lambda x: x[1], reverse=True)[:n])

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        return sorted(self.unique_tags, key=len, reverse=True)[:n]

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and 
        top-n longest tags in terms of the number of characters.
        """
        top_words = set(self.most_words(n).keys())
        top_chars = set(self.longest(n))
        return sorted(top_words & top_chars, key=len, reverse=True)
        
    def most_popular(self, n):
        """
        The method returns the most popular tags. 
        It is a dict where the keys are tags and the values are the counts.
        """
        all_tags = [line[2].strip().lower() for line in self.data_tags]
        return dict(Counter(all_tags).most_common(n))
        
    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates.
        """
        tags_with_word = [tag for tag in self.unique_tags if word.lower() in tag.lower()]
        return sorted(tags_with_word)
    

    """Additional part"""
    def get_tags_by_word_count(self, count):
        """
        Returns a list of unique tags consisting of exactly the specified number of words.
        """
        found_tags = [tag for tag in self.unique_tags if len(tag.split()) == count]
        return sorted(found_tags)
    

    
    def get_tags_stats(self):
        """
        Returns statistics on unique tags: minimum, maximum, and
        average tag length in characters.”
        """
        if not self.unique_tags:
            return {'min': 0, 'max': 0, 'average': 0}
        
        tag_lengths = [len(tag) for tag in self.unique_tags]
        min_length = min(tag_lengths)
        max_length = max(tag_lengths)
        average_length = round(sum(tag_lengths) / len(tag_lengths), 2)
        return {
            'min': min_length,
            'max': max_length,
            'average': average_length
        }