from .ethnicity_label_converting import EntityConverterEngine
from .university_matching import UniversityMatchEngine
from .webscraping import ActorScraperEngine

converter = EntityConverterEngine()
university_matcher = UniversityMatchEngine()
spider = ActorScraperEngine()
