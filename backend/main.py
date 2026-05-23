from flask import Flask, jsonify, request, send_from_directory
import json
import os

app = Flask(__name__, static_folder='frontend', static_url_path='')

DATA_FILE = os.path.join(os.path.dirname(__file__), 'schools.json')


def load_schools():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')


@app.route('/api/schools', methods=['GET'])
def get_schools():
    schools = load_schools()
    district = request.args.get('district')
    school_type = request.args.get('type')
    level = request.args.get('level')

    if district:
        schools = [s for s in schools if s.get('district') == district]
    if school_type:
        schools = [s for s in schools if s.get('type') == school_type]
    if level:
        schools = [s for s in schools if s.get('level') == level]

    return jsonify({'code': 200, 'data': schools})


@app.route('/api/schools/<school_id>', methods=['GET'])
def get_school(school_id):
    schools = load_schools()
    school = next((s for s in schools if s.get('id') == school_id), None)
    if school:
        return jsonify({'code': 200, 'data': school})
    return jsonify({'code': 404, 'message': '学校不存在'})


@app.route('/api/recommend', methods=['GET'])
def recommend():
    score = int(request.args.get('score', 0))
    category = request.args.get('category', 'AC').upper()
    schools = load_schools()

    score_key = 'score_ac' if category == 'AC' else 'score_d'

    rush = []
    stable = []
    secure = []

    for s in schools:
        s_score = s.get(score_key, 0)
        if not s_score:
            continue
        diff = score - s_score  # 正数表示成绩高于录取线

        if diff >= -20 and diff < -5:  # 冲：输入分低于录取线5-20分
            rush.append(s)
        elif diff >= -5 and diff <= 10:  # 稳：输入分高于或接近录取线（-5到+10）
            stable.append(s)
        elif diff > 10:  # 保：输入分高于录取线10分以上
            secure.append(s)

    # 按分数降序
    for lst in [rush, stable, secure]:
        lst.sort(key=lambda x: x.get(score_key, 0), reverse=True)

    # 每个类别最多4所
    return jsonify({'code': 200, 'data': {
        'rush': rush,
        'stable': stable,
        'secure': secure
    }})


if __name__ == '__main__':
    print('深圳高中志愿填报查询系统启动中...')
    print('访问 http://localhost:5188')
    app.run(host='0.0.0.0', port=5188, debug=True)