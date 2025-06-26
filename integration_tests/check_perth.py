import perth
print("Perth module contents:")
print(dir(perth))
print(f"Perth version: {getattr(perth, '__version__', 'Unknown')}")

# Try to find the correct class
for attr in dir(perth):
    obj = getattr(perth, attr)
    if hasattr(obj, '__call__') and 'watermark' in attr.lower():
        print(f"Found watermarker: {attr}")
        try:
            instance = obj()
            print(f"Successfully created: {instance}")
        except Exception as e:
            print(f"Failed to create {attr}: {e}")
