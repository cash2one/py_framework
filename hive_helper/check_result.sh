# etl_date=2016-10-24
# hour=08
# hive_check_hour ods.o_p04_web_mall_1111_hongbao_count_i 120 120 $etl_date $hour single
#set -x
# args is table_name sleep_seconds sleep_rounds check_date check_hour check_mode[single/total]
function hive_check_hour()
{
   #参数一：表名，必须设置。
   if [ "x$1" = "x" ];then
      echo "[ERROR] 请输入待检查的表名！"
      return 255
   else
      tb_name=$1
   fi
   tbname=${1:-"dual"}
   #参数二：休眠时间（单位：秒，默认120秒）。
   sleep_time=${2:-"120"}
   #参数三：检查次数（默认120次）
   loop_cnt=${3:-"120"}
   e_date=$(date -d '-1 day' '+%Y-%m-%d')
   e_date=${4:-$e_date}
   e_hour=$(date -d '-1 day' '+%H')
   e_hour=${5:-$e_hour}   
   chk_type=${6:-"total"}
   #检验结果标记
   flag="0" 
   for((j=1;j<=${loop_cnt};j++))
   {
      if [ "$chk_type" = "total" ];then
        c1=$(hive -e "show partitions ${tb_name} partition(dt='$e_date')"|wc -l)
        if [  ${c1} -lt $e_hour  ]  ; then 
            echo sleep ${sleep_time}    
            sleep ${sleep_time}    
        else
            flag="1" 
            break
        fi
      else # single
        c1=$(hive -e "show partitions ${tb_name} partition(dt='$e_date',hour='$e_hour')"|wc -l)
        if [  ${c1} -lt "1"  ]  ; then 
            echo sleep ${sleep_time}    
            sleep ${sleep_time}    
        else
            flag="1" 
            break
        fi        
      fi
   }
   info="${tb_name} $e_date $e_hour $chk_type"
   if [ ${flag} == "0" ]
   then   
      echo "[INFO] 数据生成失败 ${info}"
      return 255
   else
      echo "[INFO] 数据已正常生成 ${info}"
   fi
}


function check_result(){
<<DOC
{do the job}
check_result $?  "$(basename $0)_[yourstep]_${thbase}" 13681300984,13681300984
DOC
  if [ $1 -ne 0 ]
  then
    local progname=$(basename $0) 
    i=${3:-"13681300984"}
    message="以下作业执行报错:""$2"
    appid="sjwj"
    alarm="http://club.api.autohome.com.cn/api/sms/send?_appid=$appid&mobile=$i&message=$message"
    curl  $alarm
    exit 255
  else
    local progname=$(basename $0)
    echo ${progname} "$2" succ
  fi
}
