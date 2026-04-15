from decision_pages_a import DECISION_ARTICLES_A
from decision_pages_b import DECISION_ARTICLES_B
from industry_pages import INDUSTRY_DETAIL_PAGES
from landing_pages import CAMPAIGN_LANDING_PAGES, GUIDE_INDEX_PAGE
from english_resource_pages import (
    CAMPAIGN_LANDING_PAGES_EN,
    EN_DECISION_ARTICLES,
    GUIDE_INDEX_PAGE_EN,
    INDUSTRY_DETAIL_PAGES_EN,
)


DECISION_ARTICLES = {}
DECISION_ARTICLES.update(DECISION_ARTICLES_A)
DECISION_ARTICLES.update(DECISION_ARTICLES_B)

for _key, _article in EN_DECISION_ARTICLES.items():
    DECISION_ARTICLES.setdefault(_key, {}).update({"en": _article})

