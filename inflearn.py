from bs4 import BeautifulSoup
import requests
import csv
import argparse


parser = None
args = None

def argparseInit():
    global parser, args
    parser = argparse.ArgumentParser()
    parser.add_argument('URL', help='write only one name per section')
    parser.add_argument('--one-section-name', '-o', action='store_true',
                        help='write only one name per section')
    args = parser.parse_args()


def inflearnFormatter():
    response = requests.get(args.URL)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        curriculum = soup.select('#main > section > div > aside.aside-container.tab-content.tab-toggle.curriculum-container.active > div.aside-content > div.list-content.e-border-scroll-content > div')

        lectureList = []
        curSection = None
        curLecture = None
        curDuration = None

        for divEl in curriculum[0].find_all('div'):
            if 'section-el' not in divEl['class'] and 'unit-el' not in divEl['class']:
                continue
            if 'section-el' in divEl['class']:
                curSection = divEl.text.strip()
                continue
            curLecture = divEl.find('div', {'class':'title'}).text.strip()
            durationStr = divEl.find('div', {'class':'unit-info'}).text.strip()
            duration = int(durationStr.split('분')[0])
            hour = str(duration // 60).zfill(2)
            minute = str(duration % 60).zfill(2)
            curDuration = hour + ':' + minute

            lectureList.append([curSection, curLecture, curDuration])
            if (args.one_section_name):
                curSection = ''

        with open('curriculum.csv', 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            columnName = ['섹션', '강의명', '강의길이']
            writer.writerow(columnName)
            print(columnName)
            writer.writerows(lectureList)
            for lecture in lectureList:
                print(lecture)
    else:
        print("접근할 수 없는 주소입니다.")


if __name__ == '__main__':
    argparseInit()
    inflearnFormatter()

