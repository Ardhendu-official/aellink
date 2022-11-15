import random
from pymysql import NULL

from sqlalchemy import false, true


class otpGenerate():
    def otpcreate():  # type: ignore
        otp_generate = random.randint(111111,999999)
        return otp_generate

class otpVerify():
    def otp_verify(req_otp_code: str, data_otp_code: str):    # type: ignore
        # return req_otp_code, data_otp_code
        if data_otp_code == NULL:
            return f"otp is not available"
        elif str(req_otp_code) == str(data_otp_code):
            return "true"
        else:
            return "false"

