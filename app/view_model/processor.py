from app.models.article import Category, Tag, Article
from app.ext import db
import datetime
from functools import reduce




def utility_processor():
    def category_lists():
        '''
        列表
        '''
        _query = Category.query.filter(Category.parent_id.is_(None)).order_by(Category.order)
        return _query.all()


    def category_lists_count():
        """
        返回栏目列表+数量
        """
        cate_list = Category.query.all()
        return [{"category": cate, "count": cate.articles.count()} for cate in cate_list]

    def tag_lists(limit = None):
        _query = Tag.query
        if isinstance(limit, int):
            _query = _query.limit(limit)
        return _query.all()

        # 最新文章列表
    def get_latest_articles(limit=8):
        _query = Article.query.filter_by(published=True).order_by(Article.last_modified.desc())
        return _query.limit(int(limit)).all()

    def get_top_articles(days=365, limit=5):
        art = []
        _start = datetime.date.today() - datetime.timedelta(days)
        art.append(Article.created >= _start)
        # //累计
        q = reduce(db.and_, art)
        return Article.query.filter_by(published=True).filter(q)\
                .order_by(Article.hits.desc()).limit(int(limit)).all()


    return dict(
        Category=Category,
        category_lists=category_lists,
        category_lists_count=category_lists_count,
        tag_lists=tag_lists,
        get_latest_articles = get_latest_articles,
        get_top_articles=get_top_articles,
    )

