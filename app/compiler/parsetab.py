
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'startAND ASC BIGGER BIGGER_EQUAL BY COLNAME COLNUMBER COMMA DATASOURCE DELETE DESC DISTINCT DIVIDE EQUAL FLOATNUMBER FROM INSERT INTO LIKE LIMIT LPAREN MINUS NEGATIVE_INTNUMBER NOT NOTEQUAL OR ORDER PATTERN PERCENT PLUS POSITIVE_INTNUMBER RPAREN SELECT SET SIMICOLON SMALLER SMALLER_EQUAL STRING TAIL TIMES UPDATE VALUES WHEREstart : select\n| insert\n| update\n| deleteempty :select : SELECT distinct select_columns FROM DATASOURCE into where order limit_or_tail SIMICOLONinsert : INSERT INTO DATASOURCE icolumn VALUES insert_values SIMICOLONupdate : UPDATE DATASOURCE SET assigns where SIMICOLONdelete : DELETE FROM DATASOURCE wherelogical :  EQUAL\n| NOTEQUAL\n| BIGGER_EQUAL\n| BIGGER\n| SMALLER_EQUAL\n| SMALLERwhere : WHERE conditionswhere : emptyconditions : LPAREN conditions RPARENconditions : conditions AND conditions\n| conditions OR conditions\n| exp LIKE STRING\n| exp logical expconditions : NOT conditionsexp : STRING\n| COLNAME\n| NUMBERNUMBER : NEGATIVE_INTNUMBER\n| POSITIVE_INTNUMBER\n| FLOATNUMBERdistinct : DISTINCTdistinct : emptycolumn : COLNUMBER\n| COLNAMEcolumns : columns COMMA columnscolumns : columnselect_columns : TIMESselect_columns : columnsinto : INTO DATASOURCEinto : emptyorder : ORDER BY column wayorder : emptyway : ASC\n| emptyway : DESClimit_or_tail : LIMIT POSITIVE_INTNUMBER\n| TAIL POSITIVE_INTNUMBERlimit_or_tail : emptyvalue : STRING\n| NUMBERvalues : values COMMA valuesvalues : valuesingle_values : LPAREN values RPARENinsert_values : insert_values COMMA insert_valuesinsert_values : single_valuesicolumn : LPAREN columns RPARENicolumn : emptyassign : column EQUAL valueassigns : assign COMMA assignsassigns : assign'
    
_lr_action_items = {'SELECT':([0,],[6,]),'INSERT':([0,],[7,]),'UPDATE':([0,],[8,]),'DELETE':([0,],[9,]),'$end':([1,2,3,4,5,24,33,35,43,46,48,49,50,51,52,60,76,79,83,84,85,86,87,100,],[0,-1,-2,-3,-4,-5,-9,-17,-16,-24,-25,-26,-27,-28,-29,-8,-23,-7,-19,-20,-18,-21,-22,-6,]),'DISTINCT':([6,],[11,]),'TIMES':([6,10,11,12,],[-5,17,-30,-31,]),'COLNUMBER':([6,10,11,12,23,26,28,41,98,],[-5,20,-30,-31,20,20,20,20,20,]),'COLNAME':([6,10,11,12,23,26,28,34,41,44,47,65,66,69,70,71,72,73,74,75,98,],[-5,21,-30,-31,21,21,21,48,21,48,48,48,48,48,-10,-11,-12,-13,-14,-15,21,]),'INTO':([7,36,],[13,54,]),'DATASOURCE':([8,13,15,25,54,],[14,22,24,36,78,]),'FROM':([9,16,17,18,19,20,21,37,],[15,25,-36,-37,-35,-32,-33,-34,]),'SET':([14,],[23,]),'COMMA':([18,19,20,21,31,37,39,50,51,52,56,57,62,63,64,81,82,91,92,99,],[26,-35,-32,-33,41,26,26,-27,-28,-29,80,-54,-57,-48,-49,93,-51,80,-52,93,]),'RPAREN':([19,20,21,37,39,46,48,49,50,51,52,63,64,67,76,81,82,83,84,85,86,87,99,],[-35,-32,-33,-34,59,-24,-25,-26,-27,-28,-29,-48,-49,85,-23,92,-51,-19,-20,-18,-21,-22,-50,]),'EQUAL':([20,21,32,45,46,48,49,50,51,52,],[-32,-33,42,70,-24,-25,-26,-27,-28,-29,]),'ASC':([20,21,103,],[-32,-33,105,]),'DESC':([20,21,103,],[-32,-33,107,]),'LIMIT':([20,21,35,36,43,46,48,49,50,51,52,53,55,76,77,78,83,84,85,86,87,88,90,103,104,105,106,107,],[-32,-33,-17,-5,-16,-24,-25,-26,-27,-28,-29,-5,-39,-23,-5,-38,-19,-20,-18,-21,-22,95,-41,-5,-40,-42,-43,-44,]),'TAIL':([20,21,35,36,43,46,48,49,50,51,52,53,55,76,77,78,83,84,85,86,87,88,90,103,104,105,106,107,],[-32,-33,-17,-5,-16,-24,-25,-26,-27,-28,-29,-5,-39,-23,-5,-38,-19,-20,-18,-21,-22,96,-41,-5,-40,-42,-43,-44,]),'SIMICOLON':([20,21,30,31,35,36,40,43,46,48,49,50,51,52,53,55,56,57,61,62,63,64,76,77,78,83,84,85,86,87,88,90,91,92,94,97,101,102,103,104,105,106,107,],[-32,-33,-5,-59,-17,-5,60,-16,-24,-25,-26,-27,-28,-29,-5,-39,79,-54,-58,-57,-48,-49,-23,-5,-38,-19,-20,-18,-21,-22,-5,-41,-53,-52,100,-47,-45,-46,-5,-40,-42,-43,-44,]),'LPAREN':([22,34,38,44,47,65,66,80,],[28,44,58,44,44,44,44,58,]),'VALUES':([22,27,29,59,],[-5,38,-56,-55,]),'WHERE':([24,30,31,36,50,51,52,53,55,61,62,63,64,78,],[34,34,-59,-5,-27,-28,-29,34,-39,-58,-57,-48,-49,-38,]),'NOT':([34,44,47,65,66,],[47,47,47,47,47,]),'STRING':([34,42,44,47,58,65,66,68,69,70,71,72,73,74,75,93,],[46,63,46,46,63,46,46,86,46,-10,-11,-12,-13,-14,-15,63,]),'NEGATIVE_INTNUMBER':([34,42,44,47,58,65,66,69,70,71,72,73,74,75,93,],[50,50,50,50,50,50,50,50,-10,-11,-12,-13,-14,-15,50,]),'POSITIVE_INTNUMBER':([34,42,44,47,58,65,66,69,70,71,72,73,74,75,93,95,96,],[51,51,51,51,51,51,51,51,-10,-11,-12,-13,-14,-15,51,101,102,]),'FLOATNUMBER':([34,42,44,47,58,65,66,69,70,71,72,73,74,75,93,],[52,52,52,52,52,52,52,52,-10,-11,-12,-13,-14,-15,52,]),'ORDER':([35,36,43,46,48,49,50,51,52,53,55,76,77,78,83,84,85,86,87,],[-17,-5,-16,-24,-25,-26,-27,-28,-29,-5,-39,-23,89,-38,-19,-20,-18,-21,-22,]),'AND':([43,46,48,49,50,51,52,67,76,83,84,85,86,87,],[65,-24,-25,-26,-27,-28,-29,65,65,65,65,-18,-21,-22,]),'OR':([43,46,48,49,50,51,52,67,76,83,84,85,86,87,],[66,-24,-25,-26,-27,-28,-29,66,66,66,66,-18,-21,-22,]),'LIKE':([45,46,48,49,50,51,52,],[68,-24,-25,-26,-27,-28,-29,]),'NOTEQUAL':([45,46,48,49,50,51,52,],[71,-24,-25,-26,-27,-28,-29,]),'BIGGER_EQUAL':([45,46,48,49,50,51,52,],[72,-24,-25,-26,-27,-28,-29,]),'BIGGER':([45,46,48,49,50,51,52,],[73,-24,-25,-26,-27,-28,-29,]),'SMALLER_EQUAL':([45,46,48,49,50,51,52,],[74,-24,-25,-26,-27,-28,-29,]),'SMALLER':([45,46,48,49,50,51,52,],[75,-24,-25,-26,-27,-28,-29,]),'BY':([89,],[98,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'start':([0,],[1,]),'select':([0,],[2,]),'insert':([0,],[3,]),'update':([0,],[4,]),'delete':([0,],[5,]),'distinct':([6,],[10,]),'empty':([6,22,24,30,36,53,77,88,103,],[12,29,35,35,55,35,90,97,106,]),'select_columns':([10,],[16,]),'columns':([10,26,28,],[18,37,39,]),'column':([10,23,26,28,41,98,],[19,32,19,19,32,103,]),'icolumn':([22,],[27,]),'assigns':([23,41,],[30,61,]),'assign':([23,41,],[31,31,]),'where':([24,30,53,],[33,40,77,]),'conditions':([34,44,47,65,66,],[43,67,76,83,84,]),'exp':([34,44,47,65,66,69,],[45,45,45,45,45,87,]),'NUMBER':([34,42,44,47,58,65,66,69,93,],[49,64,49,49,64,49,49,49,64,]),'into':([36,],[53,]),'insert_values':([38,80,],[56,91,]),'single_values':([38,80,],[57,57,]),'value':([42,58,93,],[62,82,82,]),'logical':([45,],[69,]),'values':([58,93,],[81,99,]),'order':([77,],[88,]),'limit_or_tail':([88,],[94,]),'way':([103,],[104,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> select','start',1,'p_start','yacc.py',5),
  ('start -> insert','start',1,'p_start','yacc.py',6),
  ('start -> update','start',1,'p_start','yacc.py',7),
  ('start -> delete','start',1,'p_start','yacc.py',8),
  ('empty -> <empty>','empty',0,'p_empty','yacc.py',13),
  ('select -> SELECT distinct select_columns FROM DATASOURCE into where order limit_or_tail SIMICOLON','select',10,'p_select','yacc.py',27),
  ('insert -> INSERT INTO DATASOURCE icolumn VALUES insert_values SIMICOLON','insert',7,'p_insert','yacc.py',61),
  ('update -> UPDATE DATASOURCE SET assigns where SIMICOLON','update',6,'p_update','yacc.py',79),
  ('delete -> DELETE FROM DATASOURCE where','delete',4,'p_delete','yacc.py',89),
  ('logical -> EQUAL','logical',1,'p_logical','yacc.py',99),
  ('logical -> NOTEQUAL','logical',1,'p_logical','yacc.py',100),
  ('logical -> BIGGER_EQUAL','logical',1,'p_logical','yacc.py',101),
  ('logical -> BIGGER','logical',1,'p_logical','yacc.py',102),
  ('logical -> SMALLER_EQUAL','logical',1,'p_logical','yacc.py',103),
  ('logical -> SMALLER','logical',1,'p_logical','yacc.py',104),
  ('where -> WHERE conditions','where',2,'p_where','yacc.py',114),
  ('where -> empty','where',1,'p_where_empty','yacc.py',119),
  ('conditions -> LPAREN conditions RPAREN','conditions',3,'p_cond_parens','yacc.py',124),
  ('conditions -> conditions AND conditions','conditions',3,'p_cond_3','yacc.py',129),
  ('conditions -> conditions OR conditions','conditions',3,'p_cond_3','yacc.py',130),
  ('conditions -> exp LIKE STRING','conditions',3,'p_cond_3','yacc.py',131),
  ('conditions -> exp logical exp','conditions',3,'p_cond_3','yacc.py',132),
  ('conditions -> NOT conditions','conditions',2,'p_conditions_not','yacc.py',137),
  ('exp -> STRING','exp',1,'p_exp','yacc.py',147),
  ('exp -> COLNAME','exp',1,'p_exp','yacc.py',148),
  ('exp -> NUMBER','exp',1,'p_exp','yacc.py',149),
  ('NUMBER -> NEGATIVE_INTNUMBER','NUMBER',1,'p_NUMBER','yacc.py',158),
  ('NUMBER -> POSITIVE_INTNUMBER','NUMBER',1,'p_NUMBER','yacc.py',159),
  ('NUMBER -> FLOATNUMBER','NUMBER',1,'p_NUMBER','yacc.py',160),
  ('distinct -> DISTINCT','distinct',1,'p_distinct','yacc.py',170),
  ('distinct -> empty','distinct',1,'p_distinct_empty','yacc.py',175),
  ('column -> COLNUMBER','column',1,'p_column','yacc.py',183),
  ('column -> COLNAME','column',1,'p_column','yacc.py',184),
  ('columns -> columns COMMA columns','columns',3,'p_columns','yacc.py',189),
  ('columns -> column','columns',1,'p_columns_base','yacc.py',196),
  ('select_columns -> TIMES','select_columns',1,'p_select_columns_all','yacc.py',206),
  ('select_columns -> columns','select_columns',1,'p_select_columns','yacc.py',211),
  ('into -> INTO DATASOURCE','into',2,'p_into','yacc.py',221),
  ('into -> empty','into',1,'p_into_empty','yacc.py',226),
  ('order -> ORDER BY column way','order',4,'p_order','yacc.py',235),
  ('order -> empty','order',1,'p_order_empty','yacc.py',240),
  ('way -> ASC','way',1,'p_way_asc','yacc.py',245),
  ('way -> empty','way',1,'p_way_asc','yacc.py',246),
  ('way -> DESC','way',1,'p_way_desc','yacc.py',251),
  ('limit_or_tail -> LIMIT POSITIVE_INTNUMBER','limit_or_tail',2,'p_limit_or_tail','yacc.py',261),
  ('limit_or_tail -> TAIL POSITIVE_INTNUMBER','limit_or_tail',2,'p_limit_or_tail','yacc.py',262),
  ('limit_or_tail -> empty','limit_or_tail',1,'p_limit_or_tail_empty','yacc.py',270),
  ('value -> STRING','value',1,'p_value','yacc.py',280),
  ('value -> NUMBER','value',1,'p_value','yacc.py',281),
  ('values -> values COMMA values','values',3,'p_values','yacc.py',287),
  ('values -> value','values',1,'p_values_end','yacc.py',299),
  ('single_values -> LPAREN values RPAREN','single_values',3,'p_single_values','yacc.py',304),
  ('insert_values -> insert_values COMMA insert_values','insert_values',3,'p_insert_values','yacc.py',309),
  ('insert_values -> single_values','insert_values',1,'p_insert_values_end','yacc.py',316),
  ('icolumn -> LPAREN columns RPAREN','icolumn',3,'p_icolumn','yacc.py',326),
  ('icolumn -> empty','icolumn',1,'p_icolumn_empty','yacc.py',331),
  ('assign -> column EQUAL value','assign',3,'p_assign','yacc.py',341),
  ('assigns -> assign COMMA assigns','assigns',3,'p_assigns','yacc.py',346),
  ('assigns -> assign','assigns',1,'p_assigns_end','yacc.py',351),
]
