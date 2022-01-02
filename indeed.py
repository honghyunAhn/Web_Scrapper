import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f'https://www.indeed.com/jobs?q=python&limit={LIMIT}'


def extract_indeed_pages():
    result = requests.get(URL)
    # result를 print시 작동된다는 뜻.
    # result.text print시 모든 html을 프린트한다.

    soup = BeautifulSoup(result.text, "html.parser")
    # 위에 쓰여진게 soup 공식인데, soup는 쉽게 말해 데이터를 분류해주는 역할을 한다.
    # 여기서 html_doc을 result.text 로 html document 를 가져와서 적어준것.

    pagination = soup.find("div", {"class": "pagination"})
    # 페이지 관련 검사를 보면, div class="pagination"이 페이지를 나타낸다
    # 따라서 soup는 html을 가져왔으니까 여기서 find해라 어떤걸? div class pagination을 가진 정보들을 가져온다.

    links = pagination.find_all('a')
    # links는 pagination 변수 에서 find all 'a'를 찾아서 리스트를 만들어준것
    # 'a'는 페이지를 가르키는 html에서 2,3,4,5 페이지를 찾는것

    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    # pages를 빈 리스트로 만들어주고 for문을 활용한다.
    # for문은 links 안에서 link라고하고 span을 찾아서 pages에 추가해라

    max_page = pages[-1]
    # max_page를 [-1]로 마지막 값만 나오게 지정

    return max_page


def extract_indeed_jobs(last_page):
    jobs = []
    # for page in range(last_page):
    result = requests.get(f"{URL}&start={0*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("a", {"class": "fs-unmask"})

    for result in results:
        jobTitle = result.find("h2", {"class": "jobTitle"})
        title = jobTitle.find("span").string
        if title == "new":
            title = jobTitle.find_all("span")[1].string

        company = result.find("span", {"class": "companyName"})
        if company is not None:
            company = company.string
        else:
            company = None
        print(title, company)

    return jobs
