import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import random
import re
import os
import time
from multiprocessing import Process, Pool
#######################################
No={}
if os.path.exists("no_omim.tsv"):
    infile=open("no_omim.tsv",'r')
    for line in infile:
        line = line.strip()
        array = line.split()
        No[array[0]]=1
#######################################
dict={}
if os.path.exists("omim.tsv"):
    infile=open("omim.tsv","r")
    for line in infile:
        line=line.strip()
        array=line.split()
        dict[array[0]]=1
    infile.close()
else:
    outfile = open("omim.tsv", "w")
    outfile.write("#MIM_Number\tLocation\tPhenotype\tPhenotype_MIM_number\tInheritance\tPhenotype_mapping_key\n")
    outfile.close()
#######################################
id=[]
infile=open("mim2gene.txt","r")#https://www.omim.org/static/omim/data/mim2gene.txt(2019-7-3)
for line in infile:
    if not line.startswith("#"):
        line=line.strip()
        array=line.split()
        if not array[0] in dict:
            if not array[0] in No:
                id.append(array[0])
infile.close()
#######################################
#############################在请求头中把User-Agent设置成浏览器中的User-Agent，来伪造浏览器访问
def run(omim_id):
    user_agents =['Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
                  'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
                  'Mozilla/5.0 (Windows Phone 8.1; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; NOKIA; Lumia 530) like Gecko (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'
                  ]#https://www.bing.com/webmaster/help/which-crawlers-does-bing-use-8c184ec0
    ip=["198.27.67.35:3128","94.230.155.137:57701","107.190.148.202:31757","46.243.108.72:31773","94.230.159.145:46749","77.48.21.58:34432",
        "77.48.23.78:36680","190.152.149.114:46124","186.10.84.226:59682","89.34.202.96:36745","200.122.209.78:43624","93.76.211.56:34217",
        "187.111.192.198:51236"]
    url="https://omim.org/entry/%s"%(omim_id)
    proxy={"https":"https://"+random.choice(ip)}
    headers = {'User-Agent': random.choice(user_agents)}
    s = requests.session()
    s.keep_alive = False
    res=requests.get(url,headers=headers,proxies=proxy)
    ret=res.text
    soup=BeautifulSoup(ret,'html.parser')
    outfile = open("omim.tsv", "a+")
    try:
        ########################################table
        Pos=soup.table.tbody.find_all('tr')#####判断表格有多少行
        #########################################Location
        Location=soup.table.tbody.td.span.a.text
        Location = Location.strip()
        ##########################################Phenotype
        Phenotype = []
        num=0
        for i in Pos:
            num+=1
            if num==1:
                str=i.find_all('span',limit=2)
                Phenotype.append(str[1].string.strip())
            else:
                str=i.td.span.string.strip()
                if str:
                    Phenotype.append(str)
        ###########################################Phenotype_MIM_number
        Phenotype_MIM_number=[]
        for i in Pos:
            str=i.find('a',href=re.compile("entry"))
            if str:
                Phenotype_MIM_number.append(str.string)
            else:
                Phenotype_MIM_number.append("_")
        ###########################################
        Inheritance = []
        key = []
        for i in Pos:
            str=i.find_all('abbr')
            tmp=""
            for j in str:
                tmp+=","
                tmp+=j.string
            array=re.split(r'(\d+)',tmp)
            real_key=0
            real_Inheritance=0
            for i in array:
                p1 = re.compile(r'[A-Za-z]')
                p2 = re.compile(r'(\d+)')
                a = p1.findall(i)
                b = p2.findall(i)
                if i.strip(",") != "":
                    if a != []:
                        Inheritance.append(i.strip(","))
                        real_Inheritance = 1
                    if b != []:
                        key.append(i.strip(","))
                        real_key = 1
            if real_key==0:
                key.append("_")
            if real_Inheritance==0:
                Inheritance.append("_")
        for i in range(len(Phenotype)):
            outfile.write(
                "%s\t%s\t%s\t%s\t%s\t%s\n" % (omim_id,Location, Phenotype[i], Phenotype_MIM_number[i], Inheritance[i], key[i]))
        outfile.close()
    except:
        outfile=open("no_omim.tsv","a+")
        outfile.write("%s\n"%(omim_id))
        outfile.close()
        print(omim_id)
if __name__=="__main__":
    start = time.time()
    pool = Pool(processes=200)
    pool.map(run, id)
    end = time.time()
    print("Elapse time is %g seconds" % (end - start))