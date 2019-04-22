from app.models.article import Category, Tag


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


    return dict(
        Category=Category,
        category_lists=category_lists,
        category_lists_count=category_lists_count,
        tag_lists=tag_lists,
    )