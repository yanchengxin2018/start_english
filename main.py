import requests, json, os
from settings import ip, username, password
#input

# 得到一张无参数卡片
def get_new_card():
    global headers, card
    response_obj = requests.get('{}/main/get_word_card/'.format(ip), headers=headers)
    data = response_obj.content
    card = json.loads(data)


headers = ''

# 请求地址
commit_url = '{}/main/get_word_card/'.format(ip)
# 请求函数
commit_handler = get_new_card
# 请求参数
word_index = ''
spell = ''
# 响应参数
card = ''


# 得到头
def get_headers():
    global headers
    url = '{}/user/log/'.format(ip)
    response_obj = requests.post(url, data={'username': username, 'password': password})
    data = response_obj.content
    data = json.loads(data)
    token = data.get('token')
    headers = {'Authorization': 'JWT {}'.format(token)}


def main():
    global card, spell, commit_url
    order=input('Q键退出,其他键继续')
    if order=='Q':
        print('bay')
        return

    get_headers()

    while True:
        if spell=='Q':
            print('bay')
            break
        # 请求
        print('正在请求新卡片...')
        get_card()
        # 解析响应
        parse_card()
        # 清屏
        os.system('clear')
        # 显示
        show_card()


def get_card():
    commit_handler()


# 解析卡片
def parse_card():
    global card, commit_url, commit_handler
    card_type = card.get('card_type')
    if card_type == 'update_card':
        commit_url = '{}/main/update_card_commit/'.format(ip)
        commit_handler = update_commit
    elif card_type == 'new_card':
        commit_url = '{}/main/new_card_commit/'.format(ip)
        commit_handler = new_commit
    elif card_type == 'info_card':
        commit_url = '{}/main/get_word_card/'.format(ip)
        commit_handler = get_new_card
    elif card_type == 'strengthen_card':
        commit_url = '{}/main/strengthen_card_commit/'.format(ip)
        commit_handler = strengthen_commit
    else:
        print('暂时不能解析{}'.format(card_type))
        print(card)
        input('任意键继续')


# 显示卡片
def show_card():
    global card, spell
    card_type = card.get('card_type')
    if card_type == 'new_card':
        new_card_show()
    elif card_type == 'update_card':
        updata_card_show()
        spell = input('输入英语单词:')
    elif card_type == 'strengthen_card':
        strengthen_card_show()
        spell = input('输入英语单词:')
    elif card_type == 'info_card':
        info_card_show()
        input('任意键继续')
    else:
        print('卡片类型不能识别')
        print(card_type)
        input('任意键继续')


#新卡提交
def new_commit():
    global headers, card, spell
    word_index = card.get('word_index')
    data = {'word_index': word_index}
    response_obj = requests.post('{}/main/new_card_commit/'.format(ip), headers=headers, data=data)
    data = response_obj.content
    card = json.loads(data)


# 升级卡提交
def update_commit():
    global headers, card, spell
    word_index = card.get('word_index')
    data = {'word_index': word_index, 'spell': spell}
    response_obj = requests.post('{}/main/update_card_commit/'.format(ip), headers=headers, data=data)
    data = response_obj.content
    card = json.loads(data)


# 加强卡提交
def strengthen_commit():
    global headers, card, spell
    word_index = card.get('word_index')
    data = {'word_index': word_index, 'spell': spell}
    response_obj = requests.post('{}/main/strengthen_card_commit/'.format(ip), headers=headers, data=data)
    data = response_obj.content
    card = json.loads(data)

#新卡显示
def new_card_show():
    global card, word_index
    word_index = card.get('word_index')

    english = card.get('english')
    chinese = card.get('chinese')
    pronunciation = card.get('pronunciation')
    line()
    context('新卡片')
    line()
    context(english)
    line()
    context(chinese)
    line()
    context(pronunciation)
    line()

# 升级卡显示
def updata_card_show():
    global card, word_index
    word_index = card.get('word_index')
    chinese = card.get('chinese')
    line()
    context('测试卡')
    line()
    context(chinese)
    line()


# 加强卡显示
def strengthen_card_show():
    global card, word_index
    word_index = card.get('word_index')
    chinese = card.get('chinese')
    line()
    context('加强测试卡')
    line()
    context(chinese)
    line()


# 信息卡显示
def info_card_show():
    global card, word_index
    level_alter = card.get('level_alter')
    is_right = card.get('is_right')
    spell = card.get('spell')
    next_memory_time = card.get('next_memory_time')
    pronunciation = card.get('pronunciation')
    word_index = card.get('word_index')
    chinese = card.get('chinese')
    english = card.get('english')
    line()
    is_right = '正确' if is_right else '错误'
    context('信息卡(拼写{})'.format(is_right))
    line()
    context('正确单词:{}'.format(english))
    context('拼写{}:{}'.format(is_right, spell))
    line()
    context(chinese)
    context(pronunciation, xiuzheng=2)
    line()
    context(level_alter, xiuzheng=1)
    context(next_memory_time)
    line()


# 显示线
def line(n=40):
    print('+{}+'.format('-' * n))


# 显示行
def context(context, n=40, xiuzheng=0):
    s = 0
    for i in context:
        if ord(i) > 200:
            s += 1
    argv = n - s
    if xiuzheng == 1:
        argv += 1
    if xiuzheng == 2:
        argv = n
    format_argv = ':^{}'.format(argv)
    format_str = '|{' + format_argv + '}|'
    line = format_str.format(context)
    print(line)


if __name__ == '__main__':
    main()
