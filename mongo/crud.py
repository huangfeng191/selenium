# -*- coding: utf-8 -*-

from mongo.i_crud import ICRUD
import time 
import logging 
from mongo.utils import indexing
from collections import OrderedDict
from bson.objectid import ObjectId
class MongoCRUD(ICRUD):
    def __init__(self, db, collection, *indexes, **kwArgs):
        '''
          @param sort 默认排序
          @param *indexes 索引列表
        '''

        self.__database = db
        self.__coll = collection
        self.__db = db[collection]
        self.__sort = [('_id', 1)]
        if indexes:
            self.index(indexes)
   
        # 测试连接

    def test_connect(self):
        try:
            sSec = time.localtime(time.time()).tm_sec
            self.db.count()
            eSec = time.localtime(time.time()).tm_sec
            return eSec - sSec
        except Exception as e:
            logging.exception(e)
            return 25

    @property
    def database(self):

        '@rtype : pymongo.Collection'
        return self.__database

    @property
    def db(self):

        '@rtype : pymongo.Collection'
        return self.__db

    @property
    def coll(self):

        '@rtype : string'
        return self.__coll

    def columns(self):
        rs = []
        for k, v in self.db.find_one().items():
            o = {}
            o['column'] = k
            o['name'] = k
            if isinstance(v, str):
                o['otype'] = 'string'
            elif isinstance(v, list):
                o['otype'] = 'list'
            elif isinstance(v, int):
                o['otype'] = 'int'
            elif isinstance(v, dict):
                o['otype'] = 'dict'
            elif isinstance(v, type(None)):
                o['otype'] = 'None'
            else:
                o['otype'] = 'string'

            o['type'] = o['otype']
            rs.append(o)
        return rs

    def exists(self, _id, *args, **kwArgs):

        return self.db.find_one(_id, projection=['_id']) is not None

    def get(self, _id, *args, **kwArgs):

        return self.db.find_one(_id)

    def one(self, query=None, sort=None, *args, **kwArgs):

        q = query or {}
        c = self.db.find(q)

        if sort is not None:
            c.sort(sort).limit(1)

        for _c in c:
            return _c

        return {}

        '''
        @param module - 注入目标
        @parma field  - 注入目标字段
        @param id_key - 注入参考字段
        208-07-29 新加
        @param id_key_def - 注入所取字段，非_id时使用
      '''

    def inject(self, module, field, id_key, deleteCascade=False,id_key_def=None):

        if self == module:
            logging.warn("Self equals module!")
            return

        def inject_on_insert(_id, obj):
            if id_key_def:
                self.db.update({id_key: obj.get(id_key_def)}, {'$set': {field: obj}}, multi=True)
            else:
                self.db.update({id_key: _id}, {'$set': {field: obj}}, multi=True)

        def inject_on_update(_id, obj, old):
            if id_key_def:
                self.db.update({id_key: obj.get(id_key_def)}, {'$set': {field: obj}}, multi=True)
            else:
                self.db.update({id_key: _id}, {'$set': {field: obj}}, multi=True)

        def inject_on_delete(_id, obj):
            if id_key_def:
                if obj.get(id_key_def):
                    for o in self.items(query={id_key: obj.get(id_key_def)}):
                        self.delete(o['_id'])
            else:
                for o in self.items(query={id_key: _id}):
                    self.delete(o['_id'])

        def self_inject_on_upsert(_id, obj, old):

            if id_key not in obj or not obj[id_key]:
                return

            if obj[id_key]:
                if id_key_def:
                    self.db.update({id_key_def: obj[id_key]}, {'$set': {field: module.get({id_key_def:obj[id_key]})}})
                else:
                    self.db.update({'_id': _id}, {'$set': {field: module.get(obj[id_key])}})


        module.on_insert += inject_on_insert;
        module.on_update += inject_on_update;

        if deleteCascade:
            module.on_delete += inject_on_delete

        self.on_upsert += self_inject_on_upsert

        indexing([(id_key, 1)])
        indexing([('%s._id' % field, 1)])

    def index(self, indexes=None):

        if indexes:
            indexing(self.__db, *indexes)

    # 清空表
    def remove(self, *args, **kwArgs):
        return self.db.remove()

    def delete(self, _id=None, record=None,_validate=True, _direct=False, multi=False, *args, **kwArgs):
        if _validate:
            self.validate(action='delete', _id=_id)

        # 强行删除多行时，直接返回
        if multi:
            return self.db.remove(_id)

        o = self.get(_id)

        if o:
            self.db.remove({'_id': o['_id']})

        if not _direct:
            self.on_delete(_id, o)

        

        return o

    '''
      数据验证接口
    '''

    def validate(self, action=None, _id=None, record=None, *args, **kwArgs):
        if not action:
            raise Exception('操作符不存在!')

        elif action == 'insert':
            if _id:
                raise Exception('非法插入!')
            return True
        elif action == 'update':
            if not _id:
                raise Exception('非法更新!')
            return True
        elif action == 'delete':
            if not _id:
                raise Exception('非法删除!')
            return True
        else:
            raise Exception('错误操作符!')

    def upsert(self, _id=None, _query=None, _changed=True, _upsert=False, _direct=False, _multi=False, _insert=True,
              _old=None, _action=None, *args, **kwArgs):

        s = kwArgs

        action = None
        if _action:
            action = _action
        else:
            action = 'update' if _id else 'insert'

        if self.validate(action=action, _id=_id):
            if action == 'insert' and not _old:
                _id = s['_id'] = str(ObjectId())

        current = int(time.time())
        old=_old or None

        if not old and action == 'update':
            old = self.get(_id); # 如果指定了 是insert 说明不需要验证重复性，由程序控制
        elif old:
            _id=old["_id"]
        if not old:

            if not _insert:
                return None

            if _changed:
                s['changed'] = current

            if 'created' not in s:
                s['created'] = current

            s['_id'] = _id

            self.db.insert(s)

            if not _direct:
                self.on_insert(_id, s)

        else:

            q = _query or {}
            q['_id'] = _id

            if any([k.startswith('$') for k in s.keys()]):

                st = s.get('$set', {})

                if _changed:
                    st['changed'] = current

                s['$set'] = st

            else:

                if _changed:
                    s['changed'] = current

                st = s
                s = {}
                s['$set'] = st

            self.db.update(q, s, upsert=_upsert, multi=_multi)

            '''同步数据'''
            s = self.get(_id)

            if not _direct:
                self.on_update(_id, s, old)

        s['_id'] = _id

        if not _direct:
            self.on_upsert(_id, s, old)

        if not _direct:
            s = self.get(_id)

        return s

    def query(self, conditions=None):

        q = OrderedDict()

        if conditions:

            for c in conditions:

                if not c: continue

                f = c.get('Field')
                r = c.get('Relation', 'and')
                o = c.get('Operate', '')
                v = c.get('Value')

                if f and o:

                    a = None

                    if r == 'and':
                        q['$and'] = q.get('$and', [])
                        a = q['$and']
                    elif r == 'or':
                        q['$or'] = q.get('$or', [])
                        a = q['$or']

                    if a is not None:

                        if o == 'like':
                            a.append({f: {'$regex': v}})
                        elif o == 'prefix':
                            a.append({f: {'$regex': '^%s' % v}})
                        elif o == '=':
                            if v == '':
                                a.append({f: {'$in': [v, []]}})
                            else:
                                a.append({f: v})
                        elif o == '>=':
                            a.append({f: {'$gte': v}})
                        elif o == '>':
                            a.append({f: {'$gt': v}})
                        elif o == '<=':
                            a.append({f: {'$lte': v}})
                        elif o == '<':
                            a.append({f: {'$lt': v}})
                        elif o == 'nil':
                            a.append({f: {'$exists': False}})
                        elif o == 'exists':
                            a.append({f: {'$exists': True}})
                        elif o == '!=':
                            a.append({f: {'$ne': v}})
                        elif o == "in":
                            a.append({f: {'$in': v}})
                        elif o == 'between' and v and len(v) == 2:
                            a.append({f: {'$gte': v[0], '$lte': v[1]}})

        if '$and' in q and len(q.get('$and')) == 0:
            del q['$and']

        if '$or' in q and len(q.get('$or')) == 0:
            del q['$or']

        return q

    def sort(self, order=None):

        if order:
            s = []
            for o in order:

                f = o.get('Field')
                t = -1 if o.get('Type', False) else 1
                if f:
                    s.append((f, t))
            return s
        else:
            return self.__sort

    def items(self, size=None, index=1, conditions=None, order=None, fields=None, query=None, _sort=None, *args,
              **kwArgs):

        q = self.query(conditions)

        if query:
            for k, v in query.items():
                q[k] = v

        c = self.db.find(q, projection=fields)

        c.sort(_sort if _sort is not None else self.sort(order=order))

        if index > 1 and (size is not None):
            c.skip((index - 1) * size)

        if size is not None and size > 0:
            c.limit(size)

        return c

    def group(self, key, condition, initial, reduce, finalize=None, *args, **kwArgs):  # @ReservedAssignment
        return self.db.group(key, condition, initial, reduce, finalize)

    def distinct(self, condition=None, fields=None, order=None, _sort=None, *args, **kwArgs):
        c = self.db.distinct(fields, condition)
        return c

    def count(self, conditions=None, query=None, *args, **kwArgs):

        q = self.query(conditions)

        if query:
            for k, v in query.items():
                q[k] = v

        return self.db.find(q).count()

    def count2(self, query=None, *args, **kwArgs):
        return self.db.find(query).count()

    def aggregate(self, count=True, index=1, size=None, conditions=None, groups=None, aggregate=None, order=None,
                  fields=None, unwind=None, *args, **kwArgs):

        pipeline = []

        p_m = {'$match': None}
        p_g = {'$group': {'_id': None}}
        p_s = {'$sort': None}
        p_f = {'$project': None}
        p_skip = {'$skip': None}
        p_limit = {'$limit': None}
        p_unwind = {'$unwind': None}

        # 条件
        if conditions:
            q = self.query(conditions)
            if len(q.items()) > 0:
                p_m['$match'] = q
        # 分组
        if groups:
            gs = OrderedDict()
            for g in groups:
                gs[g.get('Field')] = '$' + g.get('Field')

            if len(gs.items()) > 0:
                p_g['$group']['_id'] = gs
        # 聚合
        if aggregate:
            for a in aggregate:
                if a['Type'] == 'fx':  # 默认输出
                    if fields == None: fields = {}
                    fields[a['Field']] = 1
                    continue

                f = a.get('Field', '') if a.get('Alias', '') == '' else a.get('Alias', '')
                t = 'sum' if a['Type'] == 'count' else a['Type']
                p_g['$group'][f] = {'$' + t: '$' + a['Field']}

        # 排序
        if order:
            v = {}
            for o in order:
                order = 1 if o['Type'] == 0 else -1
                v[o['Field']] = order

            p_s['$sort'] = v
        # 筛选字段
        if fields:
            if not groups and not aggregate:  # 有group 或 aggregate的情况下默认跳过
                o = {}
                for k, v in fields.items():
                    o[k] = v
                p_f['$project'] = o

        # 展开的数组字段
        if unwind: p_unwind['$unwind'] = '$' + unwind

        if index > 1 and (size is not None): p_skip['$skip'] = (index - 1) * size

        if  size is not None and size > 0: p_limit['$limit'] = size

        if p_m['$match']: pipeline.append(p_m)
        if p_unwind['$unwind']: pipeline.append(p_unwind)
        if p_g['$group']['_id'] or len(p_g['$group'].items()) > 1: pipeline.append(p_g)
        if p_f['$project']: pipeline.append(p_f)
        if p_s['$sort']: pipeline.append(p_s)
        if p_skip['$skip']: pipeline.append(p_skip)
        if p_limit['$limit']: pipeline.append(p_limit)

        def assemble(rs, count):
            d = []
            for r in rs._CommandCursor__data:
                o = {}
                for k, v in r.items():
                    if k == '_id' and v:
                        # 如果不是字符串
                        if isinstance(v, tuple):
                            for _id in v.items():
                                o[_id[0]] = _id[1]
                        else:
                            o[k] = v
                    else:
                        o[k] = v
            d.append(o)

            c = 0
            if count: c = rs._CommandCursor__collection.count()

            return d, c

        return assemble(self.db.aggregate(pipeline), count)


