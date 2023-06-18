from flask import Flask, render_template, request
from store_function import get_store_list_in_dong, count_column, create_table_with_selected_columns, plot_bar_chart, plot_pie_chart
from signgu_code import get_signgu_code

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    signgu_name = request.form['signgu_name']
    count_column_value = request.form['indsLclsCd']
    work_code = request.form['WorkCode']

    signgu_code = get_signgu_code(signgu_name)
    if signgu_code is None:
        return render_template('error.html')

    json_data = get_store_list_in_dong(signgu_code, work_code)
    count_result = count_column(json_data, count_column_value)

    selected_columns = [count_column_value+'Nm', count_column_value+'Cd', 'Count']
    result_table = create_table_with_selected_columns(count_result, selected_columns)

    # 그래프 생성
    bar_chart = plot_bar_chart(json_data, count_column_value)
    pie_chart = plot_pie_chart(json_data, count_column_value)

    return render_template('result.html', signgu_name=signgu_name, result_table=result_table, bar_chart=bar_chart, pie_chart=pie_chart)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

