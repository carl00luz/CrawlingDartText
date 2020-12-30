# CrawlingDartText

This is for Crawling text from dart which is stands up for financial information

크롤링을 통해 Dart의 기업 보고서를 수집하는 프로그램입니다.

현재는 텍스트 자료인 "기업 보고서"만을 수집합니다.

사용 조건으로는

1. 같은 폴더에 Kospi.csv와 main.py가 위치해야 합니다.

2. date = "ex)20180101"에 수집을 시작할 년도를 입력합니다. 해당일로부터 현재일까지의 기업 보고서를 수집합니다.

3. 77번 라인의 key = "api key를 발급받아 입력하세요"에 Key를 Dart API 요청후 입력해야 합니다.

현재는 패키지화를 하지 않고 제공하는데 이는 나중에 args로 필요한 요소를 바꿀 계획입니다.
