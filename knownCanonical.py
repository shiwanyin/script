file1="/data/Database/knownCanonical/LRG_RefSeqGene"#ftp://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/RefSeqGene/
file2="/data/Database/knownCanonical/appris_data.principal.txt"#http://appris.bioinfo.cnio.es
genelist="/data/Panel275/gene_list/gene_275.list"
dict={}
infile=open(genelist,"r")
for line in infile:
    line = line.strip()
    array = line.split("\t")
    dict[array[0]]=[]
infile.close()
infile1=open(file1,"r")
for line in infile1:
    line=line.strip()
    array=line.split("\t")
    if array[-1]=="reference standard":
        if array[2] in dict:
            dict[array[2]].append(array[5])
infile1.close()

infile2=open(file2,"r")
for line in infile2:
    line = line.strip()
    array = line.split("\t")
    if array[0] in dict and dict[array[0]]==[] and array[-1]=="PRINCIPAL:1":
        dict[array[0]].append(array[2])
        continue
for line in infile2:
    line = line.strip()
    array = line.split("\t")
    if array[0] in dict and dict[array[0]]==[] and array[-1]=="PRINCIPAL:2":
        dict[array[0]].append(array[2])
        print("PRINCIPAL:2",array[0])
        continue
for line in infile2:
    line = line.strip()
    array = line.split("\t")
    if array[0] in dict and dict[array[0]]==[] and array[-1]=="PRINCIPAL:3":
        dict[array[0]].append(array[2])
        print("PRINCIPAL:3", array[0])
        continue
infile2.close()