import os
import re
root_dir="/data/TSO500"
outdir="/data/TSO500/stat"
if not os.path.exists(outdir):
    os.mkdir(outdir)

out_total=open("%s/tumor_vs_normal.tsv"%(outdir),"w")
out_total.write("Tumor\tNormal\tTumor_unique\tOverlap\tNormal_unique\n")
t_path,n_path=[],[]
for (root, dirs, files) in os.walk(root_dir):
    for file in files:
        tmp = os.path.join(root, file)
        array=tmp.split("/")
        if array[-1].endswith(".tmb.tsv"):
            if re.search('NF',array[-1]):
                n_path.append(tmp)
            if re.search('TF',array[-1]):
                t_path.append(tmp)
############################################
for tumor in t_path:
    t_unique, n_unique, common,num= 0, 0, 0,0
    dict_t,dict_n = {},{}
    tumor_name=tumor.split("/")[-2]
    normal_name=re.sub(r'TF',"NF",tumor_name)
    infile = open(tumor, "r")
    f1, f2, f3, f4 = 0, 0, 0, 0
    for line in infile:
        num+=1
        line = line.strip()
        array = line.split("\t")
        if num!=1:
            tmp = array[0] + "_" + array[1] + "_" + array[2] + "_" + array[3]
            if array[f1] == "False" and array[f2] == "Somatic" and array[f3] == "True" and array[f4] == "False":
                dict_t[tmp] = line
        else:
            for k in range(len(array)):
                if array[k] == "GermlineFilterDatabase":
                    f1 = k
                if array[k] == "SomaticStatus":
                    f2 = k
                if array[k] == "CodingVariant":
                    f3 = k
                if array[k] == "GermlineFilterProxi":
                    f4 = k
    infile.close()
    num=0
    for normal in n_path:
        if re.search(normal_name,normal):
            infile = open(normal, "r")
            for line in infile:
                num+=1
                line = line.strip()
                array = line.split("\t")
                if num!=1:
                    if array[f1] == "False" and array[f2] == "Somatic" and array[f3] == "True" and array[f4] == "False":
                        tmp = array[0] + "_" + array[1] + "_" + array[2] + "_" + array[3]
                        dict_n[tmp] = line
                        if tmp in dict_t:
                            common+=1
                        else:
                            n_unique+=1
                else:
                    for k in range(len(array)):
                        if array[k] == "GermlineFilterDatabase":
                            f1 = k
                        if array[k] == "SomaticStatus":
                            f2 = k
                        if array[k] == "CodingVariant":
                            f3 = k
                        if array[k] == "GermlineFilterProxi":
                            f4 = k
            infile.close()
            for tmp1 in dict_t:
                if not tmp1 in dict_n:
                    t_unique += 1
            out_total.write("%s\t%s\t%s\t%s\t%s\n" % (tumor.split("/")[-2], normal.split("/")[-2], t_unique, common, n_unique))
        else:
            pass
out_total.close()