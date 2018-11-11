import random


def randomizeBase():
    first = random.randint(0,1)
    second = random.randint(0,1)
    third = random.randint(0,1)

    base = [first, second, third]

    return base


def countingOne(base):
    # 'item == 1'은 주자가 있는 베이스를 의미한다. 인덱스는 0부터 시작하므로 1을 더해준 값을 사용한다.
    base_occupied = [index + 1 for index, item in enumerate(base) if item == 1]

    return base_occupied


def countingScore(base_occupied, hit):

    score = 0
    base = [0, 0, 0]
    hit_kind = {'안타':1, '2루타':2, '3루타':3, '홈런':4}

    for index, item in enumerate(base_occupied):
        if item + hit_kind[hit] <= 3:    # True면 base 정리만, False면 득점 후 base 정리
            base[item + hit_kind[hit] - 1] = 1  # 원래 베이스에 있던 사람 이동
        else:
            score += 1

    # 이제 막 출루한 사람의 위치 조정하는 부분
    if hit != '홈런':
        base[hit_kind[hit] - 1] = 1
    else:
        score += 1  # 솔로 홈런일 경우, 위치 조정하면서 점수 증가
        base = [0,0,0]

    print('score = ', score)

    return base

def main():
    base = randomizeBase()
    print('base = ', base)
    base_occupied = countingOne(base)
    print('base_occupied = ', base_occupied)

    res = countingScore(base_occupied, '홈런')

    print(res)


if __name__ == "__main__":
    main()