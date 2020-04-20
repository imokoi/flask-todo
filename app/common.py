"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/20 3:24 PM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/20 3:24 PM
"""


def api_result(status: bool, code: int, message: str, data: dict = None) -> dict:
    if data:
        return {
            "status": status,
            "code": code,
            "data": data,
            "message": message
        }
    else:
        return {
            "status": status,
            "code": code,
            "message": message
        }