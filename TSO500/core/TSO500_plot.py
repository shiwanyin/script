import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

TMB_MSI="/data/TSO500/stat/TMB_MSI.tsv"
samplelist="/data/TSO500/samplelist.csv"
outdir="/data/TSO500/stat/"
def run(TMB_MSI,samplelist,outdir):
    infile=open(samplelist,"r")
    normal,tumor=[],[]
    num,f1,f2,f3,rate=0,0,0,0,0
    for line in infile:
        line=line.strip()
        array=line.split(",")
        num+=1
        if num==1:
            for k in range(len(array)):
                if array[k]=="yes_no_illumina":
                    f1=k
                if array[k]=="Remarks":
                    f2=k
                if array[k] == "Pairs":
                    f3=k
                if array[k] == "rate":
                    rate=k
        else:
            if array[f1]=="yes":
                if array[f2]=="T" and array[f3]!="." and array[rate]!="E":
                    tumor.append(array[0])
                    normal.append(array[f3])
    infile.close()
    TMB,MSI,Nonsynonymous_TMB={},{},{}
    infile=open(TMB_MSI,"r")
    num,f4,f5,f6=0,0,0,0
    for line in infile:
        line = line.strip()
        array = line.split("\t")
        num+=1
        if num == 1:
            for k in range(len(array)):
                if array[k] == "Total_TMB":
                    f4 = k
                if array[k] == "Percent_Unstable_Site":
                    f5 = k
                if array[k] == "Nonsynonymous_TMB":
                    f6=k
        if array[f4]!="NaN" and array[f5]!="NaN":
                TMB[array[2]]=array[f4]
                MSI[array[2]]=array[f5]
                Nonsynonymous_TMB[array[2]]=array[f6]
    infile.close()
    outfile=open("%s/plot.tsv"%(outdir),"w")
    outfile.write("Tumor_ID\tTumor_TMB\tTumor_Nonsynonymous_TMB\tTumor_MSI\tNormal_ID\tNormal_TMB\tNormal_Nonsynonymous_TMB\tNormal_MSI\tPairs_TMB\tPairs_MSI\n")

    for k in range(len(tumor)):
        if tumor[k] in TMB and tumor[k] in MSI and normal[k] in TMB and normal[k] in MSI:
            if normal[k]!="TS19387NF" and normal[k]!="TS19033NF":
                t1=float(TMB[tumor[k]])-float(TMB[normal[k]])
                t3=float(MSI[tumor[k]])-float(MSI[normal[k]])
                outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
                              %(tumor[k],TMB[tumor[k]],Nonsynonymous_TMB[tumor[k]],MSI[tumor[k]],normal[k],TMB[normal[k]],Nonsynonymous_TMB[normal[k]],MSI[normal[k]],t1,t3))
    outfile.close()
    df = pd.read_csv("%s/plot.tsv" % (outdir), sep="\t",header=0)
    x = df['Pairs_TMB']
    y = df['Tumor_TMB']
    plt.figure(figsize=(18, 10))
    sns.regplot(x=x, y=y, data=df)
    plt.savefig('%s/TMB_pairs_only.png'%(outdir), dpi=300)


    x = df['Pairs_MSI']
    y = df['Tumor_MSI']
    plt.figure(figsize=(18, 10))
    sns.regplot(x=x, y=y, data=df)
    plt.savefig('%s/MSI_pairs_vs_only.png'%(outdir), dpi=300)

if __name__=="__main__":
    run(TMB_MSI,samplelist,outdir)