import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64


def get_store_list_in_dong(signgu_code, workCode):
    key = 'ziPMmWty9CCA45LDM9%2BYSs3xjJx28Y3%2BW6RYoB3RjpexDNO%2BX70d8HlxcQ1QvI8vQtV8pZbWa3%2B7mrE7%2BAQkkA%3D%3D'
    divId = "signguCd"  # 시군구 코드
    url = f"http://apis.data.go.kr/B553077/api/open/sdsc2/storeListInDong?type=json&serviceKey={key}&key={signgu_code}&divId={divId}"

    if len(workCode) == 2:
        url += f"&indsLclsCd={workCode}"
    elif len(workCode) == 5:
        url += f"&indsMclsCd={workCode}"
    else:
        url += f"&indsSclsCd={workCode}"

    response = requests.get(url)
    data = response.content.decode('utf-8')
    json_data = json.loads(data)

    return json_data


def count_column(json_data, countColumn):
    columnNm_list = []
    columnCd_list = []

    nameColumn = countColumn + 'Nm'
    codeColumn = countColumn + 'Cd'

    for item in json_data['body']['items']:
        columnNm_list.append(item[nameColumn])
        columnCd_list.append(item[codeColumn])

    count_df = pd.DataFrame({nameColumn: columnNm_list, codeColumn: columnCd_list})
    count_result = count_df.groupby([nameColumn, codeColumn]).size().reset_index(name='Count')

    return count_result


def create_table_with_selected_columns(df, columns):
    selected_df = df[columns]

    # 'Count' 열을 기준으로 내림차순 정렬
    selected_df = selected_df.sort_values(by='Count', ascending=False)

    html_table = selected_df.to_html(index=False)
    return html_table


def count_indsSclsNm(json_data):
    indsSclsNm_list = []
    indsSclsCd_list = []

    for item in json_data['body']['items']:
        indsSclsNm_list.append(item['indsSclsNm'])
        indsSclsCd_list.append(item['indsSclsCd'])

    count_df = pd.DataFrame({'indsSclsNm': indsSclsNm_list, 'indsSclsCd': indsSclsCd_list})
    count_result = count_df.groupby(['indsSclsNm', 'indsSclsCd']).size().reset_index(name='Count')

    return count_result


def plot_bar_chart(json_data, countColumn):
    indsSclsCd_list = [item[countColumn + 'Cd'] for item in json_data['body']['items']]
    counts = pd.Series(indsSclsCd_list).value_counts().sort_values(ascending=False)

    plt.figure(figsize=(10, 8))
    plt.bar(counts.index, counts.values)
    plt.xlabel(countColumn + 'Cd')
    plt.ylabel('Count')
    plt.title('Frequency of ' + countColumn + 'Cd')
    plt.xticks(rotation=45)
    plt.tight_layout()

    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    encoded_img = base64.b64encode(img_data.getvalue()).decode('utf-8')

    img_html = f'<img src="data:image/png;base64,{encoded_img}" alt="Bar Chart">'

    return img_html


def plot_pie_chart(json_data, countColumn):
    indsSclsCd_list = [item[countColumn + 'Cd'] for item in json_data['body']['items']]
    counts = pd.Series(indsSclsCd_list).value_counts().sort_values(ascending=False)

    plt.figure(figsize=(10, 8))
    plt.pie(counts.values, labels=counts.index, autopct='%1.1f%%')
    plt.title('Frequency of ' + countColumn + 'Cd')
    plt.axis('equal')

    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    encoded_img = base64.b64encode(img_data.getvalue()).decode('utf-8')

    img_html = f'<img src="data:image/png;base64,{encoded_img}" alt="Pie Chart">'

    return img_html

