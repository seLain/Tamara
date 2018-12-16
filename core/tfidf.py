import jieba
import jieba.analyse
from jieba.analyse.tfidf import TFIDF as jiebaTFIDF


class TFIDF(jiebaTFIDF):

    def __init__(self):
        super(TFIDF, self).__init__()

    def update_idf(self):
        from core.models import FragmentTag
        self.idf_freq = {t.name: t.idf for t in FragmentTag.objects.all()}
        self.median_idf = sorted(
            self.idf_freq.values())[len(self.idf_freq) // 2] if self.idf_freq else None

tfidf = TFIDF()