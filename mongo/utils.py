import logging
import time 

# mongodb 添加索引
def indexing(db=None, *indexes):

    if db and indexes:

        _indexes = set([]) if db.count(
        ) == 0 else db.index_information().keys()

        for idx in indexes:

            options = dict(idx).get('__options__', {})
            idx = [k for k in idx if k[0] != '__options__']
            options['background'] = True

            now = time.time()
            # db.ensure_index(idx, **options)
            db.create_index(idx, **options)
            if time.time() - now > 1.0:
                logging.info("create index %s->%s" % (repr(idx), repr(db)))
    return lambda func: func


    