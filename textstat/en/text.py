import warnings
from importlib import resources
from math import sqrt

from textstat import core
from textstat.citation import citeable
from textstat.citation.metadata import BookSource, JournalSource
from textstat.en import mixins
from textstat.en.sentence import Sentence
from textstat.en.word import Word


class Text(mixins.Span, core.Text):
    """English Text class with readability formulas and text statistics.

    Extends the core Text class with English-specific readability formulas
    and analysis methods. Provides various standardized readability scores
    used in education and publishing.

    Attributes:
        sentence_class: The Sentence class to use (English version).
        word_class: The Word class to use (English version).
    """

    sentence_class = Sentence
    word_class = Word

    @citeable(
        authors=["Flesch, R."],
        title="A new readability yardstick",
        year=1948,
        source=JournalSource(
            name="Journal of Applied Psychology", volume=32, issue=3, pages="221-232"
        ),
        doi="10.1037/h0057532",
    )
    def flesch_reading_ease(self) -> float:
        """Calculate Flesch Reading Ease score.

        Returns a score from 0-100, where higher scores indicate easier readability.
        """
        return (
            206.835
            - (1.015 * self.avg("words", per="sentences"))
            - (84.6 * self.avg("syllables", per="words"))
        )

    @citeable(
        authors=["Kincaid, J.P.", "Fishburne, R.P.", "Rogers, R.L.", "Chissom, B.S."],
        title="Derivation of new readability formulas for Navy enlisted personnel",
        year=1975,
        source=BookSource(publisher="Naval Technical Training Command"),
        doi="10.21236/ADA006655",
    )
    def flesch_kincaid_grade(self) -> float:
        """Calculate Flesch-Kincaid Grade Level.

        Returns the US grade level required to understand the text.
        """
        return (
            (0.39 * self.avg("words", per="sentences"))
            + (11.8 * self.avg("syllables", per="words"))
            - 15.59
        )

    def smog(self) -> float:
        """
        https://web.archive.org/web/20150905104444/http://www.harrymclaughlin.com/SMOG.htm
        """
        # TODO: Implement sampling
        if len(self.sentences) < 30:
            warnings.warn(
                "Texts of fewer than 30 sentences are considered statistically "
                "invalid, because the formula was normed on 30-sentence samples."
            )
        return 1.0430 * sqrt(
            len(self.filter(Word.syllables >= 3)) * (30 / len(self.sentences)) + 3.1291
        )

    @citeable(
        authors=["Mc Laughlin, G.H."],
        title="SMOG Grading-a New Readability Formula",
        year=1969,
        source=JournalSource(
            name="Journal of Reading", volume=12, issue=8, pages="639-646"
        ),
    )
    def smog_grade(self) -> float:
        """Calculate SMOG (Simple Measure of Gobbledygook) grade level.

        Returns the years of education required to understand the text.
        """
        # TODO: Implement sampling
        if len(self.sentences) < 30:
            warnings.warn(
                "Texts of fewer than 30 sentences are considered statistically "
                "invalid, because the formula was normed on 30-sentence samples."
            )
        return (
            sqrt(len(self.filter(Word.syllables >= 3)) * (30 / len(self.sentences))) + 3
        )

    @citeable(
        authors=["Coleman, M.", "Liau, T.L."],
        title="A computer readability formula designed for machine scoring",
        year=1975,
        source=JournalSource(
            name="Journal of Applied Psychology", volume=60, issue=2, pages="283-284"
        ),
        doi="10.1037/h0076540",
    )
    def coleman_liau_index(self) -> float:
        """Calculate Coleman-Liau Index.

        Returns the US grade level required to understand the text.
        """
        return (
            (0.0588 * (self.avg("letters", per="words") * 100))
            - (0.296 * (self.avg("sentences", per="words") * 100))
            - 15.8
        )

    @citeable(
        authors=["Senter, R.J.", "Smith, E.A."],
        title="Automated readability index",
        year=1967,
        source=BookSource(publisher="Cincinnati University"),
    )
    def automated_readability_index(self) -> float:
        """Calculate Automated Readability Index (ARI).

        Returns the US grade level required to understand the text.
        """
        return (
            4.71 * self.avg("characters", per="words")
            + 0.5 * self.avg("words", per="sentences")
            - 21.43
        )

    @citeable(
        authors=["Klare, George R."],
        title="Assessing Readability",
        year=1974,
        source=JournalSource(
            name="Reading Research Quarterly", volume=10, issue=1, pages="62-102"
        ),
        doi="10.2307/747086",
    )
    def linsear_write_formula(self) -> float:
        """
        Klare, George R. "Assessing readability."
        Reading research quarterly (1974): 62-102.
        """
        # TODO: Implement sampling
        easy_points = len(self.filter(Word.syllables < 3)) * 1
        difficult_points = len(self.filter(Word.syllables >= 3)) * 3

        result = (easy_points + difficult_points) / len(self.sentences)

        return result / 2 if result > 20 else (result / 2) - 1

    @citeable(
        authors=["Chall, Jeanne Sternlicht", "Dale, Edgar"],
        title="Readability Revisited: The New Dale-Chall Readability Formula",
        year=1995,
        source=BookSource(publisher="Brookline Books", isbn="1571290087"),
    )
    def dale_chall_readability_score(self) -> float:
        """ """
        _word_list = resources.read_text(
            "textstat.en.resources", "dale_chall_3000.txt"
        ).split(" ")

    @citeable(
        authors=["Dale, Edgar", "Chall, Jeanne Sternlicht"],
        title="A Formula for Predicting Readability: Instructions",
        year=1948,
        source=JournalSource(
            name="Educational Research Bulletin", volume=27, issue=2, pages="37-54"
        ),
    )
    def dale_chall_readability_score_original(self) -> float:
        """ """
        # TODO: Needs Dale-Chall 763 word list
        ...

    @citeable(
        authors=["Gunning, R."],
        title="Technique of clear writing",
        year=1952,
        source=BookSource(publisher="McGraw-Hill"),
    )
    def gunning_fog(self) -> float:
        """Calculate Gunning Fog Index.

        Returns the years of education required to understand the text.
        """
        # TODO: Implement sampling
        return 0.4 * (
            self.avg("words", per="sentences")
            + (len(self.filter(Word.syllables >= 3)) / len(self.words)) * 100
        )

    @citeable(
        authors=["Björnsson, C. H."],
        title="Läsbarhet",
        year=1968,
        source=BookSource(publisher="Liber"),
    )
    def lix(self) -> float:
        """ """
        return (len(self.words) / len(self.sentences)) + (
            (len(self.filter(Word.length > 6)) / len(self.words)) * 100
        )

    @citeable(
        authors=["Anderson, Jonathan"],
        title="Lix and rix: Variations on a little-known readability index",
        year=1983,
        source=JournalSource(
            name="Journal of Reading", volume=26, issue=6, pages="490-496"
        ),
    )
    def rix(self) -> float:
        """
        Anderson, Jonathan.
        "Lix and rix: Variations on a little-known readability index."
        Journal of Reading 26.6 (1983): 490-496.
        """
        return len(self.filter(Word.length >= 7)) / len(self.sentences)

    @citeable(
        authors=["Spache, George"],
        title="A New Readability Formula for Primary-Grade Reading Materials",
        year=1953,
        source=JournalSource(
            name="The Elementary School Journal", volume=53, issue=7, pages="410-413"
        ),
        doi="10.1086/458513",
    )
    def spache_readability(self) -> float:
        """
        Spache, George.
        "A new readability formula for primary-grade reading materials."
        The Elementary School Journal 53.7 (1953): 410-413.
        """
        # TODO: Needs Dale-Chall 763 word list
        ...
