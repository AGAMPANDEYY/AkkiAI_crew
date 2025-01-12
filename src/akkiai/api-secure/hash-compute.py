import hmac
import hashlib
import os 

solution_id="2"
input1="string"
input2="string"
input3="string"

secret_key=os.getenv("SECRET_KEY")
data=f"{solution_id}|{input1}|{input2}|{input3}"

hash=hmac.new(secret_key.encode(), data.encode(), hashlib.sha256).hexdigest()

print(hash)