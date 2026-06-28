import time
import logging
from functools import wraps
from typing import Any, Callable


logger = logging.getLogger(__name__)

def time_logger(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # 1. 開始時間を記録
        start_time = time.perf_counter()
        # 2. 本物の関数（func）を実行して結果を受け取る
        result = func(*args, **kwargs)
        # 3. 終了時間を記録して、ログやプリントで実行時間を表示
        end_time = time.perf_counter()
        process_time = end_time - start_time
        # 4. 結果を返す
        logger.info(f"[{func.__name__}] 実行時間: {process_time:.6f} 秒")
        return result
    return wrapper

def action_logger(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # 前処理：関数が呼ばれたことをログに書く
        logger.info(f"★ [{func.__name__}] の処理を開始します")

        result = func(*args, **kwargs)

        # 後処理：関数が終わったことをログに書く
        logger.info(f"☆ [{func.__name__}] の処理が終了しました")
        return result
    return wrapper
