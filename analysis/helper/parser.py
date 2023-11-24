import pandas
import json
import datetime

def timestampUsec_to_datetime(timestamp_usec):
    """timestampUsec を datetime 型に変換します。
    Args:
      timestamp_usec: マイクロ秒単位のタイムスタンプ
    Returns:
      datetime 型のタイムスタンプ
    """
    # 秒単位のタイムスタンプを取得
    seconds = timestamp_usec // 10**6
    # タイムスタンプを datetime 型に変換
    datetime_time = datetime.datetime(1970, 1, 1, 0, 0, 0, 0) + datetime.timedelta(seconds=seconds)
    return datetime_time


def objects_converted_from(jsonl_file_path):
    """yt-dlp から取得したコメントファイルを Python の辞書型配列に変換
    変換する上で、JSON ファイルから必要なデータ（コメントとコメントがされた時間）のみを取得
    また、Pandas に変換する際に、時間が datetime 型である必要があるので、配列に格納する時に時間の変換もしている
    """
    results = []

    with open(jsonl_file_path, "r", encoding="UTF-8") as f:
        for index, row in enumerate(f):
            object_line = json.loads(row.rstrip())
            try:
                chat_message = object_line['replayChatItemAction']['actions'][0]['addChatItemAction']['item']['liveChatTextMessageRenderer']['message']['runs'][0]['text']
                receive_time_timestampUsec = object_line['replayChatItemAction']['actions'][0]['addChatItemAction']['item']['liveChatTextMessageRenderer']['timestampUsec']
                receive_time = timestampUsec_to_datetime(int(receive_time_timestampUsec))
                result = {'time': receive_time, 'message': chat_message}
                results.append(result)
            except KeyError:
                print(f"パス：{jsonl_file_path} の {index+1}行目の JSON 構造には、キー text が含まれていません")

    return results


def data_frame_converted_from(python_object):
    return pandas.DataFrame(python_object)
