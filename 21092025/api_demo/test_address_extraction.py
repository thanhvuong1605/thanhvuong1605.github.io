"""
Test address extraction for Vietnamese addresses
"""
from url_parser import extract_ward_from_address, extract_province_from_address

# Test addresses
test_addresses = [
    "55A Ngô Quang Huy, Thảo Điền, Thủ Đức, Thành phố Hồ Chí Minh 70000",
    "165 Số 6, An Lạc A Bình Tân, Hồ Chí Minh",
    "911/17 Lạc Long Quân, Phường 11, Tân Bình, Thành phố Hồ Chí Minh",
    "123 Nguyễn Huệ, Bến Nghé, Quận 1, TP. HCM",
    "45 Lê Lợi, Phường Bến Thành, Quận 1, Hồ Chí Minh",
    "78 Võ Văn Tần, Phường 6, Quận 3, Thành phố Hồ Chí Minh",
    "Tầng 5, 234 Điện Biên Phủ, Võ Thị Sáu, Quận 3, TP.HCM",
]

print("="*80)
print("Testing Vietnamese Address Extraction")
print("="*80)

for i, address in enumerate(test_addresses, 1):
    print(f"\n{i}. Address: {address}")
    ward = extract_ward_from_address(address)
    province = extract_province_from_address(address)
    print(f"   → Ward: {ward or '❌ Not found'}")
    print(f"   → Province: {province}")

print("\n" + "="*80)
print("✓ Test complete!")

