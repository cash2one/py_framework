import re
PAT=re.compile('aa\.(\w+)')

def get_identifier():
	set_f=set()
	fname='create_ads_1111_ec_page_flw_filter_view.hql'
	fname='create_ads_1111_ec_page_flw_view.hql'
	for l in open(fname):
		ms=PAT.findall(l)
		if len(ms)==0:continue
		for m in ms:
			print m
			set_f.add(m)
	print ','.join(sorted(set_f))

import sqlparse
import glob
def u2g(st):
	return st.encode('gbk','ignore')
def find_depend():
	for fname in glob.glob('*.hql'):
	# for fname in glob.glob('../hql/*.hql'):
		st=''.join([l for l in open(fname).readlines()])
		sql= sqlparse.format( st,reindent=True)
		# print u2g(sql)
		print '[%s]'%fname
		for stat in sqlparse.parse(sql):
			# print type(stat);continue
			print_stat(stat,0)
					
def print_stat(stat,i):
	i=i+1
	if i>4:return
	if type(stat)==sqlparse.sql.Identifier:
		iname=u2g(unicode(stat)).split('.')[-1]
		if iname.endswith('_id') or iname in('dt'):
			return
		print iname,i
	elif type(stat)==sqlparse.sql.IdentifierList:
		return
	else:
		# print type(stat)
		for stat in stat.get_sublists():
			print_stat(stat,i)
find_depend()