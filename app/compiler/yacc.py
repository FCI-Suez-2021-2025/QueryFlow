
start = 'start'
def p_start(p):
    '''start : select 
             | insert 
             | update 
             | delete'''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print("Syntax error!")



###########################
#==== SELECT STATEMENT​​ ====
###########################

def p_select(p):
    'select : SELECT distinct select_columns FROM DATASOURCE into where order limit SIMICOLON'

    if type(p[3]) == str:
        p[3] = "'" + p[3] + "'"

    p[5] = str(p[5]).replace("\\", "\\\\")
    p[6] = str(p[6]).replace("\\", "\\\\")
    p[0] = (
        f"from app import etl\n"
        f"\n"
        f"data = etl.extract('{p[5]}')\n"
        f"data = etl.transform(\n"
        f"   data,\n"
        f"   {{\n"
        f"        'COLUMNS':  {p[3]},\n"
        f"        'DISTINCT': {p[2]},\n"
        f"        'FILTER':   {p[7]},\n"
        f"        'ORDER':    {p[8]},\n"
        f"        'LIMIT':    {p[9]},\n"
        f"    }}\n"
        f")\n"
        f"etl.load(data, '{p[6]}')\n"
    )
    


###########################
#==== INSERT STATEMENT ====
###########################

def p_insert(p):
    'insert : INSERT INTO DATASOURCE icolumn VALUES insert_values SIMICOLON'

    p[3] = str(p[3]).replace("\\", "\\\\")
    p[0] = (
        f"from app import etl\n"
        f"import pandas as pd\n"
        f"\n"
        f"values = {p[6]}\n"
        f"data_destination = '{p[3]}'\n"
        f"data = pd.DataFrame(values, columns={p[4]})\n"
        f"etl.load(data, data_destination)\n"
    )



###########################
#==== Update STATEMENT ====
###########################
def p_update(p):
    'update : UPDATE DATASOURCE SET assigns where SIMICOLON'
    p[0] = None



###########################
#==== DELETE STATEMENT​​ ====
###########################

def p_delete(p):
    'delete : DELETE FROM DATASOURCE where'
    p[0] = None



##########################
#====== COMPARISON =======
##########################

def p_logical(p):
    '''logical :  EQUAL 
                | NOTEQUAL 
                | BIGGER_EQUAL 
                | BIGGER 
                | SMALLER_EQUAL 
                | SMALLER'''
    p[0] = p[1]



##########################
#====== WHERE CLAUSE =====
##########################

def p_where(p):
    'where : WHERE conditions'         
    p[0] = p[2]

def p_where_empty(p):
    'where : empty'
    p[0] = None

def p_cond_parens(p):
    'conditions : LPAREN conditions RPAREN'
    p[0] = p[2]

def p_cond_3(p):
    '''conditions : conditions AND conditions 
                  | conditions OR conditions
                  | exp LIKE STRING
                  | exp logical exp'''
    p[0] = {'type': p[2], 'left': p[1], 'right': p[3]}

def p_conditions_not(p):
    'conditions : NOT conditions'
    p[0] = {p[1]: p[2]}



##########################
#========== EXP ==========
##########################

def p_exp(p):
    '''exp : STRING
           | COLNAME
           | NUMBER''' 
    p[0] = p[1]



###########################
#======== Distinct ========
###########################

def p_distinct(p):
    '''distinct : DISTINCT'''
    p[0] = True

def p_distinct_empty(p):
    '''distinct : empty'''
    p[0] = False


###########################
#======== COLUMNS =========
###########################
def p_column(p):
    '''column : COLNUMBER
               | COLNAME'''
    p[0] = p[1]

def p_columns(p):
    '''columns : columns COMMA columns'''
    p[0] = []
    p[0].extend(p[1])
    p[0].extend(p[3])

def p_columns_base(p):
    '''columns : column'''
    p[0] = [p[1]]


###########################
#===== SELECT COLUMNS​​ =====
###########################

def p_select_columns_all(p):
    'select_columns : TIMES'
    p[0] = '__all__'

def p_select_columns(p):
    'select_columns : columns'
    p[0] = p[1]



###########################
#========= Into ===========
###########################

def p_into(p):
    'into : INTO DATASOURCE'
    p[0] = p[2]

def p_into_empty(p):
    'into : empty'
    p[0] = 'custom::'



###########################
#======= Order by =========
###########################

def p_order_by(p):
    '''order : ORDER BY column way'''
    p[0] = (p[3], p[4])

def p_order_empty(p):
    'order : empty'
    p[0] = None

def p_way_asc(p):
    '''way : ASC 
           | empty'''
    p[0] = 'ASC'

def p_way_desc(p):
    'way : DESC'
    p[0] = 'DESC'



###########################
#========= Limit ==========
###########################

def p_limit(p):
    '''limit : LIMIT NUMBER'''
    if p[2] < 0:
        p[0] = None
    else:
        p[0] = p[2]

def p_limit_empty(p):
    'limit : empty'
    p[0] = None



###########################
#========= VALUES​ =========
###########################

def p_value(p):
    '''value : STRING
             | NUMBER'''
    p[0] = p[1]

def p_values(p):
    'values : values COMMA values'
    p[0] = []
    p[0].extend(p[1])
    p[0].extend(p[3])



###########################
#===== INSERT VALUES​ ======
###########################

def p_values_end(p):
    'values : value'
    p[0] = [p[1]]

def p_single_values(p):
    'single_values : LPAREN values RPAREN'
    p[0] = p[2]

def p_insert_values(p):
    'insert_values : insert_values COMMA insert_values'
    p[0] = []
    p[0].extend(p[1])
    p[0].extend(p[3])

def p_insert_values_end(p):
    'insert_values : single_values'
    p[0] = [p[1]]



###########################
#===== Insert Columns​​ =====
###########################

def p_icolumn(p):
    'icolumn : LPAREN columns RPAREN'
    p[0] = p[2]


def p_icolumn_empty(p):
    'icolumn : empty'
    p[0] = None



###########################
#==== ASSIGNS STATEMENT​​ ===
###########################

def p_assign(p):
    'assign : column EQUAL value'
    p[0] = (p[1], p[3])

def p_assigns(p):
    'assigns : assign COMMA assigns'
    p[0] = [p[1]].extend(p[3])

def p_assigns_end(p):
    'assigns : assign'
    p[0] = [p[1]]

    