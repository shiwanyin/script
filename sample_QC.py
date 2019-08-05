import os
import sys
import subprocess
picard="/software/picard/picard.jar"
ref="/data/Database/hg19/ucsc.hg19.fasta"
gatk3="/software/gatk/3.7/GenomeAnalysisTK.jar"
def run(target_bed,probe_bed,bam,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    ####BedToIntervalList (Picard)#############
    cmd="java -jar %s BedToIntervalList I=%s O=%s/target.interval_list SD=%s" %(picard,target_bed,outdir,bam)
    subprocess.check_call(cmd,shell=True)
    cmd = "java -jar %s BedToIntervalList I=%s O=%s/probe.interval_list SD=%s" % (picard, probe_bed, outdir, bam)
    subprocess.check_call(cmd, shell=True)
    ####Metrics generated by CollectHsMetrics for the analysis of target-capture sequencing experiments#######
    cmd="java -Xmx40g -jar %s CollectHsMetrics I=%s O=%s.hs_metrics.txt R=%s TARGET_INTERVALS=%s/target.interval_list" \
        " BAIT_INTERVALS=%s/probe.interval_list COVMAX=1000000 "%(picard,bam,out,ref,outdir,outdir)
    subprocess.check_call(cmd,shell=True)
    ####Assess sequence coverage by a wide array of metrics, partitioned by sample, read group, or library#############
    cmd="java -Xmx40g -jar %s -T DepthOfCoverage --minBaseQuality 20 --minMappingQuality 20 -R %s -I %s -nt 8 -o %s -ct 50 -L %s"\
        %(gatk3,ref,bam,out,target_bed)
    subprocess.check_call(cmd,shell=True)


if __name__=="__main__":
    if (len(sys.argv)!=6):
        print("\nUsage:python3 %s target_bed probe_bed bamfile outdir prefix"%(sys.argv[0]))
        print("\nEmail:fanyucai1@126.com")
    else:
        target_bed=sys.argv[1]
        probe_bed=sys.argv[2]
        bam=sys.argv[3]
        outdir=sys.argv[4]
        prefix=sys.argv[5]
        run(target_bed,probe_bed,bam,outdir,prefix)
