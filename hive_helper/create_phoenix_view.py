t='''
create view "ads_1111_ec_page_{}" ( pk VARCHAR PRIMARY KEY, "cf"."pv" VARCHAR, "cf"."uv" VARCHAR );
'''
d='''
flw_1_minute
flw_10_minute
flw_30_minute
flw_hour
flw_day
flw_accu_day
flw_accu_hour
'''

for n in d.strip().split('\n'):
    print t.format(n.strip()).strip()