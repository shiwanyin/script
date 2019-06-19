import requests
from bs4 import BeautifulSoup
import re
import time
import random
#############################在请求头中把User-Agent设置成浏览器中的User-Agent，来伪造浏览器访问
user_agents = ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']
proxy_list =["206.189.228.188:8080","138.197.163.225:8080","38.91.107.213:3128","142.93.124.90:3128"]#设置多个代理服务器
vcf="CosmicCodingMuts.vcf"
infile=open(vcf,"r")
outfile=open("cosmic.tsv","w")
outfile.write("#ID\tType\n")
dict={}
for line in infile:
    line=line.strip()
    time.sleep(random.randint(0,2))# 暂停0~1秒，时间区间：[0,1)
    if not line.startswith("#"):
        array=line.split("\t")
        pattern=re.compile(r'(\d+)')
        id=pattern.findall(array[2])
        url = 'https://cancer.sanger.ac.uk/cosmic/mutation/overview?genome=37&id=%s' %(id[0])
        headers = {'User-Agent': random.choice(user_agents)}#随机选择一个User-Agent的
        proxy = random.choice(proxy_list)#随机选取一个代理服务器
        s = requests.session()
        s.keep_alive = False
        s.proxies = {"https":'https://' + proxy}
        res=s.get(url,headers=headers,auth=('yucaifan@chosenmedtech.com', 'Fyc_840924'))
        print(url)
        ret = res.text
        soup=BeautifulSoup(ret,'html.parser')
        dbsnp = soup.find_all(text=re.compile("has been flagged as a SNP."))
        dt = soup.find_all('dt')
        dd = soup.find_all('dd')
        for i in range(len(dt)):
            if dt[i].string == "Ever confirmed somatic?":
                print("%s\t%s" % (array[2], dd[i].string))
                dict[array[2]] = dd[i].string
        if dbsnp!=[]:
            dict[array[2]] = "SNP"
            print("%s\tSNP" % (array[2]))
infile.close()
for key in dict:
    outfile.write("%s\t%s\n" % (key, dict[key]))
outfile.close()
print("#This pcocess done.")