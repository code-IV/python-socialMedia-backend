import urllib.parse
from fastapi import APIRouter


router = APIRouter(
    prefix='/encode',
    tags=['Encode (EXTRAS)']
)


@router.get('/', status_code=200)
def encode_url(request):
    encoded_url = urllib.parse.quote(request)
    return encoded_url