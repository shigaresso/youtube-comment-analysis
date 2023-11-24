import pandas

import user_env
from helper.parser import objects_converted_from, data_frame_converted_from
from graph.graph_creater import create_coordinates, create_matplotlib


# yt-dlp でダウンロードしたコメントデータを pandas で利用する為のデータフレームの作成
json_file_path = input("コメントが保存されている JSON を実行ファイルからの相対パスでファイル名を指定：")
objects = objects_converted_from(json_file_path)
data_frame = data_frame_converted_from(objects)

# コメント内容（DataFrame の各行）が条件を満たしているかを True False で返す
is_contain_text = data_frame["message"].str.contains(user_env.regex)
# 正規表現を満たしていたかどうかを表す列をデータフレームに追加する
data_frame["contain"] = is_contain_text
print(data_frame)
# コメントデータを pandas で使えるようになったので 1 分毎のコメント数に集計する
count_per_minute = data_frame.groupby(pandas.Grouper(key="time", freq="1min"))["message"].count().reset_index()
print(count_per_minute)
# 満たしていたコメントのみを 1 分ごとに集計する
search_text_per_minute = data_frame[data_frame["contain"] == True].groupby(pandas.Grouper(key="time", freq="1min"))["contain"].count().reset_index()
print(search_text_per_minute)
# 1 分単位に集計したコメント（単純なコメント、正規表現を満たしたコメント）を 1 つのデータフレームに結合する
per_minute_comments = count_per_minute.merge(search_text_per_minute, on="time", how="left")
# 列が存在しなかった部分が NaN となってしまうので 0 に置き換える
per_minute_comments = per_minute_comments.fillna({"contain": 0})

# left join した時に NaN がでるので float 型になってしまった数値を int 型にもどす
per_minute_comments["contain"] = per_minute_comments["contain"].astype("int")
print(per_minute_comments)
# 1 分ごとに集計した値から matplotlib で描画するためのコードを呼び出す
create_matplotlib(per_minute_comments)
