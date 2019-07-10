#Email:fanyucai1@126.com
import os
import re
def vardict(tumor,vcf,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    infile=open(vcf,"r")
    outfile=open("%s/%s.vcf"%(outdir,tumor),"w")
    outfile.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    name=-2
    for line in infile:
        line=line.strip()
        if line.startswith("#CHROM"):
            array=line.split("\t")
            if array[-2]==tumor:
                name=-2
            else:
                print("please input right tumor sample name!!!")
                break
        if not line.startswith("#"):
            array = line.split("\t")
            info=array[-2].split(":")
            GT=info[0]#GT
            p1=re.compile(r',')
            a=re.findall(array[4])#ALT
            b=re.findall(info[5])#AD
            c=re.findall(info[6])#AF
            Ref_Reads=b[0]
            if a!=[]:
                for i in range(len(a)):
                    ALT=a[i]
                    Alt_Reads=b[i+1]
                    Var=c[i]
                    outfile.write("%s\t%s\t%s\t%s\t%s\t.\t.\tGT=%s;Ref_Reads=%s;Alt_Reads=%s;Var=%s\n"
                                  % (array[0], array[1], array[2], array[3], ALT,GT,Ref_Reads,Alt_Reads,Var))
            else:
                outfile.write("%s\t%s\t%s\t%s\t%s\t.\t.\tGT=%s;Ref_Reads=%s;Alt_Reads=%s;Var=%s\n"
                              %(array[0],array[1],array[2],array[3],array[4],GT,Ref_Reads,b[1],c[0]))
    infile.close()
    outfile.close()