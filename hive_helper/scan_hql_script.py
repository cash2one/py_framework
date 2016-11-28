import sqlparse
import glob
import collections
from sqlparse import tokens as Token
DEBUG=False
def u2g(st):
    return unicode(st).encode('gbk','ignore')

def get_tok_name(tok):
    return unicode(' ("%s",%s) '%(tok.normalized,tok.ttype))
    
def get_toks_name(toks):
    return ','.join(map(get_tok_name,toks))
    
def peek_sql(sql):
    stmts=sqlparse.parse(sql)
    stmt=stmts[0]
    print 'Statement type:',stmt.get_type()
    flat_tok=[tok for tok in stmt.flatten()]
    print 'Flatten Tokens:',map(get_tok_name,flat_tok),len(flat_tok)
    print 'Nested Tokens:',map(get_tok_name,stmt.tokens),len(stmt.tokens)
    for tok in stmt.tokens:
        print get_tok_name(tok),
        if tok.is_group:
            print '[sub]:',tok.tokens
    print '#'*8
    return stmt
    
def next_not_empty_type(i,toks):
    for j in range(1,10):
        ttype=toks[i+j].ttype
        if ttype not in (Token.Text.Whitespace, Token.Punctuation ,Token.Text.Whitespace.Newline):
            return ttype,toks[i+j],j
    return ttype,toks[i+j],j
    
def last_not_empty_type(i,toks):
    for j in range(1,10):
        ttype=toks[i-j].ttype
        if ttype not in (Token.Text.Whitespace, Token.Punctuation ,Token.Text.Whitespace.Newline):
            return ttype,toks[i-j],j
    return ttype,toks[i-j],j
        
def find_depend(path):
    tbl_info=collections.defaultdict(set)
    for fname in glob.glob(path):
        # print 'Process File:',fname
        sql=''.join([l for l in open(fname).readlines()])
        # sql= sqlparse.format( st,reindent=True)        
        for statement in sqlparse.parse(sql):
            # print statement.get_type() sqlparse.sql.Identifier            
            toks=[tb_part for tb_part in statement.flatten()]
            ntoks=statement.tokens
            stype=statement.get_type()
            if DEBUG:
                s= get_toks_name(toks)                
                print s.encode('gbk','ignore')
                print ''
            for i,tok in enumerate(toks):
                this_token=tok.normalized
                ### select from
                if (this_token in ('FROM','JOIN') or this_token.endswith('JOIN')) \
                and tok.ttype==Token.Keyword:
                    # print next_not_empty_type(i,toks)
                    if next_not_empty_type(i,toks)[0]!=Token.Name:                        
                        continue
                    tbname=get_tokens_tablename(i,toks)
                    # print tbname
                    tbl_info[fname].add(('depend_table',tbname))
                ### insert create to
                # print stype,'[]',u2g(this_token)
                if stype in ('CREATE','INSERT','CREATE OR REPLACE') \
                and this_token in ('TABLE','VIEW') \
                and tok.ttype==Token.Keyword:
                    if next_not_empty_type(i,toks)[0]!=Token.Name:
                        continue
                    if  str(last_not_empty_type(i,toks)[1]).lower()=='lateral':                    
                        continue
                    tbname=get_tokens_tablename(i,toks)
                    # print tbname
                    tbl_info[fname].add(('operate_table',tbname))
                ### temp function
                if stype=='CREATE' and this_token=='CREATE'\
                and toks[i+2].normalized=='TEMPORARY'  \
                and toks[i+4].normalized=='FUNCTION':
                    # print get_toks_name(toks)
                    func_name=toks[i+6].normalized.strip(';')
                    class_name=toks[i+10].normalized.strip(';')
                    # print func_name,class_name
                    tbl_info[fname].add(('create_function',func_name,class_name))
                ### add jar
                if stype=='UNKNOWN' and this_token=='ADD'\
                and toks[i+2].normalized=='jar' :
                    # print get_toks_name(ntoks[4:])
                    nameparts=[tok.value for tok in ntoks[i+4:-1]]
                    file_name=''.join(nameparts).strip()
                    # print file_name
                    tbl_info[fname].add(('add_jar',file_name))
    #### print result
    for k in tbl_info:
        # print k
        t=['','','','']
        for tup in tbl_info[k]:
            # print k+'\t'+'\t'.join(tup)
            if tup[0]=='depend_table':t[0]+=','+tup[1]
            if tup[0]=='operate_table':t[1]+=','+tup[1]
            if tup[0]=='create_function':t[2]+=','+tup[1]+":"+tup[2]
            if tup[0]=='add_jar':t[3]+=', '+tup[1]
        t=map(lambda x:x.strip(', '),t)
        t.insert(0,k)
        print "\t".join(t)
    # print tbl_info
    return tbl_info

def get_tokens_tablename(i,toks):  
    ttype,namepart,basej=next_not_empty_type(i,toks)
    tbname=str(namepart)
    for j in range(3):
        ppos=i+basej+1+j*2
        npos=i+basej+2+j*2
        if npos>len(toks):
            break
        if str(toks[ppos])!='.':
            break
        elif toks[npos].ttype==Token.Name:
            tbname+='.'+str(toks[npos])        
    return tbname.lower()
    
def parenthetic_contents(string):
    """Generate parenthesized contents in string as pairs (level, contents)."""
    stack = []
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')' and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1: i])
    

if __name__=='__main__':
    path='../create_view/*.hql'
    # path='../hql/ads_1111_ec_app_flw_day.hql'
    # path='../hql/*accu*.hql'
    path='hql_parse_test.hql'
    import optparse,sys
    parser = optparse.OptionParser()
    parser.add_option('-p', '--path', action="store", dest="path", help="path", default=path)
    parser.add_option('-d', '--debug', action="store_true", dest="debug", help="debug", default=False)
    opts, args = parser.parse_args()
    print>>sys.stderr, 'Path mask: ', opts.path
    
    DEBUG=opts.debug
    find_depend(opts.path)