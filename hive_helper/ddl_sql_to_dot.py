#!/usr/bin/python
from pyparsing import Literal,CaselessLiteral,Word,delimitedList,Optional,Combine,Group,alphas,nums,alphanums,Forward,oneOf,sglQuotedString,OneOrMore,ZeroOrMore, CharsNotIn,Suppress

parenthesis = Forward()        

parenthesis <<= "(" + ZeroOrMore(CharsNotIn("()") | parenthesis)  + ")"

field_def = OneOrMore(Word(alphanums+"_\"':-") | parenthesis)

def field_act(s,loc,tok):
    return ("<"+tok[0]+"> " + " ".join(tok)).replace("\"","\\\"")
    
field_def.setParseAction(field_act)

field_list_def =  field_def + ZeroOrMore(Suppress(",") + field_def)

def field_list_act(s,loc,tok):
    return " | ".join(tok)
    
field_list_def.setParseAction(field_list_act)

create_table_def = Literal("CREATE")+"TABLE"+Word(alphas).setResultsName("tableName")+"("+field_list_def.setResultsName("fields")+")"+";"

def create_table_act(s,loc,tok):
    return """"%(tableName)s" [\n\t label="<%(tableName)s> %(tableName)s | %(fields)s"\n\t shape="record"\n];""" % tok

create_table_def.setParseAction(create_table_act)

add_fkey_def=Literal("ALTER")+"TABLE"+"ONLY" + Word(alphanums+"_").setResultsName("tableName") + "ADD"     + "CONSTRAINT" + Word(alphanums+"_") + "FOREIGN"+"KEY"+"("+Word(alphanums+"_").setResultsName("keyName")+")"     +"REFERENCES"+Word(alphanums+"_").setResultsName("fkTable")+"("+Word(alphanums+"_").setResultsName("fkCol")+")"+";"
    
def add_fkey_act(s,loc,tok):
    return """ "%(tableName)s":%(keyName)s -> "%(fkTable)s":%(fkCol)s """ % tok

add_fkey_def.setParseAction(add_fkey_act)

other_statement_def = ( OneOrMore(CharsNotIn(";") )  + ";")

def other_statement_act(s,loc,tok):
    return ""
    
other_statement_def.setParseAction(other_statement_act)

comment_def = "--" + ZeroOrMore(CharsNotIn("\n"))

comment_def.setParseAction(other_statement_act)

statement_def =  comment_def | create_table_def | add_fkey_def | other_statement_def

defs =  OneOrMore(statement_def)

print """digraph g { graph [ rankdir = "LR" ]; """

for i in defs.parseFile("dump.sql"):
    if i!="":
        print i
print "}"