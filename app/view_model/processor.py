from app.models.article import Category


def utility_processor():
    def  category_lists():
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
        return [{"category": cate.name, "count": cate.articles.count()} for cate in cate_list]

    return dict(
        Category=Category,
        category_lists=category_lists,
        category_lists_count=category_lists_count,
    )