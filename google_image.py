#-*- coding:utf-8 -*-
# Google の Custom Search Engine で画像を検索して保存
import json
import os
import sys
import urllib2
import httplib2
import shutil
import pickle
from apiclient.discovery import build

def main(query):
  service = build("customsearch", "v1",
                  developerKey="AIzaSyAAw0dvpQixKKnR9A1TROk5iah2BmMrEVE") # API Key (39文字)
  res = service.cse().list(
    q=query,
    searchType='image',
    # imgType='face',
    safe='high',
    cx='018225352934674576036:yuxrk2izns8', # 検索エンジンID (33文字)
    ).execute()

  return res

# URL先の画像ファイルを保存
def url_download(dir,urls):
    if os.path.exists(dir)==False:
        os.mkdir(dir)
    opener = urllib2.build_opener()
    http = httplib2.Http(".cache")
    # URLの数だけ画像DL
    for i in range(len(set(urls))):
        try:
            fn, ext = os.path.splitext(urls[i])
            response, content = http.request(urls[i])
            with open(str(i)+ext, 'wb') as f:
                f.write(content)
            shutil.move((str(i)+ext).encode("utf-8"), dir)
        except:
            continue

if __name__ == '__main__':
  q=sys.argv[1]
  d=sys.argv[2]
  result = main(q)
  pickle.dump(result, open("result_"+d+".dump", "w"))

  print result
  urls=[]
  for el in result['items']:
    urls.append(el['link'])
  print "[download]",urls
  url_download(d,urls)


