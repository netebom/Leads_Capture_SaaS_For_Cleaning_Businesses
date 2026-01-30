import os

PAYSTACK_SECRET_KEY = os.getenv(
    "PAYSTACK_SECRET_KEY",
    "sk_test_75b0c6ea56aa16189f71f479bd7eae4ecc4f67af"
)

PAYSTACK_PUBLIC_KEY = os.getenv(
    "PAYSTACK_PUBLIC_KEY",
    "pk_test_13aef872b0d09d49bc836bee06dcb7db762f37a4"
)

BASE_URL = os.getenv(
    "BASE_URL",
    "http://127.0.0.1:5000"
)

BASIC_PLAN_PRICE_NGN = int(os.getenv(
    "BASIC_PLAN_PRICE_NGN",
    "3000000"
))