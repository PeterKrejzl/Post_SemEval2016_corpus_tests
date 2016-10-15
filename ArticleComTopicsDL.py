# -*- coding: utf-8 -*-
import logging
from bs4 import BeautifulSoup
import urllib
import re
import codecs

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


articles = [
'http://zpravy.idnes.cz/zeman-zpozdeni-rizeni-letoveho-provozu-ceska-delegace-kovac-pohreb-11c-/domaci.aspx?c=A161014_154238_domaci_san',
'http://zpravy.idnes.cz/hrad-odmita-pochybeni-pri-zemanove-ceste-na-kovacuv-pohreb-pa1-/domaci.aspx?c=A161013_201320_domaci_fka',
'http://zpravy.idnes.cz/kauza-dne-radio-impuls-zaoralek-americke-volby-fqh-/domaci.aspx?c=A161013_151308_domaci_jkk',
'http://zpravy.idnes.cz/slovensko-pohreb-exprezident-kovac-db5-/zahranicni.aspx?c=A161013_114558_zahranicni_bur',
'http://zpravy.idnes.cz/atmosfera-na-jednani-vlady-babis-daz-/domaci.aspx?c=A161012_124919_domaci_jj',
'http://zpravy.idnes.cz/chovanec-by-v-prezidentskych-volbach-podporil-zemana-pdg-/domaci.aspx?c=A161012_075404_domaci_jj',
'http://zpravy.idnes.cz/zimola-byl-na-schuzce-u-prezidenta-d5u-/domaci.aspx?c=A161011_194738_domaci_pku',
'http://zpravy.idnes.cz/milos-zeman-jiri-ovcacek-prazsky-hrad-d83-/domaci.aspx?c=A161011_112438_domaci_fer',
'http://zpravy.idnes.cz/prazsky-hrad-soud-omluva-ferdinand-peroutka-milos-zeman-pkt-/domaci.aspx?c=A161011_111858_domaci_fer',
'http://zpravy.idnes.cz/zeman-nechce-po-krajskych-volbach-tancit-na-hrobe-cssd-pf0-/domaci.aspx?c=A161009_110657_domaci_kop',
'http://zpravy.idnes.cz/zeman-migrace-vyroky-rhodos-europoslanec-pittella-fxf-/zahranicni.aspx?c=A161004_213638_zahranicni_ane',
'http://zlin.idnes.cz/prezident-zeman-ve-zlinskem-kraji-pred-krajskymi-volbami-2016-pl0-/zlin-zpravy.aspx?c=A161003_2276774_zlin-zpravy_ras',
'http://zpravy.idnes.cz/milos-zeman-rozhovor-financial-times-uprchlici-f5u-/zahranicni.aspx?c=A161002_111538_zahranicni_pku',
'http://zpravy.idnes.cz/zeman-jakunin-islamsky-stat-rhodos-projev-fjt-/zahranicni.aspx?c=A160930_133907_zahranicni_ert',
'http://zpravy.idnes.cz/trenyrky-na-hrade-ztohoven-soud-stiznost-zalobkyne-f9n-/domaci.aspx?c=A160927_093738_domaci_hro',
'http://zpravy.idnes.cz/milos-zeman-valne-shromazdeni-osn-new-york-boj-proti-terorismu-ps6-/zahranicni.aspx?c=A160921_154902_zahranicni_fer',
'http://zpravy.idnes.cz/rozstrel-prezident-milos-zeman-dno-/domaci.aspx?c=A160920_090500_domaci_pku',
'http://zpravy.idnes.cz/rozstrel-idnes-cz-rozhovor-jaroslava-plesla-a-prezidentem-milosem-zemanem-167-/domaci.aspx?c=A160919_153656_domaci_jav',
'http://pardubice.idnes.cz/mladika-odvezla-z-mitinku-prezidenta-policie-fnx-/pardubice-zpravy.aspx?c=A160916_155918_pardubice-zpravy_msv',
'http://pardubice.idnes.cz/andrej-babis-milos-zeman-0wx-/pardubice-zpravy.aspx?c=A160915_160037_pardubice-zpravy_jah',
'http://pardubice.idnes.cz/navsteva-prezident-zeman-pardubicky-kraj-fgi-/pardubice-zpravy.aspx?c=A160915_2273286_pardubice-zpravy_jah',
'http://zpravy.idnes.cz/uprchlici-k-nam-prijdou-z-nemecka-ne-balkanskou-cestou-tvrdi-zeman-101-/domaci.aspx?c=A160914_190037_domaci_kop',
'http://zpravy.idnes.cz/zeman-rozhovor-the-guardian-d1a-/zahranicni.aspx?c=A160914_104339_zahranicni_ert',
'http://zpravy.idnes.cz/peroutka-odvolani-soud-0v2-/domaci.aspx?c=A160831_204835_domaci_pku',
'http://zpravy.idnes.cz/imhof-medaile-za-zasluhy-zeman-de8-/domaci.aspx?c=A160827_153519_domaci_ane',
'http://zpravy.idnes.cz/nemecko-nemuze-dle-zemana-prenaset-odpovednost-na-zeme-jez-migranty-nezvou-1ba-/domaci.aspx?c=A160825_183258_domaci_kop'
]



def process_article(url):
    #logging.log(logging.INFO, 'processing url = ' + url)

    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r, 'html.parser')

    main_text = ''

    #get keywords
    keywords = []
    for meta in soup.find_all("meta"):
        meta_name = meta.get('name')
        if meta_name == 'keywords':
            keywords = meta.get('content').split(',')
            keywords = ','.join(keywords)



    #get title
    for title in soup.find_all('title'):
        ttt = title.getText().replace(' - iDNES.cz', '')
        #print(title.getText())


    #article has 2 pieces
    #opener and the main text
    for div in soup.find_all('div'):
        if div.get('class') == ['opener']:
            #print(div.getText().strip())
            opener = div.getText().strip()
            #print(opener)
            if len(opener) > 0:
                main_text += opener




    #main text
    for div in soup.find_all('div'):
        if div.get('class') == ['bbtext']:
            article_text = div.getText().strip()
            #print(div.getText().strip())
            article_text = article_text.split()
            article_text = ' '.join(article_text)
            #print(article_text)
            #rint(article_text)
            #print(len(article_text))
            if len(article_text) > 0:
                main_text += ' ' + article_text



    #link to comments
    #first parse normal url to get path
    first_part_of_url = url.split('.cz/')[0] + '.cz'
    for a in soup.find_all('a'):
        if a.get('id') == 'moot-linkin':
            discussion_url = first_part_of_url + a.get('href')
            #print(discussion_url)



    return keywords, ttt, main_text, discussion_url


def get_comments (url, get_users = True):
    comments = []
    users = []

    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r, "html.parser")

    for div in soup.find_all("div"):
        cls = div.get("class")
        if cls == ['contribution']:
            h4s = div.find_all("h4")

            for h4 in h4s:
                links = h4.find_all("a")
                for link in links:
                    user_name = re.sub(r'\d+', '', link.getText())
                    users.append(user_name)

            coms = div.find_all("div")
            for com in coms:
                coms2 = com.find_all("p")
                sentences = ''
                for com2 in coms2:
                    sentences += ' ' + com2.getText().strip()
                if len(sentences) > 0:
                    comments.append(sentences.strip())

    return zip(users, comments)


def get_comments_ext (url):
    print(url)
    url_by_time = url + '&razeni=time'
    print(url_by_time)

    comments = []
    users = []

    go = True
    page_num = 1


    while go:
        print('PAGE = %s' % page_num)

        url_to_call = url_by_time + '&strana=' + str(page_num)


        r = urllib.urlopen(url_to_call).read()
        soup = BeautifulSoup(r, "html.parser")

        for div in soup.find_all("div"):
            cls = div.get("class")
            if cls == ['contribution']:
                h4s = div.find_all("h4")

                for h4 in h4s:
                    links = h4.find_all("a")
                    for link in links:
                        user_name = re.sub(r'\d+', '', link.getText())
                        users.append(user_name)

                coms = div.find_all("div")
                for com in coms:
                    coms2 = com.find_all("p")
                    sentences = ''
                    for com2 in coms2:
                        sentences += ' ' + com2.getText().strip()
                    if len(sentences) > 0:
                        comments.append(sentences.strip())


        #check ending

        for span in soup.find_all('span'):
            spn = span.get('class')
            if spn == ['vh']:
                #print('FINAL PAGE')
                if page_num > 1:
                    go = False

        exist_next = False
        for td in soup.find_all('td'):
            td_n = td.get('class')
            if td_n == ['tac']:
                exist_next = True
        if exist_next == False:
            go = False




        page_num += 1

    return zip(users, comments)



'''
 <td class="tac">

                      <b><span>1</span></b>

                      <a href='http://zpravy.idnes.cz/diskuse.aspx?iddiskuse=A161014_154238_domaci_san&razeni=time&strana=2'><span>2</span></a>

                      <a href='http://zpravy.idnes.cz/diskuse.aspx?iddiskuse=A161014_154238_domaci_san&razeni=time&strana=3'><span>3</span></a>

                      <a href='http://zpravy.idnes.cz/diskuse.aspx?iddiskuse=A161014_154238_domaci_san&razeni=time&strana=4'><span>4</span></a>

                      <a href='http://zpravy.idnes.cz/diskuse.aspx?iddiskuse=A161014_154238_domaci_san&razeni=time&strana=5'><span>5</span></a>

                      <a href='http://zpravy.idnes.cz/diskuse.aspx?iddiskuse=A161014_154238_domaci_san&razeni=time&strana=6'><span>6</span></a>

                      <a href='http://zpravy.idnes.cz/diskuse.aspx?iddiskuse=A161014_154238_domaci_san&razeni=time&strana=7'><span>7</span></a>

                      <a href='http://zpravy.idnes.cz/diskuse.aspx?iddiskuse=A161014_154238_domaci_san&razeni=time&strana=8'><span>8</span></a>

                      <a href='http://zpravy.idnes.cz/diskuse.aspx?iddiskuse=A161014_154238_domaci_san&razeni=time&strana=9'><span>9</span></a>
                  &nbsp;&nbsp;...
      </td>

'''





art_file = codecs.open('articles.txt', 'w', 'utf-8')
com_file = codecs.open('comments.txt', 'w', 'utf-8')
com_ext_file = codecs.open('comments_extended.txt', 'w', 'utf-8')
csv_file = codecs.open('annotate_top.csv', 'w', 'utf-8')






article_id = 1

for url in articles:
    keywords, title, article_text, discussion_url = process_article(url)
    comments = get_comments(discussion_url)

    comments2 = get_comments_ext(discussion_url)





    print('%s ||||| %s ||||| %s ||||| %s ||||| %s ||||| %s' % (article_id, url, discussion_url, title, keywords, article_text))
    art_file.write(str(article_id) + ' ||||| ' + url + ' ||||| ' + discussion_url + ' ||||| ' + title + ' ||||| ' + keywords + ' |||||| ' + article_text + '\n')

    comment_id = 1
    for comment in comments:
        com_file.write(str(comment_id) + ' |||||| ' + str(article_id) + ' ||||| ' + comment[0] + ' ||||| ' + comment[1] + '\n')

        csv_file.write(str(article_id) + '|||||' + str(comment_id) + '|||||' + comment[1] + '|||||')
        for kw in keywords.split(','):
            csv_file.write(kw + '|||||')
        csv_file.write('\n')


        comment_id += 1

    #extended
    comment_ext_id = 1
    for comment in comments2:
        com_ext_file.write(str(comment_ext_id) + ' ||||| ' + str(article_id) + '|||||' + comment[0] + ' ||||| ' + comment[1] + '\n')


        comment_ext_id += 1


    article_id += 1



    if article_id > 0:
        #break
        pass

art_file.close()
com_file.close()
com_ext_file.close()





