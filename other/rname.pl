#!/usr/bin/perl

foreach $file (@ARGV){
    print $file,"\n";
}
opendir(DIR,'.');
@dir=readdir DIR;
foreach $file (@dir){
    $temp=$file;
    if($temp =~ s/laun/ab/ ){
        print $temp,"\n",$file,"\n"
        #`mv $file $temp`;
    }
}
