import hashlib
from django.db import models



class Level(models.Model):
    hash = models.CharField(max_length=40, primary_key=True)
    name = models.CharField(max_length=64)

    # points = models.IntegerField()
    # maxsize = models.IntegerField()
    # order = models.IntegerField(default=0)

    file = models.FilePathField()

    class Meta:
        ordering = ['name']

    # def __init__(self, *args, **kwargs):
    #     super(Level, self).__init__(*args, **kwargs)
    #     self.lines = [map(str, line) for line in self.content.split()]

    # def get(self, x, y):
    #     if all([x >= 0, x < len(self.lines),
    #            y >= 0, y < len(self.lines[0])]):
    #         return self.lines[x][y]
    #     return None

    # @property
    # def start(self):
    #     for i, line in enumerate(self.lines):
    #         try:
    #             index = line.index("u")
    #             return (i, index)
    #         except ValueError:
    #             pass

    # @property
    # def dots(self):
    #     dots = []
    #     for y, line in enumerate(self.lines):
    #         for x, element in enumerate(line):
    #             if element == "o":
    #                 dots.append((y, x))
    #     return dots

    def __unicode__(self):
        return self.name
