#! /bin/bash

infile=../src/data/support_$1
outfile=../patterns/support_$1

if test -d "$outfile"; then
  :
else
  mkdir $outfile
fi

do_this (){
  #echo Case:$2, Pattern: $1
  grep -ri $1 $infile > $outfile/$2
}


noise=".*\t10\.2.*\t.*\t.*\t.*"
do_this $noise noise 

fp=".*\twww\.random\.org\.\t.*\t6\.443\tL"  
do_this $fp fp

ibot=".*\t172\.16.*\t.*\t6\.22\t.*"
do_this $ibot ibot

bot1scan=".*\t192\.168\.1\.6\t.*\t6\.22\tS"
do_this $bot1scan bot1scan

bot2scan=".*\t192\.168\.1\.41\t.*\t6\.22\tS"
do_this $bot2scan bot2scan

bot1login=".*\t192\.168\.1\.6\t.*\t6\.22\tM"
do_this $bot1login bot1login

bot2login=".*\t192\.168\.1\.41\t.*\t6\.22\tM"
do_this $bot2login bot2login

loader=".*\t172\.16\.135\.194\t.*\t6\.8000\tL"
do_this $loader loader

cnc=".*\t.*\t.*\t6\.4567\tS"
do_this $cnc cnc

ddos=".*\t192\.168\.1\.47\t.*\t6\.80\tM"
do_this $ddos ddos

rddos="192\.168\.1\.47\t192\.168\.1\.1\t.*\t17\.53\tS"
do_this $rddos rddos

grep -riv -e "iot" -e $noise -e $fp -e $ibot -e $bot1scan -e $bot2scan -e $bot1login -e $bot2login -e $loader -e $cnc -e $ddos -e $rddos $infile > $outfile/others
