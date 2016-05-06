# -*- coding: utf-8 -*-
from .. import _NTM_
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL

class dbo(object):
    """description of class"""

    __metaclass__ = _NTM_
    recursive_level = 0

    def __init__(self, obj_cfg, *args, **kwargs):
        self.config = obj_cfg
        return super(dbo, self).__init__(extra, *args, **kwargs)

    def recurse(self):
        if self.recursive_level >= self.config['max_recursive_level']:
            self.recursive_level = 0
            sce = mysqlc.Error("Error generating SQL command: maximum recursive level reached.")
            self.log(ERROR, sce.message)
            raise sce
            return False
        else:
            self.recursive_level += 1
            return True

    def dqlSelect(self, select, recursive_level_reset = False, **kwargs):
        if recursive_level_reset:
            self.recursive_level = 0
        if not self.recurse():
            return ("")
        DQL = (
            "SELECT "
            "{distinction} {priority} {straight_join} {result_options} {cache_option} {calc_found_rows} "
            "{select_exprs} {alais_name} "
            "{from_cls} "
            "{where_cls} "
            "{group_by_cls} "
            "{having_cls} "
            "{order_by_cls} "
            "{limit_cls} "
            "{procedure_cls} "
            "{into_cls} "
            "{locking_option}"
            ).format(
                distinction = select['distinct'],
                priority = select['priority'] if 'priority' in select else "",
                straight_join = "STRAIGHT_JOIN" if 'straight_join' in select and select['straight_join'] else "",
                result_options = "SQL_{option}_RESULT".format(
                    option = select['result_option']
                    ) if 'result_option' in select else "",
                cache_option = "SQL{c}_CACHE".format(
                    c = "_NO" if not select['cache'] else ""
                    ) if 'cache' in select else "",
                calc_found_rows = "SQL_CALC_FOUND_ROWS" if 'calc_found_rows' in select and select['calc_found_rows'] else "",
                select_exprs = ", ".join([ self.expExpression(item) for item in select['exprs'] ]),
                alais_name = "AS %s" % select['alais_name'] if 'alais_name' in select else "",
                from_cls = self.clsFrom(select['from_para']) if 'from_para' in select else "",
                where_cls = self.clsWhere(select['where_para'])if 'where_para' in select else "",
                group_by_cls = self.clsGroupBy(select['groupby_para']) if 'groupby_para' in select else "",
                having_cls = self.clsWhere(select['having_para']) if 'having_para' in select else "",
                oder_by_cls = self.clsOrderBy(select['orderby_para']) if 'orderby_para' in select else "",
                limit_cls = self.clsLimit(select['limit_para']) if 'limit_para' in select else "",
                procedure_cls = self.clsProcedure(select['procedure_para']) if 'procedure_para' in select else "",
                into_cls = self.clsInto(select['into_para']) if 'into_para' in select else "",
                locking_option = select['locking']
            )
        return (DQL)

    def expExpression(self, expr, **kwargs):
        if not self.recurse():
            return ("")
        if expr['operation'] in ["IS", ""]:
            EXP = "{boolean_primary} {is_cls}".format(
                boolean_primary = self.expBooleanPrimary(expr['boolean_primary']),
                is_cls = "IS {NOT} {val}".format(
                    NOT = "NOT" if expr['not'] else "",
                    val = expr['val']
                    ) if expr['operation'] else ""
                )
        else:
            EXP = "{left_expr} {operation} {right_expr}".format(
                left_expr = self.expExpression(expr['left_expr']),
                operation = expr['operation'],
                right_expr = self.expExpression(expr['right_expr'])
                )
        return (strip(EXP))

    def expBooleanPrimary(self, boolean_primary, **kwargs):
        if not self.recurse():
            return ("")
        if 'subquery' in boolean_primary:
            RIGHT = "{determiner} {subquery}".format(
                determiner = boolean_primary['determiner'],
                subquery = "(" + self.dqlSelect(**(boolean_primary['subquery'])) + ")"
                )
        elif boolean_primary['operation'] == "IS":
            RIGHT = "{NOT} NULL".format(
                NOT = "NOT" if ('not' in boolean_primary and boolean_primary['not']) else ""
                )
        else:
            RIGHT = self.expPredicate(boolean_primary['predicate'])
        EXP = "{nested_boolean_primary} {operation} {right_expr}".format(
            nested_boolean_primary = (self.expBooleanPrimary(boolean_primary['boolean_primary']) 
                                      if 'boolean_primary' in boolean_primary else ""),
            operation = boolean_primary['operation'],
            right_expr = strip(RIGHT)
            ) 
        return (strip(EXP))

    def expPredicate(self, predicate, **kwargs):
        if not self.recurse():
            return ("")
        if predicate['operation'] == "IN":
            RIGHT = "(" + (self.dqlSelect(**(predicate['subquery'])) if 'subquery' in predicate
                     else [self.expExpression(expr) for expr in predicate['exprs']]) + ")"
        elif predicate['operation'] == "BETWEEN":
            RIGHT = "{bit_expr} AND {nested_predicate}".format(
                bit_expr = predicate['bit_expr_2'],
                nested_predicate = self.expPredicate(predicate['predicate'])
                )
        elif predicate['operation'] == "SOUNDS LIKE":
            RIGHT = self.expBitExpression(predicate['bit_expr_2'])
        elif predicate['operation'] == "LIKE":
            RIGHT = "{simple_expr} {escape}".format(
                simple_expr = self.expSimpleExpression(predicate['simple_expr_1']),
                escape = "ESCAPE {simple_expr}".format(
                    simple_expr = self.expSimpleExpression(predicate['simple_expr_2'])
                    )
                )
        elif predicate['operation'] == "REGEXP":
            RIGHT = "REGEXP {bit_expr}".format(
                bit_expr = self.expBitExpression(predicate['bit_expr_2'])
                )
        else:
            sce = mysqlc.Error("Error generating SQL command: invalid parameter.")
            self.log(ERROR, sce.message)
            raise sce
        EXP = "{bit_expr} {NOT} {operation} {right_expr}".format(
            bit_expr = self.expBitExpression(predicate['bit_expr_1']),
            NOT = "NOT" if ('not' in predicate and predicate['not']) else "",
            operation = predicate['operation'],
            right_expr = strip(RIGHT)
            )
        return (strip(EXP))

    def expBitExpression(self, bit_expr, **kwargs):
        if not self.recurse():
            return ("")
        if 'simple_expr' in bit_expr:
            RIGHT = self.expSimpleExpression(bit_expr['simple_expr'])
        elif 'interval_expr' in bit_expr:
            RIGHT = bit_expr['interval_expr']
        else:
            RIGHT = self.expBitExpression(bit_expr['bit_expr_2'])
        EXP = "{left_expr} {operation} {right_expr}".format(
            left_expr = self.expBitExpression(bit_expr['bit_expr_1']) if 'bit_expr_1' in bit_expr else "",
            operation = bit_expr['operation'] if 'operation' in bit_expr else "",
            right_expr = strip(RIGHT)
            )
        return (strip(EXP))
    
    def expSimpleExpression(self, simple_expr, **kwargs):
        if not self.recurse():
            return ("")
        if simple_expr['operation'] == "COLLATE":
            RIGHT = simple_expr['collation_name']
        elif simple_expr['operation'] in [ "||", "+", "-", "~", "!", "BINARY" ]:
            RIGHT = self.expSimpleExpression(simple_expr['simple_expr_2'])
        elif 'exprs' in simple_expr:
            RIGHT = "{ROW} {expr_list}".format(
                ROW = "ROW" if 'row' in simple_expr and simple_expr['row'] else "",
                expr_list = "(" + ", ".join(simple_expr['exprs']) + ")"
                )
        elif 'subquery' in simple_expr:
            RIGHT = "{EXISTS} {subquery}".format(
                EXISTS = "EXISTS" if 'exists' in simple_expr and simple_expr['exists'] else "",
                subquery = self.dqlSelect(**(simple_expr['subquery']))
                )
        elif 'identifier' in simple_expr:
            RIGHT = ("{{ {identifier} {expr} }}".format(
                identifier = self.expIdentifier(simple_expr['identifier']),
                expr = self.expExpression(simple_expr['expr'])
                ) if 'expr' in simple_expr 
                else self.expIdentifier(simple_expr['identifier']))
        elif 'match_expr' in simple_expr:
            RIGHT = self.fctMatch(simple_expr['match_expr'])
        elif 'case_expr' in simple_expr:
            RIGHT = self.fcsCase(simple_expr['case_expr'])
        else:
            RIGHT = simple_expr['plain']
        EXP = "{left_expr} {operation} {right_expr}".format(
            left_expr = self.expSimpleExpression(simple_expr['simple_expr_1']) if 'simple_expr_1' in simple_expr else "",
            operation = simple_expr['operation'] if 'operation' in simple_expr else "",
            right_expr = strip(RIGHT)
            )
        return (strip(EXP))

    def fctMatch(self, match_expr, **kwargs):
        if not self.recurse():
            return ("")
        if 'search_modifier' in match_expr:
            if match_expr['search_modifier'] == "NL":
                MOD = "IN NATURAL LANGUAGE MODE"
            elif match_expr['search_modifier'] == "NQ":
                MOD = "IN NATURAL LANGUAGE MODE WITH QUERY EXPANSION"
            elif match_expr['search_modifier'] == "BL":
                MOD = "IN BOOLEAN MODE"
            elif match_expr['search_modifier'] == "QE":
                MOD = "WITH QUERY EXPANSION"
            else:
                sce = mysqlc.Error("Error generating SQL command: invalid parameter.")
                self.log(ERROR, sce.message)
                raise sce
        else:
            MOD = ""
        FCT = "MATCH {column_list} AGAINST ({expr} {search_modifier})".format(
            column_list = "(" + ", ".join(match_expr['columns']) + ")",
            expr = self.expExpression(match_expr['expr']),
            search_modifier = MOD
            )
        return (FCT)

    def fctCase(self, case_expr, **kwargs):
        if not self.recurse():
            return ("")
        WTL = [ "WHEN {compare_or_condition} THEN {result}".format(
            compare_or_condition = when_then['compare_or_condition'] if 'compare_or_condition' in when_then else "",
            result = when_then['result']
            ) for when_then in case_expr['when_then_list'] ]
        FCT = "CASE {value} {when_then_list} {ELSE} END".format(
            value = case_expr['value'],
            when_then_list = WTL,
            ELSE = "ELSE {result}".format(
                result = case_expr['else_result']
                ) if 'else_result' in case_expr else ""
            )
        return (FCT)

    def fctIf(self, if_expr, **kwargs):
        if not self.recurse():
            return ("")
        FCT = "IF({expr1},{expr2},{expr3})".format(
            expr1 = self.expExpression(if_expr['expr1']),
            expr2 = self.expExpression(if_expr['expr2']),
            expr3 = self.expExpression(if_expr['expr3'])
            )
        return (FCT)

    def fctIfNull(self, if_null_expr, **kwargs):
        if not self.recurse():
            return ("")
        FCT = "IFNULL({expr1},{expr2})".format(
            expr1 = self.expExpression(if_null_expr['expr1']),
            expr2 = self.expExpression(if_null_expr['expr2'])
            )
        return (FCT)

    def fctNullIf(self, null_if_expr, **kwargs):
        if not self.recurse():
            return ("")
        FCT = "NULLIF({expr1},{expr2})".format(
            expr1 = self.expExpression(null_if_expr['expr1']),
            expr2 = self.expExpression(null_if_expr['expr2'])
            )
        return (FCT)

    def optPartition(self, partition_options, **kwargs):
        if not self.recurse():
            return ("")
        OPT = ""
        return OPT

    def expTableFactor(self, table_factor, **kwargs):
        if not self.recurse():
            return ("")
        if 'table_subquery' in table_factor:
            EXP = "{table_subquery} AS {alias}".format(
                table_subquery = self.dqlSelect(**(table_factor['table_subquery'])),
                alias = table_factor['ailas']
                )
        elif 'table_references' in table_factor:
            EXP = "(" + ", ".join([self.expTableReference(item) for item in table_factor['table_references']]) + ")"
        else:
            EXP = "{table_name} {partition} {alias} {index_hint_list}".format(
                table_name = table_factor['table_name'],
                partition = self.optPartition(table_factor['partition']) if 'partition' in table_factor else "",
                alias = ("AS " + table_factor['alias']) if 'alias' in table_factor else "",
                index_hint_list = self.optIndexHintList(table_factor['index_hint_list']) if 'index_hint_list' in table_factor else ""
            )
        return (EXP)

    def expJoinTable(self, join_table, **kwargs):
        if not self.recurse():
            return ("")
        if join_table['join_option'] in [ "INNER", "CROSS" ]:
            JOIN = join_table['join_option'] + " JOIN"
            RIGHT = "{table_factor} {join_condition}".format(
                table_factor = self.expTableFactor(join_table['table_factor']),
                join_condition = self.expJoinCondition(join_table['join_condition']) if 'join_condition' in join_table else ""
                )
        elif join_table['join_option'] == "STRAIGHT_JOIN":
            JOIN = join_table['join_option']
            RIGHT = "{table_factor} {condition}".format(
                table_factor = self.expTableFactor(join_table['table_factor']),
                condition = "ON " + self.expExpression(join_table['conditional_expr']) if 'conditional_expr' in join_table else ""
                )
        elif join_table['join_option'] in [ "NATURAL", "DEFAULT" ]:
            JOIN = "{natural} {left_right} {outer} JOIN".format(
                natural = "NATURAL" if 'natural' in join_table and join_table['natural'] else "",
                left_right = join_table['left_right'] if 'left_right' in join_table else "",
                outer = "OUTER" if 'outer' in join_table and join_table['outer'] else ""
                )
            RIGHT = (self.expTableFactor(join_table['table_factor']) if 'natural' in join_table and join_table['natural'] 
                     else "{table_reference} {join_condition}".format(
                         table_reference = self.expTableReference(join_table['table_reference']),
                         join_condition = self.expJoinCondition(join_table['join_condition'])
                         )
                     )
        else:
            sce = mysqlc.Error("Error generating SQL command: invalid parameter.")
            self.log(ERROR, sce.message)
            raise sce
        EXP = "{table_reference} {join_option} {right_expr}".format(
            table_reference = self.expTableReference(join_table['table_reference']),
            join_option = strip(JOIN),
            right_expr = strip(RIGHT)
            )
        return (EXP)

    def expJoinCondition(self, join_condition, **kwargs):
        if not self.recurse():
            return ("")
        EXP = ("ON " + self.expExpression(join_condition['conditional_expr']) if join_condition['operation'] == "ON" 
               else "USING ({column_list})".format(
                   column_list = ",".join(join_condition['column_list'])
                   )
               )

    def optIndexHintList(self, index_hint_list, **kwargs):
        if not self.recurse():
            return ("")
        HINTS = [ ]
        for index_hint in index_hint_list:
            HINTS.append("{option} INDEX {for_clause} {index_list}".format(
                option = index_hint['option'],
                for_clause = "FOR {purpose}".format(
                    purpose = index_hint['for_purpose']
                    ) if index_hint['for_purpose'] else "",
                index_list = "(" + ", ".join(index_hint['index_names']) + ")"
                ))
        OPT = ", ".join(HINTS)
        return (OPT)

    def clsWhere(self, where_para, **kwargs):
        if not self.recurse():
            return ("")
        CLS = "WHERE {where_condition}".format(
            where_condition = self.expExpression(where_para['where_condition'])
            )
        return (CLS)

    def dqlUnion(self, unions, recursive_level_reset = False, **kwargs):
        if recursive_level_reset:
            self.recursive_level = 0
        if not self.recurse():
            return ("")
        UNI = [ strip("UNION {option} {select}".format(
            option = item['option'] if 'option' in item else "",
            select = self.dqlSelect(**(item['select']))
            )) for index, item in enumerate(unions) if index > 0 ]
        DQL = self.dqlSelect(**(unions[0]['select'])) + ", ".join(UNI)
        return (DQL)

    def expTableReference(self, table_reference, **kwargs):
        if not self.recurse():
            return ("")
        REF = "{OJ} {table_reference}".format(
            OJ = "OJ" if 'OJ' in item and item['OJ'] else "",
            table_reference = (self.expTableFactor(item['table_factor']) if 'table_factor' in item 
                                else self.expJoinTable(item['join_table']))
            )
        return (strip(REF))

    def clsFrom(self, from_para, **kwargs):
        if not self.recurse():
            return ("")
        CLS = "FROM {table_references} {partition}".format(
            table_references = ", ".join([self.expTableReference(item) for item in from_para['table_refernces']]),
            partition = self.optPartition(from_para['partition_list']) if 'partition_list' in from_para else ""
            )
        return (CLS)

    def clsGroupBy(self, groupby_para, **kwargs):
        if not self.recurse():
            return ("")
        ACC = [ "{accordance} {sorting}".format(
            accordance = item['accordance'],
            sorting = item['sorting']
            ) for item in groupby_para['accordance_list'] ]
        CLS = "GROUP BY {accordance_list} {rollup}".format(
            accordance_list = ", ".join(ACC),
            rollup = "WITH ROLLUP" if 'rollup' in groupby_para and groupby_para['rollup'] else ""
            )
        return (CLS)

    def clsHaving(self, having_para, **kwargs):
        if not self.recurse():
            return ("")
        CLS = "HAVING {where_condition}".format(
            where_condition = self.expExpression(having_para['where_condition'])
            )
        return (CLS)

    def clsOrderBy(self, orderby_para, **kwargs):
        if not self.recurse():
            return ("")
        ACC = [ "{accordance} {sorting}".format(
            accordance = item['accordance'],
            sorting = item['sorting']
            ) for item in orderby_para['accordance_list'] ]
        CLS = "ORDER BY {accordance_list}".format(
            accordance_list = ", ".join(ACC),
            )
        return (CLS)

    def clsLimit(self, limit_para, **kwargs):
        if not self.recurse():
            return ("")
        CLS = "LIMIT {offset}{row_count}".format(
            offset = limit_para['offset'] + ", " if 'offset' in limit_para else "",
            row_count = limit_para['row_count']
            )
        return (CLS)

    def clsProcedure(self, procedure_para, **kwargs):
        if not self.recurse():
            return ("")
        CLS = "PROCEDURE {procedure_name}({argument_list})".format(
            procedure_name = procedure_para['procedure_name'],
            argument_list = ", ".join(procedure_para['argument_list'])
            )
        return (CLS)

    def clsInto(self, into_para, **kwargs):
        if not self.recurse():
            return ("")
        elif self.recursive_level <= 2:
            sce = mysqlc.Error("Error generating SQL command: invalid parameter.")
            self.log(ERROR, sce.message)
            raise sce
            return ("")
        if into_para['targer_type'] in [ "OUTFILE", "DUMPFILE" ]:
            TGT = "\'" + into_para['file_name'] + "\'",
            OPT = "{charset} {export_options}".format(
                charset = "CHARACTER SET " + into_para['charset_name'] if 'charset_name' in into_para else "",
                export_options = ", ".join(into_para['export_options'])
                ) if into_para['target_type'] == "OUTFILE" else ""
        elif into_para['target_type'] == "":
            TGT = ", ".join(into_para['var_list'])
            OPT = ""
        CLS = "INTO {target_type} {target} {options}".format(
            target_type = into_para['target_type'],
            target = strip(TGT),
            options = strip(OPT)
            )
        return (CLS)

    def dmlInsert(self, inserts, recursive_level_reset = False, **kwargs):
        if recursive_level_reset:
            self.recursive_level = 0
        if not self.recurse():
            return ("")
        DML = REC = OND = [ ]
        for insert in inserts:
            REC = ", ".join([ "{col_name}={exp}".format(
                col_name = col,
                exp = "DEFAULT" if not col in insert or insert[col] == "DEFAULT" else self.expExpression(insert[col])
                ) for col in insert ])
            OND = "ON DUPLICATE KEY UPDATE " + ", ".join([ "{col_name}={exp}".format(
                col_name = col,
                exp = self.expExpression(insert['on_dup_updt'][col])
                ) for col in insert['on_dup_updt'] ])
            DML.append("INSERT {priority} INTO {tbl_name} SET {records} {on_dup_updt}".format(
                priority = insert['priority'] if 'priority' in insert else "",
                tbl_name = insert['tbl_name'],
                records = REC,
                on_dup_updt = OND
                )
                       )
        return (DML)

    def dmlInsertSelect(self, inserts, recursive_level_reset = False, **kwargs):
        if recursive_level_reset:
            self.recursive_level = 0
        if not self.recurse():
            return ("")
        DML = COL = SEL = OND = [ ]
        for insert_select in inserts:
            COL = "(" + ", ".join(insert_select['col_list']) + ")"
            SEL = self.dqlSelect(insert_select['select_expr'])
            OND = "ON DUPLICATE KEY UPDATE " + ", ".join([ "{col_name}={exp}".format(
                col_name = col,
                exp = insert_select['on_dup_updt'][col]
                ) for col in insert_select['on_dup_updt'] ]) if 'on_dup_updt' in insert_select else ""
            DML.append("INSERT {priority} INTO {tbl_name} {partition} {col_list} {select_expr} {on_dup_updt}".format(
               priority = insert_select['priority'] if 'priority' in insert_select else "",
               tbl_name = insert_select['tbl_name'],
               col_list = COL,
               select_expr = SEL,
               on_dup_updt = OND
               )
                       )
        return (DML)

    def dmlDelete(self, deletes, recursive_level_reset = False, **kwargs):
        if recursive_level_reset:
            self.recursive_level = 0
        if not self.recurse():
            return ("")
        DML = [ ]
        for delete in deletes:
            DML.append("DELETE {priority} {quick} {ignore} FROM {tbl_list} {using} {partition} {where} {order_by} {limit}".format(
                priority = delete['priority'] if 'priority' in delete else "",
                quick = "QUICK" if 'quick' in delete and delete['quick'] == True else "",
                ignore = "IGNORE" if 'ignore' in delete and delete['ignore'] == True else "",
                tbl_list = ", ".join(delete['tbl_list']),
                using = "USING" + ", ".join([ self.expTableReference(item) for item in delete['table_references'] ]) if 'table_references' in delete else "",
                partition = self.optPartition(delete['partition']) if 'partition' in delete else "",
                where = self.clsWhere(delete['where']) if 'where' in delete else "",
                order_by = self.clsOrderBy(delete['order_by']) if 'order_by' in delete else "",
                limit = self.clsLimit(delete['limit']) if 'limit' in delete else ""
                ) )
        return (DML)

    def dmlUpdate(self, updates, recursive_level_reset = False, **kwargs):
        if recursive_level_reset:
            self.recursive_level = 0
        if not self.recurse():
            return ("")
        DML = [ ]
        for update in updates:
            REC = ", ".join([ "{col_name}={exp}".format(
                col_name = col,
                exp = "DEFAULT" if not col in update or update[col] == "DEFAULT" else self.expExpression(update[col])
                ) for col in update ])
            DML.append("UPDATE {priority} {ignore} {tabel_reference} SET {records} {where} {order_by} {limit}".format(
                priority = update['priority'] if 'priority' in update else "",
                ignore = "IGNORE" if 'ignore' in update and update['ignore'] else "",
                table_reference = self.expTableReference(updates[0]['table_reference']),
                records = REC,
                where = self.clsWhere(update['where_condition']) if 'where_condition' in update else "",
                order_by = self.clsOrderBy(update['order_by']) if 'order_by' in update else "",
                limit = self.clsLimit(update['limit']) if 'limit' in update else ""
                )
                       )
        return (DML)

    def mscCase(self, recursive_level_reset = False, **kwargs):
        if recursive_level_reset:
            self.recursive_level = 0
        if not self.recurse():
            return ("")
        pass

