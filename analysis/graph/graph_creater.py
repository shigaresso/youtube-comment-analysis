import matplotlib.pyplot as plot

def create_coordinates(data_frame_column):
    # 1 分単位で集計している引数から matplotlib で用いる配列を作成する

    # 1 分単位のコメントを集計していると思うので、そこから横軸用の座標を作成する（単位は 1 分）
    x = list(range(len(data_frame_column)))
    # 縦軸は 1 分単位で集計されているコメント数を list 化しただけ
    y = data_frame_column.tolist()
    return x, y

def create_matplotlib(count_per_minutes):
    # 引数は 1 分単位で集計した値が複数含まれる可能性がある
    plot.xlabel("minute")
    plot.ylabel("comment_count_per_minute")

    count_x, count_y = create_coordinates(count_per_minutes["message"])
    plot.plot(count_x, count_y, "o-", color="blue")

    search_x, search_y = create_coordinates(count_per_minutes["contain"])
    plot.plot(search_x, search_y, "o-", color="black")

    plot.show()
