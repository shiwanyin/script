import os
import sys
import subprocess

annovar="/software/docker_tumor_base/Resource/Annovar/"
def run(vcf,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out = outdir + "/" + prefix
    par = " -protocol refGene,cytoBand,snp138,avsnp150,exac03,esp6500siv2_all,1000g2015aug_all,gnomad211_exome,gnomad211_genome,cosmic88_coding,clinvar_20190305,ljb26_all,intervar_20180118"
    par += " -operation g,r,f,f,f,f,f,f,f,f,f,f,f "
    par += " -nastring . -polish "
    subprocess.check_call("perl %s/table_annovar.pl %s %s/humandb -buildver hg19 -out %s -remove %s -vcfinput " % (annovar, vcf, annovar, out, par), shell=True)
    
if __name__=="__main__":
    if len(sys.argv)!=4:
        print("python3 %s vcf outdir prefix\n"%(sys.argv[0]))
        print("Email:fanyucai1@126.com")
    else:
        vcf,outdir, prefix=sys.argv[1],sys.argv[2],sys.argv[3]
        run(vcf, outdir, prefix)