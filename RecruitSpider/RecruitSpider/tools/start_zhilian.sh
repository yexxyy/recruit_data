#!/bin/bash
#Author: xander<yeli.studio@qq.com>
#Program:
#This shell script is used to start scrapy process.
#When the process got down, this script will restart it.


TIMESTAMP(){
    echo $(date "+%Y-%m-%d %H:%M:%S")
}

stop_process_if_running(){
    # $1 -> process name

    running_process_num=$(ps -ef | grep $1 | grep -v grep | wc -l)
    if [ $running_process_num -gt 0 ];then
        echo "$(TIMESTAMP) $1 is running..."
        ps -ef | grep $1 | grep -v grep | awk '{ print $2 }' | xargs kill -9
        if [ $? -eq 0 ]; then
            echo "$1 is killed successfully."
        fi
    else
        echo "$(TIMESTAMP) $1 is not running."
    fi
}

start_process(){
    # $1 -> process name
    # $2 -> project dir
    running_process_num=$(ps -ef | grep $1 | grep -v grep | wc -l)
    if [ $running_process_num -gt 0 ];then
        echo "$(TIMESTAMP) $1 is running, no need to restart..."
    else
        #Before restart scrapy process,delete the requests.queue
        jobdir=$(cat $2/RecruitSpider/settings.py | grep JOBDIR)
        jobdir=${jobdir:7}
        jobdir=${jobdir//"'"/""}
        echo $jobdir
        rm -rf $jobdir/requests.queue

        cd $2
        echo "Current workdir is $PWD"

        nohup scrapy crawl zhilian >> $2/nohup.out &
        if [ $? -eq 0 ];then
            echo "$(TIMESTAMP) $1 starts successfully."
        else
            echo  "$(TIMESTAMP) $1 starts failly."
        fi
    fi
}


process_name="crawl"
project_dir=/Users/yexianyong/Desktop/spider/recruit_data/RecruitSpider


stop_process_if_running $process_name

while true;do
	start_process $process_name $project_dir
	echo "$(TIMESTAMP) This is daemon for $process_name"
	sleep 10
done